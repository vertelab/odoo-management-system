## 1. Kärnmodulen `mgmtsystem_iso_base` — stomme

- [x] 1.1 Skapa modulkatalogen `mgmtsystem_iso_base/` med `__init__.py`,
      `__manifest__.py` (depends: `mgmtsystem`, `mgmtsystem_objective`,
      `mgmtsystem_manual`) och tomma `models/`, `views/`, `security/`, `data/`,
      `i18n/`. Verifiera att `python3 -c "import ast; ast.parse(open('mgmtsystem_iso_base/__manifest__.py').read())"` lyckas och att modulen syns i Odoos applista.
- [x] 1.2 Skapa `security/security.xml` med modulkategori och grupper
      (`group_iso_base_user`, `group_iso_base_manager`) samt `ir.model.access.csv`
      för kärnans fyra modeller. Verifiera att grupperna syns under
      Inställningar → Användare och att access-radfilen laddar utan fel.

## 2. Kärnmodulen — datamodell

- [x] 2.1 Implementera `mgmtsystem.iso.standard` (namn, beteckning, version,
      aktiv) med unikhetsvillkor på beteckning. Verifiera med ett test som
      skapar två standarder med samma beteckning och förväntar valideringsfel.
- [x] 2.2 Implementera `mgmtsystem.iso.clause` (`name`, `clause_number`,
      `standard_id`, `parent_id`, `child_ids`, `sequence`, `description`,
      `company_id`, `display_name`) med unikhet på (`clause_number`,
      `standard_id`). Verifiera med test: samma klausulnummer i två standarder
      tillåts, dubbelt inom samma standard avvisas.
- [x] 2.3 Implementera `mgmtsystem.iso.gap` (`name`, `date`, `assessed_by`,
      `state`, `standard_id`, `company_id`, `line_ids`) med övergångarna
      `action_start`/`action_done`/`action_draft`. Verifiera med test att en
      analys utan standard avvisas och att statusflödet följer utkast →
      pågående → klar.
- [x] 2.4 Implementera `mgmtsystem.iso.gap.line` (`gap_id`, `clause_id`,
      `maturity_level` 0–5, `finding`, `recommendation`, `status`,
      `company_id` related). Verifiera med test att en ny rad har
      mognadsnivå 0 och att fynd/rekommendation sparas.
- [x] 2.5 Lägg `ir.rule` för företagsavskärmning på alla fyra modellerna.
      Verifiera med test som listar poster från två företag och förväntar att
      bara det egna företagets poster syns.

## 3. Kärnmodulen — vyer och data

- [x] 3.1 Skapa list-, form- och sökvyer för klausul, standard, gap och
      gap-rad, samt meny. Verifiera att vyerna laddar utan Odoo-varningar och
      att klausulträdet visar över-/underklausuler i rätt ordning.
- [x] 3.2 Lägg standardregistret som data (`data/iso_standard_data.xml`) med
      posterna 9001, 14001, 22000, 27001, 42001 och 45001. Verifiera att
      posterna finns efter installation och att inaktiva standarder inte
      erbjuds i val.
- [x] 3.3 Skapa `i18n/sv.po` för kärnans modellnamn och fältetiketter.
      Verifiera att filen genereras via `checkmodule -e` (inte handskriven)
      och att svenska strängar visas i gränssnittet.

## 4. `mgmtsystem_9001` blir skal-modul

- [x] 4.1 Ändra `mgmtsystem_9001/__manifest__.py`: sätt `depends` till
      `mgmtsystem_iso_base` (plus de OCA-moduler som faktiskt används).
      Verifiera att modulen kan installeras efter kärnan.
- [x] 4.2 Ta bort `models/iso9001_clause.py`, `iso9001_gap.py` och
      `iso9001_gap_line.py`; uppdatera `models/__init__.py`. Verifiera att
      ingen 9001-specifik klausul-/gap-modell finns kvar i modellistan.
- [x] 4.3 Ta bort `models/iso9001_policy.py` och `models/iso9001_objective.py`.
      Verifiera att policyn hanteras i manual-/dokumentmodulen och mål i
      målmodulen, och att inga referenser till de borttagna modellerna finns
      kvar i vyer, säkerhet eller data.
- [x] 4.4 Behåll `models/iso9001_process.py` men byt klausulkopplingen från
      `iso9001.clause` till `mgmtsystem.iso.clause`. Verifiera att en process
      kan kopplas till en ISO 9001-klausul och att kopplingen visas.
- [x] 4.5 Flytta klausuldatan (4–10) till kärnans klausulmodell med
      `standard_id` = ISO 9001 och nya xmlid i kärnans namnrymd. Verifiera att
      klausulerna 4–10 finns kopplade till ISO 9001 och att ingen dubbel
      klausuldata ligger kvar.
- [x] 4.6 Uppdatera 9001:s vyer, säkerhet och meny så att de pekar på kärnans
      modeller. Verifiera att menyn fungerar och att inga `iso9001.clause`-,
      `iso9001.gap`-, `iso9001.policy`- eller `iso9001.objective`-referenser
      återstår (`grep -rn "iso9001\.\(clause\|gap\|policy\|objective\)"`).

## 5. Migrering av befintlig data

- [x] 5.1 Skriv migreringsskript som flyttar poster från `iso9001.clause`,
      `iso9001.gap` och `iso9001.gap.line` till kärnans modeller med ISO 9001
      som standard, skyddat av `_table_exists` och idempotent. Verifiera med
      antalsräkning före/efter att varje klausul och analys finns på ett enda
      ställe och att mognadsnivåer är bevarade.
- [x] 5.2 Verifiera att migreringen inte skapar dubbletter vid en andra
      körning (kör uppgraderingen två gånger i samma databas).
- [x] 5.3 Behåll de gamla tabellerna orörda (ingen `DROP`) så att rollback är
      möjlig, och dokumentera rollback-vägen i modulens README.

## 6. Integration och verifiering

- [x] 6.1 Kör `checkmodule -t` för `mgmtsystem_iso_base` och `mgmtsystem_9001`
      på en testdatabas och verifiera att alla tester passerar.
- [x] 6.2 Verifiera i en riktig Odoo 18-miljö att en gap-analys för ISO 9001
      kan skapas, fyllas med mognadsnivåer och slutföras, och att resultatet
      läses från kärnans modeller.
- [x] 6.3 Uppdatera `requirements.repo`/dokumentation så att beroendet till
      `odooext-OCA-management-system` framgår, och verifiera att en installation
      från tom databas drar in rätt moduler.
