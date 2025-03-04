import logging
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class AIQuest(models.Model):
    _inherit = 'ai.quest'

    ai_type = fields.Selection(selection_add=[('law_summary', 'Law Summary')],ondelete={'law_summary': 'cascade'})
    
    def generate_summary(self,text):
        # Initialize the language model
        llm = self.get_llm()
        
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(text)
        
        # Create Document objects
        docs = [Document(page_content=t) for t in texts]
        
        # Load the summarization chain
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        
        # Generate the summary
        summary = chain.run(docs)
        
        return summary
