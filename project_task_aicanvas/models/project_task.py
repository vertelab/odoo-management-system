from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    needs = fields.Html(string="Needs")
    solution = fields.Html(string="Solution")
    ai_capability = fields.Selection([
        ('Visuellt', 'Visuellt'),
        ('Audiellt', 'Audiellt'),
        ('Språk', 'Språk'),
        ('Robotik', 'Robotik'),
        ('Upptäcka', 'Upptäcka'),
        ('Prediktering', 'Prediktering'),
        ('Optimera', 'Optimera'),
        ('Skapande', 'Skapande'),
    ], string="AI Capability")


    value = fields.Html(string="Value")
    value_point = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
        ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
    ], string="Value Point", default=None, aggregator="max",
        help="Värde (låg or hög)", group_expand='_read_group_value_point')

    feasibility = fields.Html(string="Feasibility")
    feasibility_point= fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
        ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
    ], string="Feasibility", default=None, aggregator="max",
        help="Genomförbarhet (svårt or lätt)", group_expand='_read_group_feasibility_point')

    # Add coordinate field to store the calculated position in the diagram
    ai_canvas_coordinate = fields.Char(string="Coordinate", help="Coordinate position in the SWOT diagram")

    @api.model
    def _read_group_value_point(self, values, domain):
        all_values = [value[0] for value in self._fields['value_point'].selection]

        # Make sure values contains all possible selection values
        missing_values = set(all_values) - set(values)
        values = values + list(missing_values)

        # Sort values numerically
        values.sort(key=lambda x: int(x) if x else 0)
        return values

    @api.model
    def _read_group_feasibility_point(self, values, domain):
        all_values = [value[0] for value in self._fields['feasibility_point'].selection]

        # Make sure values contains all possible selection values
        missing_values = set(all_values) - set(values)
        values = values + list(missing_values)

        # Sort values numerically
        values.sort(key=lambda x: int(x) if x else 0)
        return values


