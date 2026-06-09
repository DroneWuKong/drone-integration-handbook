# Chapter 24: MAVLink Military Dialect — Gap Analysis and Proposed Extensions

> Auterion's `mavlink-military` dialect (the `military.xml` file,
> `Auterion/mavlink-military`) adds a fires/targeting layer on top
> of standard MAVLink. It covers Find, Target, and Assess well, but
> the authorize, engage, and guide middle of the kill chain is thin.
> This chapter documents what exists and what could be added — both
> for operational completeness and for Law-of-Armed-Conflict (LOAC)
> auditability.

This document is bilingual. The English version is first; the
Croatian mirror (**Hrvatska verzija**) follows below the divider.

---

## What the dialect contains today

The dialect includes `common.xml`, declares dialect version 0, and
places every message in the **53000–53010** ID range to avoid
collisions with the common set and other dialects.

### Messages

| ID | Name | Role |
|---|---|---|
| 53000 | `TARGET_SET_COORD` | Circular target area (centroid, radius, validity window) |
| 53001 | `TARGET_BOX_COORD` | Quadrilateral area, four WGS84 corners, clockwise |
| 53002 | `TARGET_COORD` | Single target: position, velocity, covariance, CEP, classification |
| 53003 | `FIRES` | Fire-mission order: impact coordinates, time, effector, expected CEP |
| 53004 | `SPLASH_CORRECTION` | Post-impact observation for accuracy correction |
| 53005 | `TARGET_HANDOVER` | Transfer of track responsibility (kinematics, class, media reference) |
| 53006 | `BATTLE_DAMAGE_ASSESSMENT` | Post-engagement destruction assessment with confidence |
| 53007 | `ESAD_STATE` | Electronic Safe and Arm Device telemetry |
| 53008 | `ESAD_ARMING` | ESAD arming command with challenge-hash authentication |
| 53009 | `RWS_POSE` | Remote Weapon System pose, velocity, mount offset, orientation |
| 53010 | `RWS_STATE` | Remote Weapon System operational and arming status |

### Enums

- `TARGET_CLASS` — main battle tank types 1–9, infantry fighting
  vehicle types 1–9, road/linear infrastructure (190), structure (200).
- `TARGET_FORCE` — Unknown (0), Neutral (10), Friendly (20),
  Foe (30), Extraterrestrial (250).
- `ESAD_ARMING_STATUS`, `ESAD_MUNITION_STATUS`, `ESAD_IGNITION_STATUS`,
  `ESAD_FAULT_FLAGS` (bitmask), `ESAD_ARMING_REQUEST`.
- `RWS_ARMING_STATE`.
- `MATCH_MEDIA_TYPE` — None, still image, video clip, infrared, SAR.

The through-line: the dialect models **information about targets**
well but is thin on **authority to act** and **ability to stop** —
the part that matters most for autonomous and semi-autonomous fires.

---

## Proposed additions

The proposals below are grouped by priority. Suggested IDs continue
the existing scheme from 53011 upward; treat them as illustrative,
not final. New fields on existing messages should use MAVLink
`<extensions>` blocks so the wire format stays backward-compatible.

### 1. Close the engagement-authority loop (highest priority)

`FIRES` is an order and `ESAD_ARMING` arms the device, but there is
no model for weapons-release authority and, critically, **no way to
stop**. This is both an operational gap and a LOAC gap.

| Proposed | ID | Purpose |
|---|---|---|
| `WEAPONS_RELEASE_CONSENT` | 53011 | Human authorization to engage, with operator ID and authority token. Separates "I have a firing solution" from "you may fire." |
| `ABORT_ENGAGEMENT` | 53012 | In-flight wave-off / abort. The single most important safety message for loitering munitions. |
| `CHECK_FIRE` / `CEASE_FIRE` | 53013 | Temporary hold and full stop of fires. |
| `ENGAGEMENT_AUTONOMY_STATE` | 53014 | Declares human-in-the-loop, human-on-the-loop, or autonomous. Auditable; increasingly a procurement and legal requirement. |
| `ROE_STATE` | 53015 | Current rules of engagement, so a platform can refuse a `FIRES` order that violates them. |

### 2. Loitering-munition in-flight state

The dominant drone-fires use case is the loitering munition, yet
there is no in-flight munition telemetry.

- `MUNITION_FLIGHT_STATE` (53016) — terminal-lock status, seeker
  track quality, time-to-impact, abort-capable flag. Pairs with
  `ABORT_ENGAGEMENT` to give real wave-off capability.

### 3. Terminal guidance and laser designation

`MATCH_MEDIA_TYPE` references imagery, but nothing supports active
guidance.

- `LASER_DESIGNATOR_STATE` (53017) — PRF code, designate start/stop.
- `LASER_SPOT_TRACK` (53018) — spot location and track quality.
  Laser-guided weapons are unusable without PRF-code coordination,
  and PRF deconfliction across multiple designators is a real
  fratricide source.

### 4. Deconfliction and fire-support coordination

`TARGET_FORCE` has a "Friendly" value but no mechanism to avoid
hitting friendlies.

- `NO_FIRE_AREA` / `RESTRICTED_FIRE_AREA` (53019) — geofenced fire
  support coordination measures, so a platform can self-reject a
  solution that lands in a no-fire zone.
- Blue-force position should be delegated to ADS-B or TAK/CoT rather
  than duplicated here; document that boundary explicitly.

### 5. Stores and weapon inventory

`RWS_STATE` carries a weapon description but no consumables.

- `WEAPON_INVENTORY` / `STORES_MANAGEMENT` (53020) — munition types
  carried, rounds or stations remaining, per-weapon built-in-test
  (BIT) status, modeled on MIL-STD-1760. Required for weapon-target
  allocation.

### 6. Target-list and priority management

Single-target messages exist, but no prioritized list.

- `TARGET_LIST` (53021) — precedence, time-sensitive-target (TST)
  flags, track staleness and confidence age. Enables weapon-target
  pairing.

### 7. Schema quality and interoperability

These improve the existing messages rather than adding new ones.

- **`TARGET_CLASS` is ad-hoc.** "Tank type 7" means nothing to
  another vendor. Map it to MIL-STD-2525 / NATO APP-6 symbol
  identification codes.
- **Coordinate and datum rigor.** Be explicit about the altitude
  reference (height above ellipsoid vs mean sea level / geoid) and
  add vertical error alongside the existing CEP.
- **Forward compatibility.** Use `<extensions>` blocks so fields can
  be added without breaking the wire format. This matters at dialect
  version 0, where churn is expected.
- **Stronger authentication.** `ESAD_ARMING` uses one challenge hash.
  A coherent scheme (nonce, replay protection, command-authority
  token, layered on MAVLink 2 signing) should apply to all release
  and arming messages.
- **NATO mapping.** A crosswalk to STANAG 4586 (UAV control) and
  Link-16 J-series fires semantics would ease adoption.

### 8. Governance

- The README is empty and there is no scope statement, ID-range
  policy, or conformance tests. At dialect version 0 with open pull
  requests, documenting "53000–53099 = fires/targeting, what is
  reserved, contribution rules" prevents ID collisions and
  unproductive debate later.

---

## Summary table

| Area | Status today | Proposed |
|---|---|---|
| Find / Fix / Track | Covered | — |
| Target classification | Ad-hoc enum | Map to MIL-STD-2525 |
| Fire order | `FIRES` | — |
| Release authority | Missing | `WEAPONS_RELEASE_CONSENT` |
| Abort / stop | Missing | `ABORT_ENGAGEMENT`, `CHECK_FIRE` |
| Autonomy declaration | Missing | `ENGAGEMENT_AUTONOMY_STATE` |
| Loitering munition state | Missing | `MUNITION_FLIGHT_STATE` |
| Laser guidance | Missing | `LASER_DESIGNATOR_STATE` |
| Fratricide avoidance | Partial enum | `NO_FIRE_AREA`, BFT via TAK |
| Weapon inventory | Description only | `WEAPON_INVENTORY` |
| Target prioritization | Missing | `TARGET_LIST` |
| Authentication | One hash | Full signing scheme |
| Governance / docs | Empty README | Scope and ID policy |

---
---

# Hrvatska verzija

# Poglavlje 24: MAVLink vojni dijalekt — analiza nedostataka i prijedlozi proširenja

> Auterionov dijalekt `mavlink-military` (datoteka `military.xml`,
> `Auterion/mavlink-military`) dodaje sloj za ciljanje i vatru povrh
> standardnog MAVLinka. Dobro pokriva faze pronalaska, ciljanja i
> procjene, ali srednji dio lanca uništenja — odobravanje, gađanje i
> navođenje — slabo je razrađen. Ovo poglavlje dokumentira što
> postoji i što bi se moglo dodati, kako radi operativne potpunosti
> tako i radi sljedivosti prema Ratnom pravu (LOAC).

Ovaj je dokument dvojezičan. Engleska verzija je gore; hrvatski
prijevod slijedi ispod.

---

## Što dijalekt sadrži danas

Dijalekt uključuje `common.xml`, deklarira verziju dijalekta 0 i
smješta sve poruke u raspon identifikatora **53000–53010** kako bi se
izbjegli sudari sa zajedničkim skupom i drugim dijalektima.

### Poruke

| ID | Naziv | Uloga |
|---|---|---|
| 53000 | `TARGET_SET_COORD` | Kružno ciljno područje (središte, polumjer, prozor valjanosti) |
| 53001 | `TARGET_BOX_COORD` | Četverokutno područje, četiri WGS84 vrha, u smjeru kazaljke |
| 53002 | `TARGET_COORD` | Pojedinačni cilj: položaj, brzina, kovarijanca, CEP, klasifikacija |
| 53003 | `FIRES` | Nalog za vatru: koordinate udara, vrijeme, sredstvo, očekivani CEP |
| 53004 | `SPLASH_CORRECTION` | Promatranje nakon udara za korekciju točnosti |
| 53005 | `TARGET_HANDOVER` | Prijenos odgovornosti za praćenje (kinematika, klasa, referenca medija) |
| 53006 | `BATTLE_DAMAGE_ASSESSMENT` | Procjena uništenja nakon djelovanja s razinom pouzdanosti |
| 53007 | `ESAD_STATE` | Telemetrija elektroničkog uređaja za osiguranje i aktiviranje |
| 53008 | `ESAD_ARMING` | Naredba za aktiviranje ESAD-a s autentikacijom putem izazovnog sažetka |
| 53009 | `RWS_POSE` | Položaj, brzina, pomak nosača i orijentacija daljinski upravljanog oružja |
| 53010 | `RWS_STATE` | Operativni status i status aktiviranja daljinski upravljanog oružja |

### Enumeracije

- `TARGET_CLASS` — glavni borbeni tenkovi tipa 1–9, borbena vozila
  pješaštva tipa 1–9, cestovna/linijska infrastruktura (190),
  građevina (200).
- `TARGET_FORCE` — Nepoznato (0), Neutralno (10), Prijateljsko (20),
  Neprijateljsko (30), Izvanzemaljsko (250).
- `ESAD_ARMING_STATUS`, `ESAD_MUNITION_STATUS`, `ESAD_IGNITION_STATUS`,
  `ESAD_FAULT_FLAGS` (bitovna maska), `ESAD_ARMING_REQUEST`.
- `RWS_ARMING_STATE`.
- `MATCH_MEDIA_TYPE` — ništa, fotografija, videoisječak, infracrveno,
  SAR.

Glavna nit: dijalekt dobro modelira **informacije o ciljevima**, ali
slabo **ovlast za djelovanje** i **mogućnost zaustavljanja** — dio
koji je najvažniji za autonomnu i poluautonomnu vatru.

---

## Predložena proširenja

Prijedlozi su grupirani po prioritetu. Predloženi identifikatori
nastavljaju postojeću shemu od 53011 naviše; uzmite ih kao
ilustrativne, ne konačne. Nova polja na postojećim porukama trebaju
koristiti MAVLink blokove `<extensions>` kako bi format na žici ostao
unatrag kompatibilan.

### 1. Zatvaranje petlje ovlasti za gađanje (najviši prioritet)

`FIRES` je nalog, a `ESAD_ARMING` aktivira uređaj, ali ne postoji
model ovlasti za otpuštanje oružja i, što je presudno, **nema načina
za zaustavljanje**. To je i operativni i LOAC nedostatak.

| Predloženo | ID | Svrha |
|---|---|---|
| `WEAPONS_RELEASE_CONSENT` | 53011 | Ljudsko odobrenje za gađanje, s identifikatorom operatera i tokenom ovlasti. Razdvaja "imam rješenje za gađanje" od "smijete pucati". |
| `ABORT_ENGAGEMENT` | 53012 | Prekid u letu. Najvažnija sigurnosna poruka za lutajuća ubojna sredstva. |
| `CHECK_FIRE` / `CEASE_FIRE` | 53013 | Privremeni zastoj i potpuni prestanak vatre. |
| `ENGAGEMENT_AUTONOMY_STATE` | 53014 | Deklarira čovjeka u petlji, čovjeka nad petljom ili autonomiju. Sljedivo; sve češći zahtjev nabave i prava. |
| `ROE_STATE` | 53015 | Trenutna pravila gađanja, kako bi platforma mogla odbiti nalog `FIRES` koji ih krši. |

### 2. Stanje lutajućeg ubojnog sredstva u letu

Dominantna uporaba dronske vatre je lutajuće ubojno sredstvo, no ne
postoji telemetrija sredstva u letu.

- `MUNITION_FLIGHT_STATE` (53016) — status završnog zaključavanja,
  kvaliteta praćenja tragača, vrijeme do udara, oznaka mogućnosti
  prekida. Uparuje se s `ABORT_ENGAGEMENT` za stvarnu mogućnost
  odustajanja.

### 3. Završno navođenje i lasersko označavanje

`MATCH_MEDIA_TYPE` upućuje na snimke, ali ništa ne podržava aktivno
navođenje.

- `LASER_DESIGNATOR_STATE` (53017) — PRF kod, početak/kraj
  označavanja.
- `LASER_SPOT_TRACK` (53018) — položaj točke i kvaliteta praćenja.
  Laserski navođeno oružje neupotrebljivo je bez usklađivanja PRF
  koda, a deklonfliktacija PRF-a između više označivača stvaran je
  izvor bratoubilačke vatre.

### 4. Deklonfliktacija i koordinacija vatrene potpore

`TARGET_FORCE` ima vrijednost "Prijateljsko", ali nema mehanizam za
izbjegavanje pogađanja vlastitih snaga.

- `NO_FIRE_AREA` / `RESTRICTED_FIRE_AREA` (53019) — geografski
  ograničene mjere koordinacije vatrene potpore, kako bi platforma
  sama odbila rješenje koje pada u zonu zabrane vatre.
- Položaj vlastitih snaga treba delegirati na ADS-B ili TAK/CoT umjesto
  dupliciranja ovdje; tu granicu treba izričito dokumentirati.

### 5. Inventar oružja i ubojnih sredstava

`RWS_STATE` nosi opis oružja, ali ne i potrošni materijal.

- `WEAPON_INVENTORY` / `STORES_MANAGEMENT` (53020) — vrste nošenih
  sredstava, preostali broj zrna ili nosača, status ugrađenog
  samotestiranja (BIT) po oružju, po uzoru na MIL-STD-1760. Potrebno
  za raspodjelu oružja na ciljeve.

### 6. Popis ciljeva i upravljanje prioritetima

Postoje poruke za pojedinačne ciljeve, ali ne i prioritizirani popis.

- `TARGET_LIST` (53021) — prednost, oznake vremenski osjetljivih
  ciljeva (TST), starost traga i pouzdanosti. Omogućuje uparivanje
  oružja i cilja.

### 7. Kvaliteta sheme i interoperabilnost

Ovo poboljšava postojeće poruke umjesto dodavanja novih.

- **`TARGET_CLASS` je proizvoljan.** "Tenk tipa 7" ne znači ništa
  drugom proizvođaču. Preslikati ga na identifikacijske kodove
  simbola MIL-STD-2525 / NATO APP-6.
- **Strogost koordinata i datuma.** Biti izričit o referenci visine
  (visina iznad elipsoida naspram srednje razine mora / geoida) i
  dodati vertikalnu pogrešku uz postojeći CEP.
- **Kompatibilnost prema naprijed.** Koristiti blokove `<extensions>`
  kako bi se polja mogla dodavati bez narušavanja formata na žici. To
  je važno pri verziji dijalekta 0, gdje su promjene očekivane.
- **Jača autentikacija.** `ESAD_ARMING` koristi jedan izazovni
  sažetak. Cjelovita shema (nonce, zaštita od ponavljanja, token
  ovlasti naredbe, povrh MAVLink 2 potpisivanja) treba se primijeniti
  na sve poruke otpuštanja i aktiviranja.
- **NATO preslikavanje.** Poveznica na STANAG 4586 (upravljanje
  bespilotnim letjelicama) i semantiku vatre Link-16 J-serije
  olakšala bi usvajanje.

### 8. Upravljanje projektom

- README je prazan i ne postoji izjava o opsegu, politika raspona
  identifikatora ni testovi sukladnosti. Pri verziji dijalekta 0 s
  otvorenim zahtjevima za povlačenje, dokumentiranje "53000–53099 =
  vatra/ciljanje, što je rezervirano, pravila doprinosa" sprječava
  buduće sudare identifikatora i neproduktivne rasprave.

---

## Sažeta tablica

| Područje | Stanje danas | Predloženo |
|---|---|---|
| Pronalazak / fiksiranje / praćenje | Pokriveno | — |
| Klasifikacija cilja | Proizvoljna enumeracija | Preslikati na MIL-STD-2525 |
| Nalog za vatru | `FIRES` | — |
| Ovlast otpuštanja | Nedostaje | `WEAPONS_RELEASE_CONSENT` |
| Prekid / zaustavljanje | Nedostaje | `ABORT_ENGAGEMENT`, `CHECK_FIRE` |
| Deklaracija autonomije | Nedostaje | `ENGAGEMENT_AUTONOMY_STATE` |
| Stanje lutajućeg sredstva | Nedostaje | `MUNITION_FLIGHT_STATE` |
| Lasersko navođenje | Nedostaje | `LASER_DESIGNATOR_STATE` |
| Izbjegavanje bratoubilačke vatre | Djelomična enumeracija | `NO_FIRE_AREA`, BFT putem TAK-a |
| Inventar oružja | Samo opis | `WEAPON_INVENTORY` |
| Prioritizacija ciljeva | Nedostaje | `TARGET_LIST` |
| Autentikacija | Jedan sažetak | Cjelovita shema potpisivanja |
| Upravljanje / dokumentacija | Prazan README | Opseg i politika identifikatora |
