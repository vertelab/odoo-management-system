## Purpose

Bryggan mellan kvalitetskontroller och ledningssystemets avvikelsehantering:
kontrollpunkter kopplas till de ISO-klausuler som kräver dem, och en underkänd
kontroll kan bli en nonconformity med rotorsaksanalys och korrigerande åtgärd
— med bakåtlänk åt båda hållen, så att golvets kvalitetsarbete och
ledningssystemets avvikelsehantering beskriver samma händelse.

## ADDED Requirements

### Requirement: Kontrollpunkt kopplas till ISO-klausul

En kontrollpunkt SHALL kunna kopplas till en eller flera ISO-klausuler, så att
det framgår vilken klausul som kräver kontrollen.

#### Scenario: Kontrollpunkt kopplas till klausul

- **WHEN** en användare kopplar en kontrollpunkt till en ISO-klausul
- **THEN** sparas kopplingen på kontrollpunkten
- **AND** klausulen visas bland kontrollpunktens klausuler

#### Scenario: Kontrollpunkt utan klausul

- **GIVEN** en kontrollpunkt utan klausulkoppling
- **WHEN** kontrollpunkten visas
- **THEN** framgår att ingen klausul är kopplad
- **AND** kontrollpunkten fungerar som förut

#### Scenario: Klausulens kontrollpunkter

- **GIVEN** en klausul med kopplade kontrollpunkter
- **WHEN** klausulen visas
- **THEN** framgår vilka kontrollpunkter som krävs av klausulen

### Requirement: Underkänd kontroll kan bli nonconformity

Systemet SHALL låta en användare skapa en nonconformity ur en underkänd
kvalitetskontroll, så att avvikelsen hamnar i ledningssystemets
avvikelsehantering utan att registreras en andra gång manuellt.

#### Scenario: Nonconformity skapas ur underkänd kontroll

- **GIVEN** en kontroll med utfallet underkänd
- **WHEN** användaren väljer att skapa en nonconformity
- **THEN** skapas en nonconformity i ledningssystemet
- **AND** dess beskrivning sammanställs ur kontrollens uppgifter
- **AND** den är kopplad tillbaka till kontrollen

#### Scenario: Godkänd kontroll ger ingen nonconformity

- **GIVEN** en kontroll med utfallet godkänd
- **WHEN** användaren ser kontrollens åtgärder
- **THEN** erbjuds ingen åtgärd för att skapa en nonconformity

#### Scenario: Kontroll utan utfall

- **GIVEN** en kontroll som ännu inte bedömts
- **WHEN** användaren ser kontrollens åtgärder
- **THEN** erbjuds ingen åtgärd för att skapa en nonconformity

### Requirement: Nonconformity kan skapas ur en kvalitetsalert

Systemet SHALL låta en användare skapa en nonconformity ur en kvalitetsalert,
så att en avvikelse som redan hanteras som ärende på golvet kan föras in i
ledningssystemet.

#### Scenario: Nonconformity skapas ur alert

- **GIVEN** en kvalitetsalert
- **WHEN** användaren väljer att skapa en nonconformity
- **THEN** skapas en nonconformity i ledningssystemet
- **AND** den är kopplad tillbaka till alerten
- **AND** om alerten hör till en kontroll är den också kopplad till kontrollen

### Requirement: Nonconformityns uppgifter härleds ur kontrollen

Den skapade nonconformityn SHALL ärva de uppgifter som finns på kontrollen:
namn, beskrivning, allvarlighetsgrad, ansvarig, chef, företag och, när det
finns, produkt, parti och partner. De fält som ledningssystemet kräver för att
en avvikelse ska kunna registreras SHALL alltid sättas, så att åtgärden inte
blockeras av att kontrollen saknar uppgiften.

#### Scenario: Namn och beskrivning sammanställs

- **GIVEN** en underkänd kontroll med titel och notering
- **WHEN** nonconformityn skapas
- **THEN** får den ett namn som identifierar kontrollen
- **AND** beskrivningen innehåller kontrollens notering och utfall

#### Scenario: Allvarlighetsgrad följer kontrollens utfall

- **GIVEN** en kontroll vars utfall och mätvärde anger en allvarlig avvikelse
- **WHEN** nonconformityn skapas
- **THEN** sätts en allvarlighetsgrad som motsvarar avvikelsens grad

#### Scenario: Företag följer kontrollen

- **GIVEN** en kontroll tillhörande ett företag
- **WHEN** nonconformityn skapas
- **THEN** tillhör nonconformityn samma företag

#### Scenario: Partner saknas på kontrollen

- **GIVEN** en kontroll utan kopplad partner
- **WHEN** nonconformityn skapas
- **THEN** skapas nonconformityn ändå
- **AND** en partner härleds ur kontrollens sammanhang eller lämnas enligt
  ledningssystemets krav

#### Scenario: Chef härleds ur den anställdes organisationstillhörighet

- **GIVEN** en kontroll vars utförare är kopplad till en anställd med en chef
- **WHEN** nonconformityn skapas
- **THEN** sätts avvikelsens chef till chefens användare
- **AND** chefens användare härleds ur den anställdes chefspost

#### Scenario: Chef saknas för utföraren

- **GIVEN** en kontroll vars utförare saknar anställd eller chef
- **WHEN** nonconformityn skapas
- **THEN** skapas nonconformityn ändå
- **AND** avvikelsens chef faller tillbaka på avvikelsens ansvariga

### Requirement: Bakåtlänk mellan nonconformity och kontroll

En nonconformity som skapats ur en kontroll eller alert SHALL bära en
bakåtlänk till sitt ursprung, så att nonconformityn kan öppna det.

#### Scenario: Nonconformity länkar till kontroll

- **GIVEN** en nonconformity skapad ur en kontroll
- **WHEN** nonconformityn visas
- **THEN** framgår vilken kontroll den uppstod ur
- **AND** användaren kan öppna kontrollen därifrån

#### Scenario: Kontrollen länkar till nonconformity

- **GIVEN** en kontroll med en skapad nonconformity
- **WHEN** kontrollen visas
- **THEN** framgår att en nonconformity finns
- **AND** användaren kan öppna den därifrån

#### Scenario: Ursprunget registreras som avvikelseorsak

- **GIVEN** en nonconformity skapad ur en kvalitetskontroll
- **WHEN** nonconformityn visas
- **THEN** är dess orsak satt till ett ursprung som anger kvalitetskontroll
- **AND** ursprunget är återanvändbart för fler avvikelser

### Requirement: En kontroll ger högst en nonconformity

Systemet SHALL säkerställa att en kontroll eller alert inte skapar mer än en
nonconformity. Finns redan en nonconformity SHALL åtgärden öppna den i stället
för att skapa en ny.

#### Scenario: Åtgärden öppnar befintlig nonconformity

- **GIVEN** en kontroll som redan har en nonconformity
- **WHEN** användaren väljer att skapa en nonconformity
- **THEN** skapas ingen ny
- **AND** den befintliga nonconformityn öppnas

#### Scenario: Upprepade anrop dubblerar inte

- **GIVEN** en underkänd kontroll
- **WHEN** åtgärden för att skapa nonconformity körs två gånger
- **THEN** finns exakt en nonconformity kopplad till kontrollen

### Requirement: Företagsavskärmning

Bryggans kopplingar SHALL respektera företagsavskärmning, så att en
nonconformity bara kan skapas ur en kontroll inom användarens företag och
klausulkopplingen bara omfattar klausuler inom samma företag.

#### Scenario: Kontroll i annat företag

- **GIVEN** en kontroll tillhörande ett annat företag än användarens
- **WHEN** användaren försöker skapa en nonconformity ur den
- **THEN** nekas åtgärden

#### Scenario: Klausul i annat företag

- **GIVEN** en klausul tillhörande ett annat företag än kontrollpunkten
- **WHEN** en användare kopplar kontrollpunkten till klausulen
- **THEN** erbjuds inte klausulen bland valbara klausuler
