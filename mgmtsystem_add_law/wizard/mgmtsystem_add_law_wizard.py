from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import requests
import logging

from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)

class MgmtsystemAddLawWizard(models.TransientModel):
    _name = 'mgmtsystem.add.law.wizard'
    _description = 'Makes it possible to add laws from the website lagen.nu to the Management System Law module.'

    law_designation = fields.Char(required=True)
    law_link = fields.Char(default="https://lagen.nu/", readonly=True)

    def add_law(self):

        law_id = self.env["document.law"].search([("rss_beteckning", '=', self.law_designation)])

        if not law_id:

            response = requests.get(f"https://lagen.nu/{self.law_designation}")

            self.law_designation = ""

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                contents = soup.find("article")
               
                rss_titel = contents.find("h1").text
                rss_beteckning = rss_titel.split("(")[1].split(")")[0]
                rss_rm = rss_beteckning.split(":")[0]
                rss_dok_id = f"sfs-{rss_beteckning.replace(':','-')}"
                rss_organ = self.find_dd(soup,"Departement")
                rss_typ = "sfs" if "sfs" in self.find_dd(soup,"Ändring införd").lower() else False
                rss_datum = self.find_dd(soup,"Utfärdad")
                rss_publicerad = self.find_dd(soup,"Senast hämtad")
                rss_systemdatum = self.find_dd(soup,"Senast hämtad")
                rss_text = "\n\n".join(map((lambda p: p.text),contents.findAll("p")))
                rss_html = contents   
              
                record = {
                    "rss_titel": rss_titel,
                    "rss_beteckning": rss_beteckning,
                    "rss_rm": rss_rm,
                    "rss_dok_id": rss_dok_id,
                    "rss_organ": rss_organ,
                    "rss_typ": rss_typ,
                    "rss_datum": rss_datum,
                    "rss_publicerad": rss_publicerad,
                    "rss_systemdatum": rss_systemdatum,
                    "rss_text": rss_text,
                    "rss_html": rss_html,
                }

                self.create_record(record)

                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }

            raise ValidationError(_("Lagen/Förordningen värkar inte exsistera"))
        raise UserError(_("Lagen/Förordningen finns readan"))
      
    def find_dd(self,soup,dt_to_find):
        dl_contents = soup.find("dl",attrs={"id": "refs-dokument"})
        dd_list = dl_contents.findAll("dd")
        dt_list = dl_contents.findAll("dt")
        for dt, dd in zip(dt_list,dd_list):
            if dt.text == dt_to_find:
                return dd.text
        return False

    def create_record(self,record):
        try:
            self.env["document.law"].create(record)
        except Exception as e:
            raise UserError(_(e))
        
