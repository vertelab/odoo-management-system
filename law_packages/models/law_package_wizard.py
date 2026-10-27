# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class LawPackageWizard(models.TransientModel):
    """Välj bransch och storlek — få listan över tillämpliga lagar.

    Paketen är byggda per bransch, men en lag gäller inte alla företag i
    branschen. Skyddsombud krävs från fem anställda, arbetsanpassning från
    tio, skyddskommitté från femtio. Ett enmansföretag ska inte se trettio
    lagar det inte omfattas av.

    Wizarden filtrerar på min_employees och size_category, visar vad som
    återstår, och skapar document.law-poster för det användaren väljer.
    """

    _name = 'law.package.wizard'
    _description = 'Välj lagpaket efter bransch och storlek'

    business_type = fields.Selection(
        selection='_selection_business_type',
        string='Bransch', required=True,
    )
    employee_count = fields.Integer(
        string='Antal anställda', default=1, required=True,
        help='Storleken avgör vilka lagar som gäller. Skyddsombud från 5, '
             'arbetsanpassning från 10, skyddskommitté från 50.',
    )
    size_category = fields.Selection(
        selection=[
            ('micro', 'Micro (0-4)'),
            ('small', 'Small (5-49)'),
            ('medium', 'Medium (50-249)'),
            ('large', 'Large (250+)'),
        ],
        string='Storlek', compute='_compute_size_category', store=True,
    )

    package_ids = fields.Many2many(
        'bpm.law.package', string='Paket',
        compute='_compute_packages', store=True,
    )
    line_ids = fields.Many2many(
        'bpm.law.package.line', string='Tillämpliga lagar',
        compute='_compute_lines', store=True,
    )
    line_count = fields.Integer(compute='_compute_lines', store=True)
    excluded_count = fields.Integer(
        string='Bortvalda (storlek)', compute='_compute_lines', store=True,
    )

    @api.model
    def _selection_business_type(self):
        return self.env['bpm.law.package']._fields['business_type'].selection

    @api.depends('employee_count')
    def _compute_size_category(self):
        for rec in self:
            n = rec.employee_count or 0
            if n < 5:
                rec.size_category = 'micro'
            elif n < 50:
                rec.size_category = 'small'
            elif n < 250:
                rec.size_category = 'medium'
            else:
                rec.size_category = 'large'

    @api.depends('business_type')
    def _compute_packages(self):
        Package = self.env['bpm.law.package']
        for rec in self:
            rec.package_ids = Package.search([
                ('business_type', '=', rec.business_type),
                ('active', '=', True),
            ])

    @api.depends('package_ids', 'employee_count', 'size_category')
    def _compute_lines(self):
        for rec in self:
            lines = rec.package_ids.mapped('line_ids')
            applies = lines.filtered(
                lambda l: not l.min_employees or l.min_employees <= rec.employee_count
            )
            rec.line_ids = applies
            rec.line_count = len(applies)
            rec.excluded_count = len(lines) - len(applies)

    def action_create_laws(self):
        """Skapa document.law för de valda lagarna.

        Bara de som saknas: en lag som redan finns som document.law ska
        inte skapas igen. SFS-numret är nyckeln — det är unikt per
        författning och ändras inte vid omtryckning.
        """
        self.ensure_one()
        DocumentLaw = self.env['document.law']
        created = DocumentLaw.browse()
        for line in self.line_ids:
            if line.document_law_id:
                continue
            existing = DocumentLaw.search([
                ('rss_beteckning', '=', line.sfs_number),
            ], limit=1) if line.sfs_number else DocumentLaw.browse()
            if existing:
                line.document_law_id = existing
                continue
            law = DocumentLaw.create({
                'rss_titel': line.name,
                'rss_beteckning': line.sfs_number or False,
                'rss_organ': line.department or False,
            })
            line.document_law_id = law
            created |= law
        return {
            'type': 'ir.actions.act_window',
            'name': _('Skapade lagar'),
            'res_model': 'document.law',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created.ids)] if created else [('id', '=', 0)],
        }
