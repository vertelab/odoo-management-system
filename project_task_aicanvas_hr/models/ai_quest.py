from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AICoworker(models.Model):
    _inherit = "ai.coworker"

    def _action_get_ai_canvas_idea(self, result_data):
        """Extract canvas idea from coworker result."""
        if isinstance(result_data, dict):
            return result_data.get('canvas', {})
        return {}
