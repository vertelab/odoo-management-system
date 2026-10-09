## Purpose

Den gemensamma ISO-kärnan: ett register över vilka ledningssystemstandarder
organisationen följer, ett klausulträd per standard, och en gap-analys med
mognadsbedömning som kan köras mot vilken standard som helst — så att flera
standarder delar datamodell i stället för att var och en bygger sin egen.

## ADDED Requirements

### Requirement: Standardregister

Systemet SHALL hålla ett register över de ledningssystemstandarder som
organisationen arbetar mot (t.ex. ISO 9001, 14001, 22000, 27001, 42001,
45001). Varje standard SHALL ha ett namn, en beteckning och en version, och
kunna vara aktiv eller inaktiv.

#### Scenario: Standard skapas

- **WHEN** en användare registrerar en standard med namn, beteckning och version
- **THEN** sparas standarden i registret
- **AND** den kan väljas när klausuler och gap-analyser skapas

#### Scenario: Två standarder med samma beteckning

- **WHEN** en användare registrerar en standard vars beteckning redan finns
- **THEN** avvisas registreringen med ett valideringsfel

#### Scenario: Inaktiv standard döljs i val

- **GIVEN** en standard markerad som inaktiv
- **WHEN** en användare skapar en ny klausul
- **THEN** visas den inaktiva standarden inte bland valbara standarder
- **AND** befintliga klausuler för standarden är oförändrade

### Requirement: Klausulträd per standard

Systemet SHALL låta varje standard ha ett eget klausulträd med
klausulnummer, benämning, beskrivning och en över-/underordnad relation.
Klausulnummer SHALL vara unikt inom sin standard men behöver inte vara unikt
mellan standarder.

#### Scenario: Klausul skapas under en standard

- **WHEN** en användare skapar en klausul och väljer en standard
- **THEN** sparas klausulen med sitt klausulnummer under den standarden
- **AND** den visas i standardens klausulträd

#### Scenario: Samma klausulnummer i två standarder

- **GIVEN** klausul 5.2 finns för ISO 9001
- **WHEN** en användare skapar klausul 5.2 för ISO 27001
- **THEN** tillåts klausulen
- **AND** de två klausulerna är åtskilda av sin standard

#### Scenario: Dubbelt klausulnummer inom samma standard

- **GIVEN** klausul 5.2 finns för ISO 9001
- **WHEN** en användare skapar ytterligare en klausul 5.2 för ISO 9001
- **THEN** avvisas den med ett valideringsfel

#### Scenario: Underklausul knyts till förälder

- **WHEN** en användare anger en förälderklausul
- **THEN** visas klausulen som underklausul till föräldern
- **AND** förälderns klausulträd omfattar underklausulen

#### Scenario: Klausulens visningsnamn

- **WHEN** en klausul visas
- **THEN** framgår både klausulnummer och benämning

### Requirement: Gap-analys mot en standard

Systemet SHALL låta en användare skapa en gap-analys för en vald standard.
En gap-analys SHALL innehålla en rad per klausul och ange datum, bedömare och
status.

#### Scenario: Gap-analys skapas för en standard

- **WHEN** en användare skapar en gap-analys och väljer en standard
- **THEN** skapas analysen med den standarden
- **AND** analysens rader avser standardens klausuler

#### Scenario: Gap-analysens status följer sitt flöde

- **GIVEN** en gap-analys i utkast
- **WHEN** användaren påbörjar analysen
- **THEN** sätts status till pågående
- **AND** när analysen slutförs sätts status till klar

#### Scenario: Gap-analys utan vald standard

- **WHEN** en användare försöker skapa en gap-analys utan standard
- **THEN** avvisas den med ett valideringsfel

### Requirement: Mognadsbedömning per klausul

Varje rad i en gap-analys SHALL ange en mognadsnivå på en skala från 0 till 5,
samt ett fynd och en rekommendation. Mognadsnivån SHALL vara valfri i den mån
att en obehandlad rad motsvarar nivå 0.

#### Scenario: Mognadsnivå sätts på en rad

- **WHEN** en användare anger mognadsnivå för en rad
- **THEN** sparas nivån på raden
- **AND** nivån visas på den sexgradiga skalan

#### Scenario: Obehandlad rad har nivå noll

- **GIVEN** en nyskapad gap-analysrad
- **WHEN** raden visas utan att ha bedömts
- **THEN** visas mognadsnivå 0

#### Scenario: Fynd och rekommendation sparas per rad

- **WHEN** en användare anger fynd och rekommendation på en rad
- **THEN** sparas båda på raden
- **AND** de är kopplade till radens klausul

### Requirement: Skal-moduler utökar kärnan

En standard-specifik modul SHALL kunna utöka kärnan utan att duplicera dess
modeller. Standardens klausuldata SHALL ligga i skal-modulen, medan
klausulmodellen, gap-modellen och standardregistret tillhör kärnan.

#### Scenario: Skal-modul lägger klausuldata

- **GIVEN** kärnan med standardregistret
- **WHEN** en skal-modul installeras
- **THEN** finns standardens klausuler i kärnans klausulmodell
- **AND** de är kopplade till rätt standard i registret

#### Scenario: Skal-modul tillför egna modeller

- **GIVEN** en standard med behov utöver klausuler och gap
- **WHEN** skal-modulen tillför en egen modell
- **THEN** kan modellen kopplas till kärnans klausuler
- **AND** kärnans modeller förblir oförändrade

#### Scenario: Gemensam förbättring slår igenom för alla standarder

- **GIVEN** flera standarder som använder kärnans klausulmodell
- **WHEN** kärnans klausulmodell ändras
- **THEN** gäller ändringen alla standarder
- **AND** ingen skal-modul behöver ändras för ändringen

### Requirement: Avvikelser hanteras i skal-modulen

När en standard avviker från kärnans gemensamma modell SHALL avvikelsen
hanteras i standardens skal-modul, inte genom att kärnan specialiseras.

#### Scenario: Standard saknar ett gemensamt begrepp

- **GIVEN** en standard som inte använder ett av kärnans begrepp
- **WHEN** skal-modulen installeras
- **THEN** är kärnans modell oförändrad
- **AND** skal-modulen väljer att inte använda begreppet

#### Scenario: Standard behöver ett extra fält

- **GIVEN** en standard som behöver ett fält kärnan inte har
- **WHEN** skal-modulen utökar kärnans modell
- **THEN** läggs fältet till i skal-modulen
- **AND** andra standarder påverkas inte

### Requirement: Företagsavskärmning

Kärnans poster SHALL avskärmas per företag, så att en användare bara ser
standarder, klausuler, gap-analyser och gap-rader som tillhör användarens
företag.

#### Scenario: Klausuler avskärmas per företag

- **GIVEN** klausuler registrerade för två olika företag
- **WHEN** en användare i det ena företaget listar klausuler
- **THEN** visas bara det egna företagets klausuler

#### Scenario: Gap-analys avskärmas per företag

- **GIVEN** gap-analyser registrerade för två olika företag
- **WHEN** en användare i det ena företaget listar gap-analyser
- **THEN** visas bara det egna företagets analyser
