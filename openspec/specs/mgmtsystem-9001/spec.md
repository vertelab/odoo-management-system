# mgmtsystem-9001 Specification

## Purpose

9001-skalet: kvalitetsledningssystemet enligt ISO 9001 ovanpå den gemensamma
ISO-kärnan — det som är unikt för kvalitetsledning (processmodellen och
klausulerna 4–10) ligger kvar här, medan klausulträd, gap-analys, policy och
mål delegeras till kärnan och OCA:s manual- och målmoduler.

## Requirements

### Requirement: 9001 bygger på den gemensamma kärnan

9001-modulen SHALL vara ett tunt lager ovanpå den gemensamma ISO-kärnan och
SHALL använda kärnans standardregister, klausulmodell och gap-modell i stället
för att definiera egna.

#### Scenario: 9001 registreras som standard i kärnan

- **WHEN** 9001-modulen installeras
- **THEN** finns ISO 9001 som post i kärnans standardregister
- **AND** 9001:s klausuler ligger i kärnans klausulmodell kopplade till den posten

#### Scenario: Ingen egen klausulmodell

- **GIVEN** 9001-modulen installerad
- **WHEN** en användare listar tillgängliga modeller för klausuler
- **THEN** finns ingen 9001-specifik klausulmodell
- **AND** kärnans klausulmodell används

#### Scenario: Gap-analys för 9001 använder kärnan

- **WHEN** en användare skapar en gap-analys med ISO 9001 som standard
- **THEN** skapas analysen i kärnans gap-modell
- **AND** raderna avser ISO 9001:s klausuler

### Requirement: Klausuldata för ISO 9001

9001-modulen SHALL tillhandahålla klausulerna 4–10 med svenska benämningar och
beskrivningar, kopplade till ISO 9001-posten i standardregistret.

#### Scenario: Klausuler installeras med modulen

- **WHEN** 9001-modulen installeras
- **THEN** finns klausulerna 4–10 i kärnans klausulmodell
- **AND** varje klausul är kopplad till ISO 9001

#### Scenario: Klausulhierarkin bevaras

- **WHEN** klausulerna visas
- **THEN** framgår huvudklausuler och underklausuler i rätt ordning
- **AND** en underklausul pekar på sin huvudklausul

### Requirement: Processmodell för kvalitetsledning

9001-modulen SHALL tillhandahålla en processmodell för organisationens
processer, med processägare, typ av process, in- och utdata, resurser, KPI:er
och koppling till relevanta ISO 9001-klausuler.

#### Scenario: Process skapas

- **WHEN** en användare skapar en process och anger namn och processtyp
- **THEN** sparas processen med sitt namn och sin typ
- **AND** den kan kopplas till en eller flera ISO 9001-klausuler

#### Scenario: Process kopplas till klausul

- **GIVEN** en process och en klausul i kärnan
- **WHEN** en användare kopplar processen till klausulen
- **THEN** framgår kopplingen på processen
- **AND** klausulen förblir kärnans post

#### Scenario: Processens livscykel

- **GIVEN** en process i utkast
- **WHEN** användaren aktiverar processen
- **THEN** sätts processen till aktiv
- **AND** den kan senare avaktiveras

### Requirement: Policy och mål delegeras till OCA-moduler

9001-modulen SHALL inte definiera egna policy- eller målmodeller. Policy SHALL
hanteras av manual-/dokumentmodulen och mål med KPI:er av målmodulen.

#### Scenario: Ingen egen policymodell

- **GIVEN** 9001-modulen installerad
- **WHEN** en användare söker efter en 9001-specifik policymodell
- **THEN** finns ingen sådan
- **AND** policyn hanteras i manual-/dokumentmodulen

#### Scenario: Ingen egen målmodell

- **GIVEN** 9001-modulen installerad
- **WHEN** en användare söker efter en 9001-specifik målmodell
- **THEN** finns ingen sådan
- **AND** mål och KPI:er hanteras i målmodulen

#### Scenario: Mål knyts till kvalitetsledningssystemet

- **WHEN** en användare skapar ett mål för kvalitetsledningen
- **THEN** kan målet knytas till systemet i manual-/dokumentmodulen
- **AND** målets KPI:er hanteras av målmodulen

### Requirement: Befintliga poster migreras till kärnan

Vid uppgradering av en installation som använder den tidigare 9001-modulens
egna modeller SHALL befintliga klausul-, gap- och gap-rad-poster flyttas till
kärnans modeller och kopplas till ISO 9001.

#### Scenario: Klausuler migreras

- **GIVEN** en installation med poster i den tidigare 9001-specifika klausulmodellen
- **WHEN** modulen uppgraderas
- **THEN** finns posterna i kärnans klausulmodell
- **AND** de är kopplade till ISO 9001

#### Scenario: Gap-analyser migreras

- **GIVEN** en installation med poster i den tidigare 9001-specifika gap-modellen
- **WHEN** modulen uppgraderas
- **THEN** finns analyserna och deras rader i kärnans gap-modell
- **AND** radernas mognadsnivåer är bevarade

#### Scenario: Ingen data dubbleras vid migrering

- **GIVEN** en installation som migreras
- **WHEN** migreringen är klar
- **THEN** finns varje klausul och varje gap-analys på ett enda ställe
- **AND** inga dubbletter har skapats
