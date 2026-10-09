# Management System: ISO 9001 — skal ovanpå den gemensamma ISO-kärnan

Denna modul är ett **tunt skal** ovanpå `mgmtsystem_iso_base`. Den lägger bara
till det som är unikt för ISO 9001:

- **Processmodellen** (`iso9001.process`) — processägare, in-/utdata, resurser,
  KPI:er och koppling till ISO 9001-klausuler. OCA:s `mgmtsystem.system` är
  bara namn + företag och är ingen processmodell, så denna är genuint unik.
- **Klausuldata 4–10** — men posterna ligger i kärnans `mgmtsystem.iso.clause`,
  kopplade till ISO 9001 i standardregistret.
- **Dashboard** — en pivot över kärnans gap-rader, filtrerad till ISO 9001.

## Vad som INTE ligger här längre

| Begrepp | Var det bor nu |
|---|---|
| Klausuler | `mgmtsystem_iso_base` (`mgmtsystem.iso.clause`) |
| Gap-analys | `mgmtsystem_iso_base` (`mgmtsystem.iso.gap` / `.gap.line`) |
| Kvalitetspolicy | `mgmtsystem_manual` / `document_page` |
| Kvalitetsmål med KPI:er | `mgmtsystem_objective` (`mgmtsystem.objective` + `.indicator`) |

## Migrering från äldre version

Vid uppgradering från en version före `18.0.1.1.0` flyttas befintliga poster
från `iso9001.clause`, `iso9001.gap` och `iso9001.gap.line` till kärnans
modeller. Migreringen:

- körs som `post-migrate` för `18.0.1.1.0`,
- är **idempotent** — att köra den två gånger skapar inga dubbletter,
- är **säker** när de gamla tabellerna inte finns (färsk installation),
- **droppar inte** de gamla tabellerna.

### Rollback

Eftersom de gamla tabellerna behålls orörda kan en återställning göras:

1. Avinstallera `mgmtsystem_9001` (och vid behov `mgmtsystem_iso_base`).
2. Installera den tidigare versionen av `mgmtsystem_9001` igen — de gamla
   tabellerna `iso9001_clause`, `iso9001_gap` och `iso9001_gap_line` finns
   kvar med sina ursprungliga rader.
3. Verifiera att klausuler och gap-analyser syns som förut.

⚠ Migreringen skriver **till** kärnan men raderar aldrig från de gamla
tabellerna. En rollback förlorar därför inte data.
