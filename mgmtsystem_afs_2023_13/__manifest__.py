# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: AFS 2023:13 — Risker vid vissa arbeten',
    'version': '18.0.1.0.0',
    'summary': 'Kopplar AFS 2023:13 till ISO 45001-klausuler och arbetsmiljöprocesser',
    'category': 'Management',
    'description': """
        AFS 2023:13 är inte ett ledningssystem — det är en föreskrift.
        Den hör därför inte hemma som egen standardmodul, utan som en
        lagpaketering som kopplar föreskriften till de ISO 45001-klausuler
        den ger innehåll åt.

        Föreskriften ersätter AFS 2006:6 (hissar) och AFS 2006:4
        (användning av arbetsutrustning) med flera. Den är konsoliderad
        till och med AFS 2025:8.

        Kapitel som berör hissverksamhet:
        - 5 kap. Byggnads- och anläggningsarbete
        - 8 kap. 18 § Hissvakt — krävs för varje hiss som manövreras
          från samma manöverplats och på varje däck som betjänas
        - 9 kap. Arbete på höjd

        Klausulmappning (data/afs_2023_13_clause_map.xml) kopplar varje
        kapitel till de ISO 45001-klausuler den svarar mot. Det gör att
        en gap-analys kan visa inte bara "vi uppfyller 6.1.3 dåligt",
        utan "vi uppfyller 6.1.3 dåligt, och det beror på att vi inte
        har rutin för hissvakt enligt 8 kap. 18 §".
    """,
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_afs_2023_13',
    'license': 'AGPL-3',
    'depends': [
        'mgmtsystem_45001',
        'law_packages',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/afs_2023_13_clause_map.xml',
        'views/iso45001_ohs_process_views.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
