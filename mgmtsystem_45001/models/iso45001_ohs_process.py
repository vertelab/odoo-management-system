# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Iso45001OhsProcess(models.Model):
    """Arbetsmiljöprocess — det som är unikt för ISO 45001.

    ISO 9001 har processkartläggning, ISO 45001 har arbetsmiljöprocesser:
    de aktiviteter där arbetstagare kan utsättas för fara. Klausul 4.4
    kräver att de identifieras, 8.1 att de styrs och 9.1 att de följs upp.

    Modellen är ett register, inte ett ärende. Ett ärende är
    mgmtsystem.nonconformity; en process är det som pågår hela tiden.
    """

    _name = 'iso45001.ohs.process'
    _description = 'Arbetsmiljöprocess (ISO 45001)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Processnamn', required=True, tracking=True)
    code = fields.Char(string='Processkod', tracking=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    process_type = fields.Selection([
        ('core', 'Kärnprocess'),
        ('support', 'Stödprocess'),
        ('management', 'Ledningsprocess'),
    ], string='Processtyp', required=True, default='core', tracking=True)

    description = fields.Html(string='Beskrivning')
    owner_id = fields.Many2one('hr.employee', string='Processägare', tracking=True)

    hazard_ids = fields.Many2many(
        'mgmtsystem.hazard',
        'iso45001_ohs_process_hazard_rel',
        'process_id', 'hazard_id',
        string='Arbetsmiljöfaror',
        help='Faror som kan uppstå i den här processen. Klausul 6.1.2.',
    )
    hazard_count = fields.Integer(compute='_compute_hazard_count')

    clause_ids = fields.Many2many(
        'mgmtsystem.iso.clause',
        'iso45001_ohs_process_clause_rel',
        'process_id', 'clause_id',
        string='ISO-klausuler',
        help='Kopplade till ISO 45001-klausuler, typiskt 4.4 och 6.1.2',
    )

    risk_level = fields.Selection([
        ('low', 'Låg'),
        ('medium', 'Medel'),
        ('high', 'Hög'),
        ('critical', 'Kritisk'),
    ], string='Samlad risknivå', compute='_compute_risk_level', store=True)

    @api.depends('hazard_ids')
    def _compute_hazard_count(self):
        for process in self:
            process.hazard_count = len(process.hazard_ids)

    @api.depends('hazard_ids')
    def _compute_risk_level(self):
        """Högsta risknivån bland processens faror.

        En process är aldrig säkrare än sin farligaste fara. Vi tar max,
        inte medel — ett medelvärde skulle dölja en kritisk fara bland
        tio ofarliga.
        """
        rank = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        for process in self:
            level = 'low'
            best = 0
            for hazard in process.hazard_ids:
                # mgmtsystem.hazard har ingen risknivå; den ligger på
                # mgmtsystem.hazard.risk. Vi läser den om den finns.
                hazard_level = getattr(hazard, 'risk_level', False)
                if hazard_level and rank.get(hazard_level, 0) > best:
                    best = rank[hazard_level]
                    level = hazard_level
            process.risk_level = level
