import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = 'res.company'
    _description = 'scaffold_test.scaffold_test'

    law_rss_url = fields.Char(string="RSS_URL", default="https://data.riksdagen.se/dokumentlista/?doktyp=sfs&dokstat=g%C3%A4llande sfs&del=global&utformat=rss&sort=datum&sortorder=desc")
