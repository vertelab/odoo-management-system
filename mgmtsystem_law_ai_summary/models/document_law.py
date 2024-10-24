from odoo import models, fields, api, _

import logging, os
from odoo.exceptions import ValidationError

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

_logger = logging.getLogger(__name__)

class DocumentLaw(models.Model):
    _description = 'scaffold_test.scaffold_test'
    _inherit = 'document.law'

    ai_policy = fields.Text()

    def ai_templet_prompt(self):

        system_prompt =\
        _("""
        {context}

        ---

        The context above is a description and summary of a company. And below is a law. Give a summary of the law and whether it is applicable to this company and its business.

        ---
        
        {law}

        ---
        Answer: 
        """).strip()

        return PromptTemplate(template=system_prompt,input_variables=["context","law"])

    def create_ai_summary(self):
        
        for rec in self:
            
            company_id = rec.company_id

            if company_id.ai_company_context:

                ai_message = self.ai_templet_prompt().invoke({"context": company_id.ai_company_context, "law": rec.rss_text})
                ai_answer = self.get_llm(company_id=company_id).invoke(ai_message)
                
                parser = StrOutputParser()

                _logger.error(f"{ai_answer=}")

                rec.ai_policy = parser.invoke(ai_answer)

                return

            raise ValidationError(_("No company context for ai"))

    def get_llm(self,company_id):

        if not company_id.ai_api_key:
            raise ValidationError(_("Pleass add a api key for your llm."))

        if company_id.ai_model == "chatgpt":

            os.environ["OPENAI_API_KEY"] = company_id.ai_api_key
            return ChatOpenAI(model="gpt-4o")
            
        elif company_id.ai_model == "mistral":
            
            os.environ["MISTRAL_API_KEY"] = company_id.ai_api_key
            return ChatMistralAI(model="mistral-large-latest")
            
        else:
            raise ValidationError(_("Pleass selecte a llm on your company."))


