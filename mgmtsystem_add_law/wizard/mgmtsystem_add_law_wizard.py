from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import requests

from bs4 import BeautifulSoup

class MgmtsystemAddLawWizard(models.TransientModel):
    _name = 'mgmtsystem.add.law.wizard'
    _description = 'Makes it possible to add laws from the website lagen.nu to the Management System Law module.'

    law_designation = fields.Char(required=True)

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
                rss_organ = contents.find("dd")
                rss_typ = "sfs" if "sfs" in contents.findAll("dd")[2].text.lower() else False
                rss_datum = contents.findAll("dd")[1].text
                rss_publicerad = contents.findAll("dd")[6].text
                rss_systemdatum = contents.findAll("dd")[6].text
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

            raise ValidationError("Lagen/Förordningen värkar inte exsitera")

        raise UserError("Lagen/Förordningen finns readan")
      
    def create_record(self,record):

        self.env["document.law"].create(record)


