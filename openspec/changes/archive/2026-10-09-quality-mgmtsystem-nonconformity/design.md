## Context

Se `proposal.md` — Why, för motivering. Det som styr designen:

- **Bryggmönstret finns redan** i repot: `fire_protection_fsm_bridge`
  (`depends: [fire_protection_sba, mgmtsystem_nonconformity, fieldservice]`)
  och `saltstack_managementsystem` (`depends: [saltstack_ai,
  mgmtsystem_nonconformity]`). Båda är rena bryggmoduler utan egen domänmodell.
  `fire_protection_fsm_bridge` gör `_inherit = "mgmtsystem.nonconformity"`,
  lägger ett M2O till sin domän och har `action_create_fsm_order()` som sätter
  `origin = "mgmtsystem.nonconformity,<id>"` på målposten.
- **`mgmtsystem.nonconformity` har redan generiska bakåtlänk-fält**:
  `res_model` (Char) och `res_id` (Integer). Inget nytt fält behövs för att
  peka tillbaka på en kontroll.
- **Två fält på nonconformity är `required=True`** och måste hanteras:
  `partner_id` (res.partner) och `origin_ids` (M2M till
  `mgmtsystem.nonconformity.origin`).
- **`quality.check` har redan** `partner_id` (related från `picking_id`),
  `product_id`, `lot_id`, `company_id`, `user_id`, `note`, `quality_state`
  (none/pass/fail) och `alert_ids` → `quality.alert`.
- **`quality.alert` har** `check_id` → `quality.check`, `partner_id` (Vendor),
  `user_id`, `product_id`, `lot_id`, `company_id`, `priority`, `reason_id`
  (Root Cause) och `action_corrective`/`action_preventive` (Html).
- **`quality.point` har inget klausulfält** — klausulkopplingen är genuint ny
  och kräver `mgmtsystem.iso.clause` från `iso-common-core`.
- **`mgmtsystem.nonconformity.origin`** är hierarkisk (`parent_id`,
  `ref_code`, `active`) och återanvändbar — en origin "Kvalitetskontroll" kan
  sättas en gång och användas av alla avvikelser.

## Goals / Non-Goals

**Goals:**

- En bryggmodul som följer det befintliga mönstret, så att den känns igen.
- Underkänd kontroll → nonconformity med ett klick, utan dubbelregistrering.
- Spårbarhet bakåt: kontrollpunkt → klausul, nonconformity → kontroll.
- Idempotens: högst en nonconformity per kontroll.
- Alla obligatoriska fält på nonconformity härleds, så att åtgärden aldrig
  blockeras av saknad data (se Beslut 6).

**Non-Goals:**

- Att slå ihop `quality.alert` och `mgmtsystem.nonconformity` till en modell.
- Att automatiskt skapa nonconformity vid varje underkänd kontroll (se
  Beslut 4).
- Helpdesk-koppling (egen uppföljande change).
- Att bygga om `quality_ce`s egna flöden (karantän, skrotning) — de behålls.

## Decisions

### Beslut 1: Egen bryggmodul, inte utökning av quality_ce

Modulen `quality_mgmtsystem_nonconformity` med `depends: [quality_ce,
mgmtsystem_nonconformity, mgmtsystem_iso_base]`.

**Varför:** `quality_ce` är en port av Enterprise-modulen och ska förbli
beroende av `stock` — inte av ledningssystemet. En kund som vill ha kvalitet
utan ISO ska kunna installera `quality_ce` utan att dra in
`mgmtsystem.nonconformity`. Bryggmodulen gör kopplingen valfri.

**Alternativ:** lägga fälten direkt i `quality_ce`. Förkastat — det tvingar
ISO-beroendet på alla kvalitetsinstallationer och bryter mot hur
`fire_protection_fsm_bridge` och `saltstack_managementsystem` är byggda.

### Beslut 2: Bakåtlänk via befintliga `res_model`/`res_id`

Nonconformityn pekar tillbaka på kontrollen/alerten via `res_model` +
`res_id` (som redan finns), inte via ett nytt M2O-fält.

**Varför:** fälten finns, är generiska och används redan av mönstret. Ett nytt
`quality_check_id`-fält skulle binda nonconformity-modellen till
kvalitetsdomänen och kräva att OCA-modellen ändras i onödan.

**Alternativ:** eget M2O `quality_check_id` på nonconformity. Förkastat —
onödig domänkoppling i en OCA-modell, och vi vill kunna peka på *antingen*
kontroll eller alert.

**Konsekvens:** åt andra hållet behövs ett fält på `quality.check`/`quality.alert`
för att hitta sin nonconformity (en compute/search över `res_model`/`res_id`,
eller ett eget M2O som sätts vid skapandet). Här väljs ett **eget M2O på
quality-sidan** (`nonconformity_id`), eftersom det ger en snabb bakåtlänk och
en enkel idempotenskontroll utan att söka i nonconformity-tabellen.

### Beslut 3: `origin_ids` sätts till en återanvändbar origin

Bryggan lägger en `mgmtsystem.nonconformity.origin` med `ref_code` (t.ex.
`quality_check`) som data, och sätter den på varje skapad nonconformity.

**Varför:** `origin_ids` är `required=True` — nonconformityn kan inte skapas
utan. En fast, återanvändbar origin gör också att avvikelser från
kvalitetskontroller kan filtreras och rapporteras som grupp.

### Beslut 4: Skapandet är en manuell åtgärd, inte automatiskt

`action_create_nonconformity()` anropas av användaren på kontrollen/alerten.
Ingen automatisk hook på `do_fail()`.

**Varför:** inte varje underkänd kontroll är en ledningssystemsavvikelse — en
omkontroll kan räcka. Automatik skulle fylla ledningssystemet med brus och
urholka nonconformity-begreppet. Detta är också skillnaden mot
`fire_protection_fsm_bridge`, där åtgärden är manuell av samma skäl.

**Alternativ:** automatisk hook i `do_fail()`. Förkastat — se ovan. Kan läggas
till senare som en inställning om behovet visar sig.

### Beslut 5: `partner_id` härleds, krävs inte på kontrollen

Eftersom nonconformityns `partner_id` är `required=True` härleder bryggan den
i tur och ordning: kontrollens `partner_id` → alertens `partner_id` →
företagets partner → användarens partner. Är ingen tillgänglig skapas
nonconformityn ändå mot företagets partner.

**Varför:** en kvalitetskontroll i produktion (t.ex. på en tillverkningsorder)
har ofta ingen extern partner. Att blockera åtgärden då vore fel — avvikelsen
är verklig även utan kund. Företagets partner är den rimliga nödlösningen.

**Alternativ:** göra `partner_id` valfri på nonconformity (OCA-ändring).
Förkastat — att ändra en OCA-modells krav för vår skull är en större
inkräktan än att härleda ett värde.

### Beslut 6: Alla obligatoriska fält på nonconformity härleds

`mgmtsystem.nonconformity` har **fem** fält med `required=True`, varav fyra
saknar default. Verifierat live: `create({"name": ..., "description": ...})`
faller på `NotNullViolation` för `partner_id`, och därefter på
`responsible_user_id`, `manager_user_id` och `origin_ids`. Bryggan måste sätta
alla fem:

| Fält | Krav | Härleds ur |
|---|---|---|
| `partner_id` | required, ingen default | Beslut 5 |
| `responsible_user_id` | required, ingen default | kontrollens `user_id` → alertens `user_id` → `env.user` |
| `manager_user_id` | required, ingen default | utförarens `hr.employee` → `parent_id` (chef) → chefens `user_id`; faller tillbaka på `responsible_user_id` |
| `origin_ids` | required, ingen default | Beslut 3 (fast origin) |
| `user_id` | required, **har default** (`env.user`) | lämnas orörd |
| `description` | required | sammanställs ur kontrollen |

**Varför härleda i stället för att kräva:** samma skäl som Beslut 5 — en
avvikelse på golvet är verklig även när ansvarig eller chef inte är satt på
kontrollen. Att blockera registreringen vore fel; den som skapar avvikelsen
blir ansvarig i sista hand.

**`manager_user_id` via `hr.employee`:** kedjan är
`res.users` → `hr.employee.user_id` → `hr.employee.parent_id` (fältet heter
"Manager") → `parent_id.user_id`.

⚠ **Rättelse:** designen påstod först att `hr` redan är installerad som en
följd av `mgmtsystem_nonconformity`. Det är **fel** — beroendekedjan är
`mgmtsystem_nonconformity` → `mgmtsystem_action` → `mgmtsystem` + `mail`, och
inget i den drar in `hr`. Verifierat i testdatabas: `hr` var `uninstalled`.
Bryggan lägger därför till `hr` som **eget beroende** (det är en Odoo-kärnmodul,
låg kostnad) och gör dessutom uppslaget defensivt, så att modulen inte kraschar
om `hr` senare tas bort: saknas modellen faller chefsfältet tillbaka på
`responsible_user_id`.

**Alternativ:** en wizard som tvingar användaren att fylla i ansvarig och chef.
Förkastat — det gör den manuella åtgärden tyngre än den behöver vara, och
Beslut 4 säger att åtgärden ska vara ett klick.

### Beslut 7: Klausulkopplingen läggs på kontrollpunkten, inte på kontrollen
`quality.point` får M2M till `mgmtsystem.iso.clause`. Kontroller som skapas ur
punkten ärver kopplingen via sin `point_id`.

**Varför:** klausulen kräver en *typ* av kontroll (en kontrollpunkt), inte en
enskild kontroll. Att lägga kopplingen på punkten gör att den ärvs och att
spårbarheten är rätt från början.

## Risks / Trade-offs

- **Beroende till `iso-common-core`** → `mgmtsystem.iso.clause` finns inte
  förrän den change:n är implementerad. Mitigering: bryggmodulens
  nonconformity-del står på egna ben; klausulkopplingen kan läggas i en
  separat modul (`quality_mgmtsystem_iso`) om man vill undvika
  beroendeordningen.
- **`res_model`/`res_id` är inte indexerade som par** → bakåtlänken blir en
  sökning. Mitigering: det egna M2O:t på quality-sidan (`nonconformity_id`)
  gör den vanliga riktningen snabb; `res_model`/`res_id` används bara för
  spårbarhet.
- **`quality.check` skapas i stora mängder** (en per kontrollpunkt per
  operation) → att lägga ett M2O-fält på den är billigt, men vyer måste vara
  försiktiga så att kontrollistan inte blir tung. Mitigering: fältet visas bara
  i kontrollens form, inte i listan.
- **`manager_user_id` kan bli tom** om utföraren saknar `hr.employee`-post,
  chefen saknar `user_id`, eller `hr` inte är installerad → Mitigering:
  uppslaget är defensivt och faller tillbaka på `responsible_user_id`, som i
  sin tur faller tillbaka på `env.user`. Åtgärden blockeras aldrig.
- **Översättning** → nya fältetiketter och åtgärdsnamn måste in i `sv.po`,
  genererat via `checkmodule -e` (handskrivna utan `#: model:`-referenser
  appliceras aldrig).
- **`quality.alert` har egen `reason_id` (Root Cause)** medan nonconformity har
  `cause_ids` → två rotorsaksbegrepp. Mitigering: bryggan kopierar inte
  rotorsak automatiskt (de har olika taxonomier); den lämnas att fylla i
  ledningssystemet. Dokumenteras i README.

## Migration Plan

1. **Fas 1 — bryggmodulen skapas** med nonconformity-delen (åtgärder,
   bakåtlänk, idempotens) och `origin`-data. Kan installeras så snart
   `quality_ce` och `mgmtsystem_nonconformity` finns.
2. **Fas 2 — klausulkopplingen** läggs till när `iso-common-core` är
   implementerad (`mgmtsystem.iso.clause` finns).
3. **Ingen datamigrering** — ändringen är additiv. Befintliga kontroller och
   alerts påverkas inte; de får bara en ny, tom bakåtlänk.

**Rollback:** avinstallera bryggmodulen. Inga befintliga modellers data ändras,
så rollback är riskfri. Nonconformitys som redan skapats via bryggan ligger
kvar i ledningssystemet (de är riktiga avvikelser).

## Open Questions

- Ska åtgärden finnas både på kontrollen och på alerten, eller räcker det med
  alerten (eftersom en kontroll som underkänns ofta redan har en alert)? Kan
  avgöras vid implementation utan att ändra modellerna.
- Ska den skapade nonconformityn kopplas till ett `mgmtsystem.system`
  (system_id) per automatik, eller lämnas tomt? Beror på om kunden kör flera
  ledningssystem parallellt — kan avgöras senare.
