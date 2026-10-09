## 1. Bryggmodulens stomme

- [x] 1.1 Skapa modulkatalogen `quality_mgmtsystem_nonconformity/` med
      `__init__.py`, `__manifest__.py` (depends: `quality_ce`,
      `mgmtsystem_nonconformity`) och tomma `models/`, `views/`, `security/`,
      `data/`, `i18n/`. Verifiera att manifestet parsar och att modulen syns i
      applistan.
- [x] 1.2 Skapa `security/ir.model.access.csv` för nya fält/åtgärder och
      verifiera att modulen installeras utan behörighetsfel.
- [x] 1.3 Lägg `data/nonconformity_origin_data.xml` med en återanvändbar
      `mgmtsystem.nonconformity.origin` (`ref_code` `quality_check`). Verifiera
      att posten finns efter installation och är aktiv.

## 2. Bakåtlänk på kvalitetssidan

- [x] 2.1 Lägg `nonconformity_id` (M2O till `mgmtsystem.nonconformity`) på
      `quality.check` via `_inherit`. Verifiera att fältet syns i kontrollens
      form och att det går att sätta och spara.
- [x] 2.2 Lägg `nonconformity_id` (M2O) på `quality.alert` via `_inherit`.
      Verifiera att fältet syns i alertens form.
- [x] 2.3 Lägg en compute för att visa om en nonconformity finns (för
      knappens tillstånd). Verifiera att en kontroll med nonconformity visar
      det.

## 3. Skapa nonconformity ur kontroll

- [x] 3.1 Implementera `action_create_nonconformity()` på `quality.check`:
      härled namn, beskrivning, allvarlighetsgrad, företag, produkt, parti och
      partner enligt designens Beslut 5, samt **alla obligatoriska fält** enligt
      Beslut 6 (`partner_id`, `responsible_user_id`, `manager_user_id`,
      `origin_ids`). `manager_user_id` härleds ur utförarens `hr.employee` →
      `parent_id` (chef) → chefens `user_id`. Verifiera med test att
      nonconformityn skapas med rätt fält ur en underkänd kontroll, och att
      skapandet inte faller på ett obligatoriskt fält.
- [x] 3.2 Sätt `res_model`/`res_id` på den skapade nonconformityn till
      kontrollen, och `origin_ids` till den återanvändbara orsaken. Verifiera
      med test att bakåtlänken pekar på rätt kontroll.
- [x] 3.3 Sätt kontrollens `nonconformity_id` till den skapade posten och
      returnera en åtgärd som öppnar nonconformityn. Verifiera att kontrollens
      bakåtlänk är satt och att åtgärden öppnar rätt post.
- [x] 3.4 Gör åtgärden idempotent: finns redan en nonconformity ska den
      befintliga öppnas och ingen ny skapas. Verifiera med test som anropar
      åtgärden två gånger och förväntar exakt en nonconformity.
- [x] 3.5 Dölj/avaktivera åtgärden när kontrollen inte är underkänd.
      Verifiera att åtgärden inte erbjuds för godkänd eller obehandlad kontroll.

## 4. Skapa nonconformity ur alert

- [x] 4.1 Implementera `action_create_nonconformity()` på `quality.alert` med
      samma härledning som för kontrollen (inkl. obligatoriska fält enligt
      Beslut 6), och koppla till alertens kontroll när en sådan finns.
      Verifiera med test att nonconformityn skapas och länkar till både alert
      och kontroll.
- [x] 4.2 Gör även denna åtgärd idempotent. Verifiera med test att upprepade
      anrop ger exakt en nonconformity.

## 5. Vyer och knappar

- [x] 5.1 Lägg knappen "Skapa avvikelse" på kontrollens och alertens form,
      med tillståndsstyrning enligt 3.5. Verifiera att knappen syns bara när
      den är användbar.
- [x] 5.2 Lägg bakåtlänken i nonconformityns form (via `res_model`/`res_id`)
      så att ursprungskontrollen kan öppnas. Verifiera att en nonconformity
      skapad ur en kontroll visar och kan öppna kontrollen.
- [x] 5.3 Lägg klausulkopplingen på kontrollpunktens form (M2M till
      `mgmtsystem.iso.clause`) — förutsätter `iso-common-core`. Verifiera att
      klausuler kan kopplas och visas.

## 6. Säkerhet och översättning

- [x] 6.1 Verifiera företagsavskärmning: en användare kan inte skapa en
      nonconformity ur en kontroll i ett annat företag, och klausuler i annat
      företag erbjuds inte. Testa med två företag.
- [x] 6.2 Skapa `i18n/sv.po` för nya fältetiketter och åtgärdsnamn, genererad
      via `checkmodule -e`. Verifiera att svenska strängar visas i
      gränssnittet.

## 7. Integration och verifiering

- [x] 7.1 Kör `checkmodule -t` för `quality_mgmtsystem_nonconformity` på en
      testdatabas och verifiera att alla tester passerar.
- [x] 7.2 Verifiera i en riktig Odoo 18-miljö hela kedjan: skapa en
      kontrollpunkt med klausul, utför en kontroll som underkänns, skapa
      nonconformity, och kontrollera att nonconformityn syns i
      ledningssystemets avvikelselista med rätt ursprung.
- [x] 7.3 Dokumentera i modulens README att rotorsak inte kopieras mellan
      `quality.alert.reason_id` och nonconformityns `cause_ids` (olika
      taxonomier), och att åtgärden är manuell avsiktligt.
