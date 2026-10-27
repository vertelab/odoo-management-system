# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Myndigheter som publicerar föreskrifter som statiska PDF:er men saknar
# RSS. Sökvägarna är förutsägbara: beteckningen räknas om till filnamn.
#
# Boverket är en Blazor-app — portalen går inte att skrapa, men PDF:erna
# ligger på rinfo.boverket.se/BFS{år}-{nr}/pdf/. Elsäkerhetsverket har
# vanliga statiska filer under /globalassets/foreskrifter/.
#
# Arbetsmiljöverket har ingen förutsägbar sökväg; AFS läggs in manuellt
# eller via document.law:s egen import.
SOURCES = {
    'boverket': {
        'name': 'Boverket',
        'url_template': 'https://rinfo.boverket.se/BFS{year}-{num}/pdf/BFS{year}-{num}.pdf',
    },
    'elsakerhetsverket': {
        'name': 'Elsäkerhetsverket',
        'url_template': 'https://elsakerhetsverket.se/globalassets/foreskrifter/elsak-fs-{year}-{num}.pdf',
    },
}


class LawFetcher(models.TransientModel):
    """Hämtar föreskrifter som PDF när myndigheten saknar RSS.

    Vi kan inte prenumerera på AFS, BFS eller ELSÄK-FS — ingen av dem har
    en feed. Men de publicerar statiska PDF:er på förutsägbara sökvägar.
    Den här wizarden tar en beteckning, bygger URL:en och kontrollerar att
    filen finns. Den laddar inte ner innehållet: document.law äger
    lagposten, och en PDF är ett dokument — inte en lagtext vi kan söka i.
    """

    _name = 'law.fetcher'
    _description = 'Hämta föreskrift som PDF'

    source = fields.Selection(
        selection=[
            ('boverket', 'Boverket (BFS)'),
            ('elsakerhetsverket', 'Elsäkerhetsverket (ELSÄK-FS)'),
        ],
        string='Myndighet', required=True, default='boverket',
    )
    designation = fields.Char(
        string='Beteckning', required=True,
        placeholder='t.ex. 2025:11 eller 2022:3',
        help='År:nummer, utan myndighetsprefix.',
    )
    url = fields.Char(string='URL', compute='_compute_url')
    available = fields.Boolean(string='Filen finns', readonly=True)
    http_status = fields.Integer(string='HTTP-status', readonly=True)
    checked = fields.Boolean(readonly=True)

    @api.depends('source', 'designation')
    def _compute_url(self):
        for rec in self:
            rec.url = rec._build_url()

    def _build_url(self):
        self.ensure_one()
        if not self.designation or ':' not in self.designation:
            return False
        year, num = self.designation.split(':', 1)
        template = SOURCES[self.source]['url_template']
        return template.format(year=year.strip(), num=num.strip())

    def action_check(self):
        """Kontrollera att filen finns, utan att ladda ner den.

        HEAD räcker: vi vill veta om sökvägen är rätt, inte läsa
        innehållet. En föreskrift är ofta flera hundra kilobyte och
        behöver inte passera Odoo för att vi ska veta att den finns.
        """
        self.ensure_one()
        if not self.url:
            raise UserError(_('Ange beteckning som år:nummer, t.ex. 2025:11.'))
        try:
            response = requests.head(self.url, timeout=15, allow_redirects=True)
        except requests.RequestException as exc:
            raise UserError(_('Kunde inte nå %s: %s') % (self.url, exc)) from exc
        self.write({
            'http_status': response.status_code,
            'available': response.status_code == 200,
            'checked': True,
        })
        if response.status_code != 200:
            raise UserError(
                _('Filen finns inte (%(status)s): %(url)s')
                % {'status': response.status_code, 'url': self.url}
            )
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
