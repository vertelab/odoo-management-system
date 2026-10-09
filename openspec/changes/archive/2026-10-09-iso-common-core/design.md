## Context

Se `proposal.md` — Why, för motivering. Det som styr designen är det faktiska
läget i repot:

- Sex moduler definierar i dag var sin klausulmodell och var sin gap-modell.
  Klausulmodellerna är fält-för-fält identiska (`name`, `clause_number`,
  `display_name`, `parent_id`, `child_ids`, `sequence`, `company_id`, samma
  `_sql_constraints`, samma `_compute_display_name`).
- Gap-modellerna är nästan identiska (`name`, `date`, `assessed_by`, `state`,
  `line_ids`) men skiljer sig i **vad raderna avser**: 9001/14001/22000/42001
  genererar rader per klausul, medan 27001 genererar rader per
  `mgmtsystem.security.control` (Annex A) och `sam` har egen `iso_clause`.
- `mgmtsystem_27001` och `mgmtsystem_22000` bygger redan på OCA:s
  `mgmtsystem.*` och utökar dem med `_inherit` (samma tabell, extra fält).
  `mgmtsystem_9001`, `_14001` och `_42001` är fristående öar
  (`depends: ['base', 'mail']`) trots att deras beskrivning påstår annat.
- OCA:s `mgmtsystem.objective` + `mgmtsystem.indicator` ger redan mål med
  KPI:er, målvärden och mätvärden — precis vad `iso*001.objective` försöker
  vara. `mgmtsystem_manual` / `document_page` ger manual/policy-dokument.
- OCA-modulerna ligger i ett separat repo (`odooext-OCA-management-system`)
  och är redan installerade/beroenden i 27001 och 22000.

## Goals / Non-Goals

**Goals:**

- En enda klausulmodell och en enda gap-modell för alla ISO-standarder, med
  OCA:s `mgmtsystem.`-prefix.
- Standarder som data (`mgmtsystem.iso.standard`) i stället för som modellnamn.
- Ett skal-mönster som 27001/22000 redan följer, så att de tre fristående
  modulerna (9001/14001/42001) kan ansluta utan att kärnan specialiseras.
- Migrering som bevarar befintlig data utan dubbletter.

**Non-Goals:**

- Att lösa kopplingen till `quality_ce` (kontrollpunkt ↔ klausul, underkänd
  kontroll ↔ nonconformity). Egen uppföljande change.
- Att bygga om `mgmtsystem.nonconformity`, `mgmtsystem.audit` eller
  `mgmtsystem.review` — de behålls som de är och används via `_inherit`.
- Att införa en generisk "vilken standard som helst"-motor. Standardregistret
  är data, men standard-specifika modeller (SoA, HACCP, processer) ligger kvar
  i skal-modulerna.
- Att migrera `mgmtsystem_sam` i denna change (se Migration Plan).

## Decisions

### Beslut 1: Kärnmodul `mgmtsystem_iso_base` med OCA-prefix

Ny modul med modellerna `mgmtsystem.iso.standard`, `mgmtsystem.iso.clause`,
`mgmtsystem.iso.gap`, `mgmtsystem.iso.gap.line`.

**Varför `mgmtsystem.`-prefix:** modellerna hör till samma domän som OCA:s
övriga `mgmtsystem.*`-modeller, och prefixet gör att de sorterar och hittas
tillsammans i modellistan. Det var också det uttryckliga önskemålet.

**Alternativ som övervägdes:**
- `iso.clause` utan standard-prefix — för generiskt, kolliderar med
  standard-specifika moduler och säger inget om hemvist.
- Behålla `iso9001.clause` som "bas" och låta de andra ärva den — gör 9001
  till en oavsiktlig kärna och kopplar samman standarder som inte hör ihop.

### Beslut 2: Standarder som poster, inte som modeller

`mgmtsystem.iso.standard` (namn, beteckning, version, aktiv) och
`mgmtsystem.iso.clause.standard_id` → standard. Klausulnumret är unikt
**per standard**, inte globalt.

**Varför:** klausul 5.2 finns i både 9001 och 27001 med olika innebörd.
Dagens sex modeller löser det genom att vara sex modeller; en modell med
`standard_id` löser samma sak utan kopiering.

**Alternativ:** en `standard`-Selection på klausulen. Förkastat — då kan inte
en kund lägga till en egen standard utan kodändring, och versionen av
standarden (9001:2015 vs 9001:2026) får ingen hemvist.

### Beslut 3: Kärnans gap-rad avser klausul; skal-modulen utökar

`mgmtsystem.iso.gap.line` har `clause_id` (obligatoriskt mot kärnans klausul)
och `maturity_level` (0–5), `finding`, `recommendation`, `status`.

27001:s kontroll-baserade gap löses genom att skal-modulen lägger till en
`control_id` på raden (via `_inherit`) och genererar rader därifrån — kärnan
förblir klausul-orienterad.

**Varför:** kärnan ska bära det som är gemensamt för alla (mognad per
klausul). Kontroll-kopplingen är en 27001-avvikelse och hör i skal-modulen,
i linje med "avvikelser hanteras i skal-modulen".

**Alternativ:** låta kärnans rad peka på en generisk "bedömningsenhet"
(polymorft). Förkastat — det gör kärnan svårare att förstå och kräver att
varje skal-modul registrerar sin enhetstyp, utan att vinna något för de
standarder som bara använder klausuler.

### Beslut 4: Skal-modulen använder `_inherit`, inte egna modeller

Skal-modulen gör `_inherit = "mgmtsystem.iso.clause"` för att lägga
standard-specifika fält (t.ex. koppling till 9001:s processer), precis som
27001 i dag gör mot `mgmtsystem.action` och `mgmtsystem.security.control`.

**Varför:** bevarar en tabell per begrepp, gör att kärnans förbättringar slår
igenom överallt, och följer det mönster som redan är etablerat i repot.

**Alternativ:** `_inherits` (delegation, egen tabell + FK). Förkastat — det
skulle ge en egen tabell per standard igen, vilket är precis dupliceringen vi
vill bort ifrån, och komplicerar migreringen.

### Beslut 5: Policy och mål rivs, OCA används

`iso*001.policy` tas bort → `mgmtsystem_manual` / `document_page`.
`iso*001.objective` tas bort → `mgmtsystem.objective` + `mgmtsystem.indicator`.

**Varför:** OCA:s modeller är rikare (indikatorer med mätvärden över tid,
målvärden, UoM, koppling till `mgmtsystem.system`) och redan beroenden i
27001/22000. Att behålla egna kopior är den duplicering change:n ska bort.

**Alternativ:** behålla `iso*001.objective` och koppla den till
`mgmtsystem.system`. Förkastat — då finns två målmodeller som båda kopplar
till systemet, vilket är samma problem i mindre skala.

### Beslut 6: `iso9001.process` behålls i skal-modulen

OCA:s `mgmtsystem.system` är bara `name` + `company_id` — den är ingen
processmodell. 9001:s processmodell (inputs/outputs/KPI/processägare/
klausulkoppling) har inget OCA-motstycke och är genuint unik för 9001.

**Varför:** "tunt lager" betyder inte "tömt". Det som inte finns någon
annanstans ska ligga kvar, men på rätt plats (skal-modulen) och kopplat till
kärnans klausuler.

## Risks / Trade-offs

- **Migrering kan dubblera data** (gamla + nya rader samtidigt) → migreringen
  körs i `pre_init`/`post_init` med `_table_exists`-kontroll och en
  idempotent mappning per standard; verifieras med antalsräkning före/efter.
- **`sam` använder ISO 45001, inte en av de fem** → `sam.iso_clause` migreras
  till kärnan med standard 45001, men `sam`-modulen i övrigt lämnas orörd i
  denna change (den har egna `sam.policy`, `sam.task_delegation` m.m.).
- **Befintliga installationer med `noupdate="1"`-klausuldata** → klausuldata
  flyttas till kärnans xmlid-rymd; gamla xmlid blir orphan och måste rensas
  eller mappas, annars ligger dubbel klausuldata kvar vid uppgradering.
- **`mgmtsystem_9001` är `application: True`** → att göra den beroende av
  kärnan ändrar installationsordningen; kärnan måste vara installerbar fristående
  först.
- **sv.po** → modellnamn och fältetiketter ändras; översättningarna måste
  regenereras via `checkmodule -e` (handskrivna utan `#: model:`-referenser
  appliceras aldrig).
- **Beroende till OCA-repot** → `mgmtsystem_iso_base` kräver att
  `odooext-OCA-management-system` finns i addons-path; det är redan fallet för
  27001/22000, men måste dokumenteras i `requirements.repo`.

## Migration Plan

1. **Fas 1 — kärnan på plats.** Skapa `mgmtsystem_iso_base`. Ingen befintlig
   modul ändras. Kärnan kan installeras fristående och verifieras.
2. **Fas 2 — 9001 migreras** (denna change, huvudspåret). `mgmtsystem_9001`
   byggs om till skal: beroende till kärnan, klausuldata flyttas, policy/mål
   rivs, processmodellen behålls. Migreringsskript flyttar befintliga
   `iso9001.*`-poster till kärnan.
3. **Fas 3 — 14001 och 42001** (uppföljande changes, samma mönster).
4. **Fas 4 — 27001, 22000 och sam** (uppföljande changes; 27001/22000 har
   redan OCA-beroenden och behöver bara byta klausul-/gap-modell mot kärnan,
   sam får sin 45001-standard i kärnan).

**Rollback:** varje fas är en egen moduluppgradering. Kärnan kan avinstalleras
först efter att alla skal-moduler återställts till sina egna modeller; därför
behålls de gamla tabellerna orörda (ingen `DROP`) i denna change, så att en
återställning är möjlig.

## Open Questions

- Ska `mgmtsystem.iso.standard` bära en `revision`/utgåva (9001:2015 vs
  9001:2026) som separat fält, eller räcker `version` som fritext? Kan avgöras
  när klausuldatan för 9001:2026 läggs in — påverkar inte modellens form.
- Ska kärnan ha en dashboard/översikt över flera standarder samtidigt, eller
  räcker det att varje skal-modul har sin egen? Kan läggas till utan att
  ändra modellerna.
