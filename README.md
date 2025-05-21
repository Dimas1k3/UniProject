# 🛡️ Fokusa palīgs

## Projekta uzdevums

**Fokusa palīgs** ir vienkārša darbvirsmas lietotne, kas palīdz uzlabot lietotāja produktivitāti, bloķējot traucējošas vietnes un lietotnes, kā arī ļauj organizēt uzdevumus. Galvenās funkcijas:

- Pārvaldīt traucējošās vietnes un lietotnes;
- Bloķēt tās uz noteiktu brīdi (`hosts` faila modifikācija vai procesu apturēšana);
- Izveidot un pārvaldīt uzdevumu sarakstu (to-do list);
- Atjaunot un redzēt statusus (aktīvs/pabeigts/bloķēts).

---

## Izmantotās Python bibliotēkas

| Bibliotēka       | Iemesls izmantošanai                                  |
|------------------|--------------------------------------------------------|
| `sqlite3`        | Lokālās SQL datubāzes izveide uzdevumu, vietņu un lietotņu glabāšanai |
| `datetime`       | Datumu un laika reģistrēšana pievienošanai un bloķēšanai |
| `webview`        | Lietotāja saskarne kā pārlūka logs, kas sasaistīts ar Python backend |
| `psutil`         | Sistēmas procesu pārvaldīšanai (piem., pārlūkprogrammu apturēšanai) |
| `os`, `platform`, `subprocess` | Operētājsistēmas funkciju izsaukšanai (`hosts` faila pieeja, procesu vadība) |

---

## Datu struktūras

Projekta laikā tika definētas sekojošas SQL datu struktūras:

### Tabula `tasks` (uzdevumi)
- `id` (INTEGER)
- `title` (TEXT)
- `is_done` (BOOLEAN)
- `created_at`, `completed_at` (TEXT)

### Tabulas `sites` un `apps` (vietnes un lietotnes)
- `id` (INTEGER)
- `url` / `name` (TEXT)
- `is_active` (BOOLEAN)
- `created_at`, `last_blocked` (TEXT)
- `total_blocks` (INTEGER)

Papildu Python pusē tiek izmantotas vārdnīcas (`dict`), kuras tiek pārsūtītas starp frontend un backend izmantojot `pywebview`.

---

## Lietošanas instrukcija

### Prasības:
- Python 3.x
- Instalētas bibliotēkas: `psutil`, `pywebview`

### Instalēšana:
```bash
pip install psutil pywebview
```

### Palaišana:
```bash
cd uniproject
python main.py
```

### Funkcionalitāte:
- Atveras GUI logs ar tīmekļa saskarni;
- Iespējams pievienot vietnes, lietotnes un uzdevumus;
- Atzīmēt kā bloķētas/izpildītas;
- Izmantot pogas vietņu bloķēšanai un pārlūkprogrammu apturēšanai;
- Sistēma bloķē piekļuvi, modificējot `hosts` failu vai apturot procesus.

---

### ⚠️ Piezīmes

- Vietņu bloķēšana darbojas tikai ar administratora piekļuvi (`hosts` fails).
- Sistēmas specifiskā funkcionalitāte ir atkarīga no OS (`Windows`, `Mac`).
