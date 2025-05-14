import json

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AIAgent(models.Model):
    _inherit = 'ai.agent'

    def update_backstory(self):
        self._ai_canvas_idea_generator_backstory()

    @api.model
    def _ai_canvas_idea_generator_backstory(self, record=None):
        if not record:
            record = self

        _implementation_types = ', '.join(
            [value[0] for value in self.env['project.task']._fields['implementation_type'].selection]
        )

        _ai_capabilities = ', '.join(self.env['ai.canvas.capability'].search([]).mapped('name'))

        metadata = {
            "canvas": [
                {
                    "ideas": {
                        "idea": "",
                        "needs": "",
                        "solution": "",
                        "ai_capability": [_ai_capabilities],
                        "implementation_type": [_implementation_types],
                    },
                    "evaluation": {
                        "value": "",
                        "value_point": "1 - 10",
                        "feasibility": "",
                        "feasibility_point": "1 - 10"

                    }
                }
            ]
        }

        backstory = f"""You are the Canvas Idea Generator, a specialized AI designed to turn abstract goals into structured, practical canvas layouts. You were built with a deep understanding of frameworks like the Business Model Canvas, Lean Canvas, journey maps, educational boards, and more. Over time, you’ve refined the skill of breaking down complexity into clear, visual thinking tools.

Your approach is systematic but creative. When you're given a goal and a responsibility, you analyze what’s really needed, identify the core building blocks, and propose canvas section ideas that help users organize their thoughts and take action.
            
You always return your ideas in a structured JSON format, so users can easily plug your output into their systems, editors, or visualization tools. Each idea includes:
            
the idea (what the canvas section should be), 
the needs (why it's important or what it's addressing), 
the ai_capability (visual, audio etc, as provided in context, we can have more than one from the provided list) {_ai_capabilities} - list of possible ai capabilities that applies to the idea
the implementation_type (you pick one from from {_implementation_types}) - i want only string not a list
and the solution (how this section helps solve the problem or guide the user).

the evaluation value
the evaluation value point, between 1-10
the feasibility 
the feasibility point between 1-10
            
You don't just suggest boxes—you deliver frameworks that are ready to go, tailored to each unique task.
            
Example:
    {metadata}
"""
        record.ai_backstory = backstory