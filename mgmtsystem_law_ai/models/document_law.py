# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import json
import logging
import re

from odoo import _, fields, models
from odoo.tools.mail import html_sanitize

_logger = logging.getLogger(__name__)

# The coworker is asked for JSON and told the exact shape. Models still wrap
# it in prose or a fenced block often enough that a plain json.loads() is not
# enough — this finds the first {...} that parses.
_JSON_BLOCK = re.compile(r'\{.*?\}', re.S)
_FENCE = re.compile(r'```(?:json)?\s*(.*?)```', re.S)


class DocumentLaw(models.Model):
    """AI support on the law register.

    Two independent jobs, both driven by the same coworker:

        action_ai_assess_relevance  — is this law relevant to the company?
        action_ai_summarise         — a summary for the reader

    The results are written back to `law_relevant`, `law_relevance_reason`
    and `law_summary`. Nothing is overwritten unless the coworker returned
    something usable — a failed run leaves the previous answer intact.
    """

    _inherit = 'document.law'

    law_summary = fields.Html(
        string='Summary',
        help='AI-generated summary of the law, written for the reader.',
    )
    law_relevant = fields.Selection(
        selection=[
            ('yes', 'Relevant'),
            ('no', 'Not Relevant'),
        ],
        string='Relevant',
        help='Whether this law concerns the company at all.',
    )
    law_relevance_reason = fields.Text(
        string='Relevance Reason',
        help='Why the coworker judged the law relevant or not.',
    )
    law_ai_checked_on = fields.Datetime(
        string='AI Checked On',
        readonly=True,
    )

    # ── Coworker plumbing ───────────────────────────────────────────────

    def _ai_coworker(self):
        """The coworker that does the law work.

        Looked up by xmlid rather than by name: a customer may rename the
        coworker in the UI, and the buttons must keep working.
        """
        return self.env.ref(
            'mgmtsystem_law_ai.coworker_law_reviewer',
            raise_if_not_found=False,
        )

    def _ai_run(self, agent_xmlid, prompt):
        """Run one agent on one law and return the raw answer text.

        `force_agent` makes the coworker run with that agent's own skills and
        tools instead of the supervisor's — the supervisor delegates, but here
        the question is narrow enough that the delegation round-trip only
        costs tokens.
        """
        self.ensure_one()
        coworker = self._ai_coworker()
        if not coworker:
            _logger.warning(
                'mgmtsystem_law_ai: coworker_law_reviewer saknas — '
                'kör moduluppgradering.')
            return False

        agent = self.env.ref(agent_xmlid, raise_if_not_found=False)
        try:
            return coworker.run(
                prompt,
                force_agent=agent or None,
                record=self,
            )
        except Exception as error:  # noqa: BLE001 — en trasig körning får
            # inte stoppa en cron som går igenom hundra lagar.
            _logger.warning(
                'mgmtsystem_law_ai: coworker-körning misslyckades för %s: %s',
                self.display_name, error)
            return False

    @staticmethod
    def _ai_parse_json(answer):
        """Pull the first JSON object out of an answer, or None.

        Tries the whole string, then a fenced block, then the first {...}
        span. Returns None rather than raising: a malformed answer is a
        normal outcome, not an error.
        """
        if not answer:
            return None
        for candidate in (
            answer,
            *(_FENCE.findall(answer)),
            *(_JSON_BLOCK.findall(answer)),
        ):
            try:
                parsed = json.loads(candidate.strip())
            except (ValueError, TypeError):
                continue
            if isinstance(parsed, dict):
                return parsed
        return None

    # ── The two jobs ────────────────────────────────────────────────────

    def _ai_law_text(self):
        """The text the coworker should read.

        `rss_text` is the plain-text body. Laws with only HTML get the HTML
        stripped, so the model is not fed markup it has to ignore.
        """
        self.ensure_one()
        if self.rss_text:
            return self.rss_text
        if self.rss_html:
            return re.sub(r'<[^>]+>', ' ', self.rss_html)
        return ''

    def action_ai_assess_relevance(self):
        """Ask the coworker whether this law concerns the company."""
        for law in self:
            text = law._ai_law_text()
            if not text:
                continue

            answer = law._ai_run(
                'mgmtsystem_law_ai.agent_law_relevance',
                _(
                    'Bedöm om följande lag är relevant för företaget.\n'
                    'Svara ENDAST med JSON i formen '
                    '{"relevant": true|false, "reason": "..."}.\n\n'
                    'Lag: %(title)s\n\n%(text)s',
                    title=law.rss_titel or '',
                    text=text[:20000],
                ),
            )
            parsed = law._ai_parse_json(answer)
            if not parsed or 'relevant' not in parsed:
                continue

            relevant = parsed.get('relevant')
            if isinstance(relevant, str):
                relevant = relevant.strip().lower() in ('true', 'yes', 'ja')

            law.write({
                'law_relevant': 'yes' if relevant else 'no',
                'law_relevance_reason': parsed.get('reason') or False,
                'law_ai_checked_on': fields.Datetime.now(),
            })
        return True

    def action_ai_summarise(self):
        """Ask the coworker for a summary written for the reader."""
        for law in self:
            text = law._ai_law_text()
            if not text:
                continue

            answer = law._ai_run(
                'mgmtsystem_law_ai.agent_law_summary',
                _(
                    'Sammanfatta följande lag för en läsare som behöver veta '
                    'vad den innebär i praktiken. Skriv i markdown med en '
                    'kort ingress och punktlista över de viktigaste kraven. '
                    'Hitta inte på — står det inte i texten, skriv det inte.'
                    '\n\nLag: %(title)s\n\n%(text)s',
                    title=law.rss_titel or '',
                    text=text[:20000],
                ),
            )
            if not answer or not answer.strip():
                continue

            # The answer is model output, not trusted input: it goes into an
            # Html field that the web client renders. Sanitise before storing.
            law.write({
                'law_summary': html_sanitize(answer),
                'law_ai_checked_on': fields.Datetime.now(),
            })
        return True

    # ── Cron ────────────────────────────────────────────────────────────

    @models.api.model
    def _cron_ai_assess_pending(self):
        """Assess every law that has never been checked.

        Opt-in: only laws in draft, and only when the company has switched
        the cron on. Running this on a full register costs one model call per
        law, so it must not start by itself.
        """
        pending = self.search([
            ('law_ai_checked_on', '=', False),
            ('stage', '=', 'draft'),
        ], limit=50)
        if pending:
            pending.action_ai_assess_relevance()
        return True
