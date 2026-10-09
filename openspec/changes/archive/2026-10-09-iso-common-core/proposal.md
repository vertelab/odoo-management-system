## Why

Sex moduler i repot (`mgmtsystem_9001`, `_14001`, `_22000`, `_27001`, `_42001`,
`_sam`) definierar var sin klausulmodell (`iso9001.clause`, `iso14001.clause`,
…, `sam.iso_clause`) och var sin gap-modell med mognadsbedömning 0–5. Modellerna
är i praktiken identiska — samma fält, samma `_sql_constraints`, samma
`_compute_display_name` — men kopierade per standard. Samtidigt är tre av
modulerna (`_9001`, `_14001`, `_42001`) fristående öar: deras manifest säger
`depends: ['base', 'mail']` trots att beskrivningen påstår att de bygger på OCA
`mgmtsystem`. Det ger en dubbel verklighet: samma begrepp (klausul, gap, policy,
mål) finns både i OCA:s `mgmtsystem.*`-modeller och i Vertels `iso*.*`-modeller,
utan koppling.

Konsekvensen är att varje ny ISO-standard innebär ännu en kopia, att
gemensamma förbättringar (t.ex. klausulhierarki, mognadsskala) måste göras sex
gånger, och att en kund som vill ha flera standarder får sex oberoende
klausulträd som inte kan jämföras eller sammanställas.

## What Changes

- **Ny modul `mgmtsystem_iso_base`** med den gemensamma datamodellen för
  ISO-standarder: `mgmtsystem.iso.standard`, `mgmtsystem.iso.clause`,
  `mgmtsystem.iso.gap` och `mgmtsystem.iso.gap.line`. Modellerna behåller
  OCA:s `mgmtsystem.`-prefix.
- **BREAKING** — `iso9001.clause`, `iso14001.clause`, `iso22000.clause`,
  `iso27001.clause`, `iso42001.clause` och `sam.iso_clause` ersätts av
  `mgmtsystem.iso.clause` (med `standard_id` som skiljer standarderna).
  Motsvarande gap- och gap.line-modeller konsolideras likaså.
- **BREAKING** — de egna `iso*001.policy`- och `iso*001.objective`-modellerna
  tas bort. Policy hanteras av `mgmtsystem_manual` / `document_page`, och mål
  med KPI:er av `mgmtsystem_objective` (`mgmtsystem.objective` +
  `mgmtsystem.indicator`).
- **Skal-moduler**: varje `mgmtsystem_<standard>` blir ett tunt lager ovanpå
  `mgmtsystem_iso_base`. Skal-modulen behåller det som är unikt för standarden
  (t.ex. `iso9001.process`, 27001:s SoA, 22000:s HACCP, 42001:s kontroller) och
  lägger standardens klausuldata. Avvikelser per standard hanteras i
  skal-modulen, inte i basmodulen.
- **Beroende-kedjan rättas**: `_9001`, `_14001` och `_42001` får verkliga
  beroenden till `mgmtsystem_iso_base` och de OCA-moduler de faktiskt använder,
  i linje med hur `_27001` och `_22000` redan är byggda.
- **Datamigrering** för befintliga installationer: poster i `iso*001.clause`
  och `iso*001.gap(.line)` flyttas till de gemensamma modellerna med rätt
  `standard_id`.

## Capabilities

### New Capabilities

- `mgmtsystem-iso-base`: den gemensamma ISO-kärnan — standardregister,
  klausulträd per standard, gap-analys med mognadsbedömning, samt regler för
  hur skal-moduler utökar kärnan och hur avvikelser hanteras.

### Modified Capabilities

Inga befintliga specs finns i repot (openspec införs med denna change). De
beteenden som ändras för 9001-skalet beskrivs därför som en ny förmåga:

- `mgmtsystem-9001`: 9001-skalet — vilka delar som blir kvar unika för 9001
  (processmodellen, klausuldata 4–10) och vilka som delegeras till kärnan och
  OCA:s mål-/manualmoduler.

## Impact

- **Nya filer**: `mgmtsystem_iso_base/` (modell, vyer, säkerhet, klausuldata för
  standardregistret).
- **Ändrade moduler**: `mgmtsystem_9001`, `mgmtsystem_14001`, `mgmtsystem_22000`,
  `mgmtsystem_27001`, `mgmtsystem_42001`, `mgmtsystem_sam` — manifest,
  modeller, vyer, säkerhet, `i18n/sv.po`.
- **Borttagna modeller** (BREAKING): `iso9001.clause/gap/gap.line/policy/objective`,
  `iso14001.*`, `iso22000.*`, `iso27001.*`, `iso42001.*`, `sam.iso_clause`
  (motsvarande delar).
- **Beroenden**: `mgmtsystem_iso_base` beror på `mgmtsystem`,
  `mgmtsystem_objective` och `mgmtsystem_manual` (OCA, i
  `odooext-OCA-management-system`).
- **Databas**: migrering av befintliga klausul-, gap- och gap.line-poster krävs
  vid uppgradering av en installation som redan använder modulerna.
- **Koppling till `quality_ce`** (kontrollpunkt ↔ klausul, underkänd kontroll ↔
  nonconformity) ligger utanför denna change och hanteras i en uppföljande
  change.
