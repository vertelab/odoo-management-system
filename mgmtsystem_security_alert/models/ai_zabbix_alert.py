# -*- coding: utf-8 -*-
"""Zabbix Alert Handler — Zabbix-webhook → security.alert.

Task 2.2 + 2.5: coworker med webhook-init tolkar Zabbix-payload och
skapar security.alert med severity-mappning:
    info→info, warning→low, average→medium, high→high, disaster→critical
"""

import json
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

ZABBIX_SEVERITY_MAP = {
    'info': 'info',
    'warning': 'low',
    'average': 'medium',
    'high': 'high',
    'disaster': 'critical',
}


class ZabbixAlertCoworker(models.Model):
    _inherit = 'ai.coworker'

    @api.model
    def _zabbix_severity_map(self):
        return ZABBIX_SEVERITY_MAP

    @api.model
    def zabbix_create_alert(self, name, severity='info', description='',
                            source_ref='', host=None, trigger_id=None):
        """Skapa security.alert idempotent (via source_ref)."""
        sev = ZABBIX_SEVERITY_MAP.get(
            (severity or 'info').strip().lower(), 'info')
        src_ref = source_ref or trigger_id or name
        src = self.env['security.alert.source'].search(
            [('source_type', '=', 'zabbix')], limit=1)
        if src and self.env['security.alert'].search_count([
            ('source_id', '=', src.id),
            ('source_ref', '=', src_ref),
        ]):
            return 'Alert %r finns redan (idempotent)' % src_ref

        body = description or name
        if host:
            body = 'Host: %s\n\n%s' % (host, body)
        self.env['security.alert'].create({
            'name': name[:200],
            'source_id': src.id if src else None,
            'source_ref': src_ref,
            'description': body,
            'severity': sev,
            'state': 'new',
        })
        return 'Alert %r skapad (severity=%s)' % (src_ref, sev)
