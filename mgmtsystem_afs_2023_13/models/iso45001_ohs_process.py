# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Iso45001OhsProcess(models.Model):
    """Arbetsmiljöprocess med AFS-koppling.

    AFS 2023:13 kap. 8 § 18 kräver hissvakt. Det är inte en abstrakt
    regel — den gäller en specifik process (hisskörning) på en specifik
    anläggning. Fälten här gör kravet gripbart: vilka processer som
    omfattas, om hissvakt är utsedd, och vilka som är det.
    """

    _inherit = 'iso45001.ohs.process'

    afs_2023_13_applies = fields.Boolean(
        string='AFS 2023:13 tillämplig',
        help='Processen omfattas av AFS 2023:13 (risker vid vissa typer '
             'av arbeten). Ersätter AFS 2006:6.',
    )
    afs_2023_13_chapters = fields.Char(
        string='Kapitel',
        help='Tillämpliga kapitel, t.ex. "8 kap. 18 § hissvakt".',
    )

    hissvakt_required = fields.Boolean(
        string='Hissvakt krävs',
        compute='_compute_hissvakt_required', store=True,
        help='AFS 2023:13 8 kap. 18 §: hissvakt krävs för varje hiss eller '
             'grupp av hissar som manövreras från samma manöverplats, och '
             'på varje däck som betjänas.',
    )
    hissvakt_assigned = fields.Boolean(
        string='Hissvakt utsedd',
        help='Kryssa när hissvakt är utsedd och informerad. '
             'Allmänna rådet tillåter att trafikvakten tar uppgiften.',
    )
    hissvakt_employee_ids = fields.Many2many(
        'hr.employee',
        'iso45001_process_hissvakt_rel',
        'process_id', 'employee_id',
        string='Utsedda hissvakter',
    )
    hissvakt_gap = fields.Boolean(
        string='Lucka',
        compute='_compute_hissvakt_required', store=True,
        help='Kravet gäller men ingen hissvakt är utsedd.',
    )

    @api.depends('afs_2023_13_applies', 'afs_2023_13_chapters', 'hissvakt_assigned')
    def _compute_hissvakt_required(self):
        for process in self:
            chapters = (process.afs_2023_13_chapters or '').lower()
            applies = process.afs_2023_13_applies and (
                'hissvakt' in chapters or '8 kap' in chapters
            )
            process.hissvakt_required = applies
            process.hissvakt_gap = applies and not process.hissvakt_assigned
