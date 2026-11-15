# odoo-management-system — gren 19.0

> **Denna gren är avsiktligt tom.** Modulerna är INTE portade till Odoo 19.
> Grenen finns så att dev-miljöer (`hansolo19`) kan klona den utan att falla,
> men den påstår ingenting om att koden är portad.

## Baseline

| | |
|---|---|
| Källa | `20.0` |
| Moduler | **22** |
| Grenar i repot | `16.0`, `18.0`, `20.0` |

## Moduler

- `law_packages`
- `mgmtsystem_14001`
- `mgmtsystem_22000`
- `mgmtsystem_27001`
- `mgmtsystem_42001`
- `mgmtsystem_9001`
- `mgmtsystem_action_ref`
- `mgmtsystem_add_law`
- `mgmtsystem_hr_skills`
- `mgmtsystem_law`
- `mgmtsystem_law_ai_chat`
- `mgmtsystem_law_ai_relevancy`
- `mgmtsystem_law_ai_summary`
- `mgmtsystem_lms`
- `mgmtsystem_nonconformity_ai`
- `mgmtsystem_nonconformity_qr`
- `mgmtsystem_onboarding`
- `mgmtsystem_sam`
- `mgmtsystem_security_alert`
- `mgmtsystem_yearwheel`
- `project_task_aicanvas`
- `project_task_aicanvas_hr`

## Blockerare

✅ Inga externa beroenden saknas i Odoo 19-kärnan eller OCA 19.0.

Modulerna kan troligen portas utan att vänta på externa bidrag.

## Nästa steg

Portering sker på `*-pfile`-maskin med versionsagnostisk kod
(`.p.py` / `.p.xml`). Se `/skill:odoo-pfiles`.
