# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Quality: Management System Nonconformity Bridge',
    'version': '18.0.1.0.0',
    'summary': 'Brygga mellan kvalitetskontroller och ledningssystemets avvikelser',
    'category': 'Manufacturing/Quality',
    'description': """
        Brygga mellan kvalitetskontroller och ledningssystemets
        avvikelsehantering.

        Implementerar:
        - Kontrollpunkter kopplas till de ISO-klausuler som kräver dem
        - En underkänd kontroll kan bli en nonconformity i ledningssystemet
          med ett klick — utan att registreras en andra gång manuellt
        - Bakåtlänk åt båda hållen: nonconformity -> kontroll/alert och
          kontroll/alert -> nonconformity
        - Idempotens: högst en nonconformity per kontroll eller alert

        Följer det etablerade bryggmönstret i repot
        (fire_protection_fsm_bridge, saltstack_managementsystem):
        en ren bryggmodul med smalt beroende, _inherit och en
        action_create_*-metod, så att kvalitet utan ISO förblir möjligt.

        quality.alert och mgmtsystem.nonconformity förblir två modeller med
        olika hemvist (golv respektive ledningssystem). Bryggan förenar dem,
        den slår inte ihop dem.
    """,
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-management-system/quality_mgmtsystem_nonconformity',
    'license': 'AGPL-3',
    'depends': [
        # quality_control_ce owns the quality.check / quality.alert form views
        # that this bridge extends; it in turn depends on quality_ce.
        'quality_control_ce',
        'mgmtsystem_nonconformity',
        'mgmtsystem_iso_base',
        # hr is an Odoo core module. Needed to derive the nonconformity's
        # manager from the responsible user's employee record (design
        # Beslut 6). Nothing in the mgmtsystem chain pulls it in.
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/nonconformity_origin_data.xml',
        'views/quality_check_views.xml',
        'views/quality_alert_views.xml',
        'views/quality_point_views.xml',
        'views/mgmtsystem_nonconformity_views.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
