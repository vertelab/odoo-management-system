# odoo-management-system

Vertels ledningssystemmoduler för Odoo 18 — ISO-standarder ovanpå OCA:s
`mgmtsystem`-moduler.

## Arkitektur: gemensam ISO-kärna + skal-moduler

Sedan change `iso-common-core` delar alla ISO-standarder **en** datamodell i
stället för att var och en definierar sin egen klausul- och gap-modell.

```
  mgmtsystem_iso_base          (kärnan — depends: mgmtsystem,
  ├── mgmtsystem.iso.standard      mgmtsystem_objective, mgmtsystem_manual)
  ├── mgmtsystem.iso.clause       standarder som POSTER (9001, 14001, …)
  ├── mgmtsystem.iso.gap          klausulnummer unikt PER standard
  └── mgmtsystem.iso.gap.line     mognadsbedömning 0–5

  mgmtsystem_9001              (skal — depends: mgmtsystem_iso_base)
  ├── iso9001.process             unikt för 9001 (OCA har ingen processmodell)
  ├── klausuldata 4–10            i kärnans klausulmodell
  └── dashboard                   pivot över kärnans gap-rader

  mgmtsystem_27001 / _14001 / _22000 / _42001 / _sam
                                  (skal — migreras i uppföljande changes)
```

### Regler

- **Standarder är data, inte modeller.** Lägg en ny standard som en post i
  `mgmtsystem.iso.standard`, inte som en ny modul med egna modeller.
- **Skal-moduler använder `_inherit`**, inte egna modeller. Standard-specifika
  fält läggs på kärnans modeller (samma mönster som `mgmtsystem_27001` redan
  använder mot `mgmtsystem.action`).
- **Avvikelser hanteras i skal-modulen.** Behöver en standard ett extra fält
  eller en egen modell (SoA, HACCP, processer) ligger det i skal-modulen —
  kärnan specialiseras aldrig.
- **Policy och mål rivs inte upp igen.** Policy → `mgmtsystem_manual` /
  `document_page`; mål med KPI:er → `mgmtsystem_objective`.

## Beroenden

`requirements.repo` drar in OCA:s management-system-repo:

```
git@github.com:OCA/management-system.git /usr/share/odooext-OCA-management-system
```

`mgmtsystem_iso_base` kräver att den finns i addons-path.

## Migrering

`mgmtsystem_9001` version `18.0.1.1.0` migrerar befintliga `iso9001.clause`,
`iso9001.gap` och `iso9001.gap.line` till kärnans modeller. Migreringen är
idempotent, säker utan gamla tabeller, och **droppar aldrig** de gamla
tabellerna — se `mgmtsystem_9001/readme/DESCRIPTION.md` för rollback.

## Öppna changes

- `iso-common-core` — kärnan + 9001-skalet (denna).
- `quality-mgmtsystem-nonconformity` — brygga till `quality_ce`.
- Uppföljande: migrera 14001/42001 (fas 3) och 27001/22000/sam (fas 4).
