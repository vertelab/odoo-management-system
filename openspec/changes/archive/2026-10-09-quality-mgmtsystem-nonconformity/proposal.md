## Why

`quality_ce` och ledningssystemet beskriver samma sak på två håll utan att
känna varandra. En underkänd kvalitetskontroll skapar i dag en `quality.alert`
— ett operativt ärende på golvet, med karantän och åtgärd — men ledningssystemet
får aldrig veta något. Samtidigt kräver ISO 9001 (§8.7, §10.2) att en avvikelse
blir en **nonconformity** med rotorsaksanalys, korrigerande åtgärd och
effektivitetsuppföljning. I dag måste den kedjan registreras manuellt en andra
gång, i `mgmtsystem.nonconformity`, av en människa som råkar komma ihåg det.

Samma sak gäller spårbarheten bakåt: en kontrollpunkt (`quality.point`) har
inget samband med den ISO-klausul som kräver kontrollen. Vid en revision går
det inte att visa *varför* en viss kontroll finns — bara att den finns.

Repot har redan ett beprövat mönster för den här sortens koppling:
`fire_protection_fsm_bridge` och `saltstack_managementsystem` är båda rena
bryggmoduler som kopplar sin domän till `mgmtsystem.nonconformity` via
`_inherit`, ett M2O och en `action_create_*` som sätter bakåtlänken. Den här
change:n följer samma mönster för kvalitetsdomänen.

## What Changes

- **Ny bryggmodul `quality_mgmtsystem_nonconformity`** med smalt beroende till
  `quality_ce` och `mgmtsystem_nonconformity`.
- **Kontrollpunkt kopplas till ISO-klausul**: `quality.point` får ett M2M till
  `mgmtsystem.iso.clause` (kärnan från `iso-common-core`), så att det framgår
  vilken klausul som kräver kontrollen.
- **Underkänd kontroll kan bli nonconformity**: en åtgärd på `quality.check`
  (och på `quality.alert`) skapar en `mgmtsystem.nonconformity` med
  bakåtlänk via `res_model`/`res_id`, severity från kontrollens utfall, och
  beskrivning som sammanställs ur kontrollen.
- **Bakåtlänk åt andra hållet**: `mgmtsystem.nonconformity` får en referens
  tillbaka till den kontroll eller alert den uppstod ur, så att en
  nonconformity kan öppna sitt ursprung.
- **Idempotens**: en kontroll som redan har en nonconformity ska inte skapa en
  till; åtgärden ska i stället öppna den befintliga.
- **Ingen ny avvikelsemodell**: `quality.alert` och `mgmtsystem.nonconformity`
  förblir två modeller med olika hemvist (golv respektive ledningssystem).
  Bryggan förenar dem, den slår inte ihop dem.

## Capabilities

### New Capabilities

- `quality-iso-nonconformity`: bryggan mellan kvalitetskontroller och
  ledningssystemets avvikelsehantering — kontrollpunktens klausulkoppling,
  skapandet av nonconformity ur en underkänd kontroll, bakåtlänken mellan dem,
  och idempotensreglerna.

### Modified Capabilities

Inga. Ändringen är additiv: den lägger en brygga ovanpå `quality_ce` och
`mgmtsystem.nonconformity` utan att ändra deras befintliga beteende. Den
förutsätter `iso-common-core` (för `mgmtsystem.iso.clause`), men den change:n
äger klausulmodellen.

## Impact

- **Ny modul**: `quality_mgmtsystem_nonconformity/` (modell, vyer, säkerhet,
  `i18n/sv.po`).
- **Beroenden**: `quality_ce` (i `odoo-quality`), `mgmtsystem_nonconformity`
  (OCA, i `odooext-OCA-management-system`) och `mgmtsystem_iso_base` (från
  `iso-common-core`) för klausulkopplingen.
- **Ändrade modeller via `_inherit`**: `quality.point` (M2M till klausul),
  `quality.check` och `quality.alert` (åtgärd + bakåtlänk),
  `mgmtsystem.nonconformity` (bakåtlänk till kontroll/alert).
- **Beroende mellan changes**: denna change förutsätter att `iso-common-core`
  är implementerad (annars finns ingen `mgmtsystem.iso.clause` att koppla
  kontrollpunkten till). Klausulkopplingen kan annars skjutas upp, men
  nonconformity-bryggan står på egna ben.
- **Utanför scope**: helpdesk-kopplingen (avvikelse → ärende) och att slå ihop
  `quality.alert` med `mgmtsystem.nonconformity`.
