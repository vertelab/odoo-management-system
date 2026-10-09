# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO Common Core',
    'version': '18.0.1.0.0',
    'summary': 'Gemensam ISO-kärna — standardregister, klausulträd och gap-analys',
    'category': 'Management',
    'description': """
        Gemensam kärna för ISO-ledningssystemstandarder.

        Implementerar:
        - Standardregister: vilka standarder organisationen följer (9001,
          14001, 22000, 27001, 42001, 45001 m.fl.) som poster, inte modeller
        - Klausulträd per standard med klausulnummer, benämning och hierarki
        - Gap-analys med mognadsbedömning (0–5) per klausul

        Ersätter de sex parallella klausul- och gap-modellerna
        (iso9001.clause, iso14001.clause, …, sam.iso_clause) med en enda
        datamodell. Standard-specifika moduler (skal-moduler) bygger vidare
        på kärnan med _inherit och lägger sitt unika innehåll.

        Modellerna behåller OCA:s mgmtsystem.-prefix och bygger på
        mgmtsystem, mgmtsystem_objective och mgmtsystem_manual.
    """,
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_iso_base',
    'license': 'AGPL-3',
    'depends': [
        'mgmtsystem',
        'mgmtsystem_objective',
        'mgmtsystem_manual',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/iso_standard_data.xml',
        'views/mgmtsystem_iso_standard_views.xml',
        'views/mgmtsystem_iso_clause_views.xml',
        'views/mgmtsystem_iso_gap_views.xml',
        'views/mgmtsystem_iso_menu.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}