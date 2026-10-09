# Quality ↔ Management System Nonconformity Bridge

Brygga mellan kvalitetskontroller (`quality_ce` / `quality_control_ce`) och
ledningssystemets avvikelsehantering (`mgmtsystem_nonconformity`).

## Vad modulen gör

- **Kontrollpunkt → ISO-klausul.** `quality.point` får ett M2M till
  `mgmtsystem.iso.clause`, så att det framgår vilken klausul som kräver
  kontrollen. Vid en revision går det då att visa *varför* kontrollen finns.
- **Underkänd kontroll → avvikelse.** En knapp på `quality.check` (och på
  `quality.alert`) skapar en `mgmtsystem.nonconformity` med ett klick.
- **Bakåtlänk åt båda hållen.** Avvikelsen pekar tillbaka via
  `res_model`/`res_id` (OCA:s befintliga generiska fält) och kontrollen/alerten
  pekar på avvikelsen via `nonconformity_id`.
- **Idempotens.** Finns redan en avvikelse öppnas den i stället för att en ny
  skapas. Högst en avvikelse per kontroll eller alert.

## Avsiktliga designval

### Åtgärden är manuell

Ingen automatisk hook på `do_fail()`. Inte varje underkänd kontroll är en
ledningssystemsavvikelse — en omkontroll kan räcka. Automatik skulle fylla
ledningssystemet med brus och urholka nonconformity-begreppet. Användaren
avgör.

### Rotorsak kopieras inte

`quality.alert` har `reason_id` (Root Cause) medan `mgmtsystem.nonconformity`
har `cause_ids`. De är **två olika taxonomier** — att kopiera den ena till den
andra skulle tyst skapa fel data. Rotorsaken lämnas att fylla i
ledningssystemet, där rotorsaksanalysen hör hemma.

### Obligatoriska fält härleds

`mgmtsystem.nonconformity` har fem `required=True`-fält, varav fyra saknar
default. Bryggan sätter alla:

| Fält | Härleds ur |
|---|---|
| `partner_id` | kontrollens partner → företagets partner → användarens partner |
| `responsible_user_id` | kontrollens ansvarige → `env.user` |
| `manager_user_id` | ansvariges `hr.employee` → `parent_id` (chef) → chefens användare; annars ansvarige |
| `origin_ids` | den återanvändbara orsaken "Kvalitetskontroll" (`ref_code` `quality_check`) |
| `description` | sammanställs ur kontrollen |

Avvikelsen blockeras aldrig av saknad data — den som skapar avvikelsen blir
ansvarig i sista hand.

## Beroenden

`quality_control_ce` (äger check-/alert-formulären som utökas),
`mgmtsystem_nonconformity`, `mgmtsystem_iso_base` (för klausulmodellen) och
`hr` (för chefshärledningen — inget i mgmtsystem-kedjan drar in `hr`).

## Vad modulen INTE gör

- Slår inte ihop `quality.alert` och `mgmtsystem.nonconformity` — de har olika
  hemvist (golv respektive ledningssystem). Bryggan förenar dem.
- Helpdesk-koppling (avvikelse → ärende) ligger i en egen uppföljande change.
- Ändrar inte `quality_ce`s egna flöden (karantän, skrotning).
