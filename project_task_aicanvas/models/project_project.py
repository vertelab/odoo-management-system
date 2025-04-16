import re
import math
import random
import logging
from odoo import api, Command, fields, models, _
from odoo.exceptions import UserError, ValidationError, AccessError

_logger = logging.getLogger(__name__)



class Project(models.Model):
    _inherit = "project.project"

    is_aicanvas = fields.Boolean(string="AI Canvas", default=False, copy=False)

    def _get_ai_canvas_swot_diagram(self):
        for rec in self:
            # Get tasks with value and feasibility points set
            tasks_with_points = rec.task_ids.filtered(lambda task: task.value_point and task.feasibility_point)

            if not tasks_with_points:
                # If no tasks have points set, return the basic chart
                rec.ai_canvas_swot_diagram = """
                    quadrantChart
                        x-axis "SVÅRT" --> "LÄTT"
                        y-axis "LÅG" --> "HÖG"
                        quadrant-1 "IDEALA ANVÄNDNINGSFALL" 
                        quadrant-2 "STOR LÅNGSIKTIG POTENTIAL"
                        quadrant-3 "HÅLL ER BORTA!"
                        quadrant-4 "SNABBA OCH ENKLA VINSTER"
                """
                continue

            # Group tasks by quadrant based on value and feasibility points
            tasks_by_quadrant = {
                'x_high': [],  # Difficult feasibility (Quadrant 1 & 3)
                'x_low': [],  # Easy feasibility (Quadrant 2 & 4)
                'y_high': [],  # High value (Quadrant 1 & 2)
                'y_low': []  # Low value (Quadrant 3 & 4)
            }

            # Define threshold for categorizing points (midpoint of the scale)
            threshold = 5.5  # Assuming scale is 1-10

            for task in tasks_with_points:
                # Convert string points to float
                value = float(task.value_point)
                feasibility = float(task.feasibility_point)

                # Categorize tasks by feasibility (x-axis)
                if feasibility > threshold:
                    tasks_by_quadrant['x_high'].append(task)  # Difficult
                else:
                    tasks_by_quadrant['x_low'].append(task)  # Easy

                # Categorize tasks by value (y-axis)
                if value >= threshold:
                    tasks_by_quadrant['y_high'].append(task)  # High value
                else:
                    tasks_by_quadrant['y_low'].append(task)  # Low value

            # Add coordinates to tasks
            for task in tasks_with_points:
                # Convert value_point from 1-10 scale to 0-1 coordinate scale
                # For y-coordinate (value): higher value → higher coordinate
                y_coord = float(task.value_point) / 10.0

                # For x-coordinate (feasibility): higher feasibility (more difficult) → lower coordinate
                # Converting from 1-10 scale to 0-1 coordinate scale with inversion
                x_coord = 1.0 - (float(task.feasibility_point) / 10.0)

                # Add some randomness to avoid overlapping points
                jitter = 0.03  # Small random adjustment
                x_coord += (random.random() - 0.5) * jitter
                y_coord += (random.random() - 0.5) * jitter

                # Ensure coordinates stay within bounds
                x_coord = max(0.05, min(0.95, x_coord))
                y_coord = max(0.05, min(0.95, y_coord))

                # Assign coordinates directly to the task
                task.ai_canvas_coordinate = f"[{x_coord:.2f}, {y_coord:.2f}]"

            # Create task entries for mermaid diagram
            task_entries = []
            for task in tasks_with_points:
                # Clean task name to avoid special characters that might break the mermaid syntax
                clean_name = re.sub(
                    r'[^\w\s]',
                    '',
                    task.name.replace('ä', 'a').replace('å', 'a').replace('ö', 'o')
                    .replace('Ä', 'A').replace('Å', 'A').replace('Ö', 'O')
                )

                # Add task entry with its coordinate - using the format shown in the example
                task_entries.append(f'{clean_name}: {task.ai_canvas_coordinate}')

            # Create the complete mermaid diagram with correct quadrant positions
            # Based on the image, the correct order is:
            # quadrant-1: STOR LÅNGSIKTIG POTENTIAL (top-left)
            # quadrant-2: IDEALA ANVÄNDNINGSFALL (top-right)
            # quadrant-3: HÅLL ER BORTA! (bottom-left)
            # quadrant-4: SNABBA OCH ENKLA VINSTER (bottom-right)
            quadrant_chart = f"""
                quadrantChart
                    x-axis "SVÅRT" --> "LÄTT"
                    y-axis "LÅG" --> "HÖG"
                    quadrant-1 "IDEALA ANVÄNDNINGSFALL" 
                    quadrant-2 "STOR LÅNGSIKTIG POTENTIAL"
                    quadrant-3 "HÅLL ER BORTA!"
                    quadrant-4 "SNABBA OCH ENKLA VINSTER"
                    {chr(10).join(task_entries)}
            """

            rec.ai_canvas_swot_diagram = quadrant_chart

    ai_canvas_swot_diagram = fields.Text(string='AI Canvas SWOT Diagram', compute=_get_ai_canvas_swot_diagram)