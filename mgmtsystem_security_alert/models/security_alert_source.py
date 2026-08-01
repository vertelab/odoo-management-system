# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import re

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SecurityAlertSource(models.Model):
    _name = "security.alert.source"
    _description = "Security Alert Source"
    _order = "name"

    name = fields.Char(required=True)
    source_type = fields.Selection(
        [
            ("cert_se", "CERT-SE (Atom Feed)"),
            ("ncsc", "NCSC (Web Scraping)"),
            ("nvd_cve", "NVD CVE (API v2.0)"),
            ("ubuntu_usn", "Ubuntu USN (REST API)"),
            ("zabbix", "Zabbix"),
        ],
        string="Source Type",
        required=True,
    )
    url = fields.Char(string="URL", required=True)
    api_key = fields.Char(
        string="API Key",
        help="API key for NVD. Free registration at https://nvd.nist.gov/developers/request-an-api-key",
    )
    active = fields.Boolean(default=True)
    last_fetch = fields.Datetime(string="Last Fetch", readonly=True)
    fetch_interval = fields.Selection(
        [
            ("hourly", "Every Hour"),
            ("daily", "Daily"),
        ],
        string="Fetch Interval",
        default="hourly",
    )
    alert_count = fields.Integer(
        string="Total Alerts",
        compute="_compute_alert_count",
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
    )

    def _compute_alert_count(self):
        for source in self:
            source.alert_count = self.env["security.alert"].search_count(
                [("source_id", "=", source.id)]
            )

    def action_fetch_now(self):
        """Manual fetch trigger."""
        self.ensure_one()
        return self.fetch_alerts()

    def fetch_alerts(self):
        """Main fetch method — called by cron or manually."""
        self.ensure_one()
        if self.source_type == "cert_se":
            return self._fetch_cert_se()
        elif self.source_type == "ncsc":
            return self._fetch_ncsc()
        elif self.source_type == "nvd_cve":
            return self._fetch_nvd_cve()
        elif self.source_type == "ubuntu_usn":
            return self._fetch_ubuntu_usn()
        return False

    def _fetch_cert_se(self):
        """Fetch CERT-SE Atom feed."""
        try:
            import feedparser
        except ImportError:
            _logger.error("feedparser not installed. Run: pip install feedparser")
            return False

        feed = feedparser.parse(self.url)
        created = 0
        for entry in feed.entries:
            if not self._alert_exists(entry.link):
                self.env["security.alert"].create({
                    "name": entry.title,
                    "source_id": self.id,
                    "source_ref": entry.link,
                    "description": entry.get("summary", ""),
                    "published_date": entry.get("published", ""),
                    "severity": "info",
                    "state": "new",
                })
                created += 1
        self.write({"last_fetch": fields.Datetime.now()})
        _logger.info("CERT-SE: Fetched %d new alerts", created)
        return True

    def _fetch_ncsc(self):
        """Fetch NCSC current articles via web scraping."""
        try:
            from bs4 import BeautifulSoup
            import requests as req_lib
        except ImportError:
            _logger.error("beautifulsoup4/requests not installed")
            return False

        try:
            resp = req_lib.get(self.url, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            _logger.error("NCSC fetch failed: %s", e)
            return False

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("article")[:20]
        created = 0
        for article in articles:
            title_elem = article.select_one("h2, h3, a")
            link_elem = article.select_one("a[href]")
            title = title_elem.get_text(strip=True) if title_elem else "NCSC Article"
            link = link_elem.get("href", "") if link_elem else ""
            if link and not link.startswith("http"):
                link = "https://www.ncsc.se" + link
            if not self._alert_exists(link):
                self.env["security.alert"].create({
                    "name": title,
                    "source_id": self.id,
                    "source_ref": link,
                    "published_date": fields.Date.today(),
                    "severity": "info",
                    "state": "new",
                })
                created += 1
        self.write({"last_fetch": fields.Datetime.now()})
        _logger.info("NCSC: Fetched %d new articles", created)
        return True

    def _fetch_nvd_cve(self):
        """Fetch CVEs from NVD API v2.0."""
        try:
            import requests as req_lib
        except ImportError:
            _logger.error("requests not installed")
            return False

        yesterday = fields.Date.today().strftime("%Y-%m-%d")
        today = fields.Date.today().strftime("%Y-%m-%d")
        params = {
            "pubStartDate": f"{yesterday}T00:00:00.000",
            "pubEndDate": f"{today}T23:59:59.999",
            "resultsPerPage": 100,
        }
        headers = {}
        if self.api_key:
            headers["apiKey"] = self.api_key

        try:
            resp = req_lib.get(self.url, params=params, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            _logger.error("NVD fetch failed: %s", e)
            return False

        created = 0
        for vuln in data.get("vulnerabilities", []):
            cve = vuln.get("cve", {})
            cve_id = cve.get("id", "")
            if not cve_id or self._alert_exists(cve_id):
                continue

            desc = cve.get("descriptions", [{}])
            description = desc[0].get("value", "") if desc else ""

            metrics = cve.get("metrics", {})
            cvss_v31 = metrics.get("cvssMetricV31", [{}])
            cvss_score = cvss_v31[0].get("cvssData", {}).get("baseScore", 0.0) if cvss_v31 else 0.0
            severity = self._cvss_to_severity(cvss_score)

            affected = []
            for node in cve.get("configurations", []):
                for cpe in node.get("nodes", []):
                    for match in cpe.get("cpeMatch", []):
                        criteria = match.get("criteria", "")
                        if criteria:
                            affected.append(criteria)
            affected_str = "\n".join(affected) if affected else ""

            self.env["security.alert"].create({
                "name": cve_id,
                "source_id": self.id,
                "source_ref": cve_id,
                "description": description,
                "cvss_score": cvss_score,
                "severity": severity,
                "affected_products": affected_str,
                "published_date": cve.get("published", ""),
                "state": "new",
            })
            created += 1

        self.write({"last_fetch": fields.Datetime.now()})
        _logger.info("NVD: Fetched %d new CVEs", created)
        return True

    def _fetch_ubuntu_usn(self):
        """Fetch Ubuntu Security Notices."""
        try:
            import requests as req_lib
        except ImportError:
            _logger.error("requests not installed")
            return False

        try:
            resp = req_lib.get(self.url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            _logger.error("Ubuntu USN fetch failed: %s", e)
            return False

        notices = data.get("notices", [])[:20]
        created = 0
        for notice in notices:
            usn_id = notice.get("id", "")
            if not usn_id or self._alert_exists(usn_id):
                continue

            cve_list = notice.get("cves", [])
            cve_str = ", ".join(cve_list) if cve_list else ""
            description = f"{notice.get('title', '')}\n\n{notice.get('description', '')}\n\nCVEs: {cve_str}"

            self.env["security.alert"].create({
                "name": f"{usn_id}: {notice.get('title', '')}",
                "source_id": self.id,
                "source_ref": usn_id,
                "description": description,
                "severity": "medium",
                "affected_products": ", ".join(cve_list) if cve_list else "",
                "published_date": notice.get("published", ""),
                "state": "new",
            })
            created += 1

        self.write({"last_fetch": fields.Datetime.now()})
        _logger.info("Ubuntu USN: Fetched %d new notices", created)
        return True

    def _alert_exists(self, source_ref):
        """Check if alert already exists by source_ref."""
        return self.env["security.alert"].search_count(
            [("source_id", "=", self.id), ("source_ref", "=", source_ref)]
        ) > 0

    @staticmethod
    def _cvss_to_severity(score):
        if score >= 9.0:
            return "critical"
        elif score >= 7.0:
            return "high"
        elif score >= 4.0:
            return "medium"
        elif score >= 0.1:
            return "low"
        return "info"

    def fetch_hourly_sources(self):
        """Cron: fetch all hourly sources."""
        for source in self.search([("active", "=", True), ("fetch_interval", "=", "hourly")]):
            try:
                source.fetch_alerts()
            except Exception as e:
                _logger.error("Hourly fetch failed for %s: %s", source.name, e)

    def fetch_daily_sources(self):
        """Cron: fetch all daily sources."""
        for source in self.search([("active", "=", True), ("fetch_interval", "=", "daily")]):
            try:
                source.fetch_alerts()
            except Exception as e:
                _logger.error("Daily fetch failed for %s: %s", source.name, e)
