from odoo import models, fields, api, _

import logging, os
from odoo.exceptions import ValidationError

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

_logger = logging.getLogger(__name__)

class AIAgent(models.Model):
    _inherit = 'ai.agent'

    ai_type = fields.Selection(selection_add=[('law_relevancy', 'Law Relevancy')],ondelete={'law_relevancy': 'cascade'})
