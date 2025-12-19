<table border="0">
 <tr>
    <td>
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/University_of_Prishtina_logo.svg/1200px-University_of_Prishtina_logo.svg.png"
           width="150" alt="University Logo" />
    </td>
    <td>
      <p>Universiteti i Prishtinës</p>
      <p>Fakulteti i Inxhinierisë Elektrike dhe Kompjuterike</p>
      <p>Inxhinieri Kompjuterike dhe Softuerike - Programi Master</p>
      <p>Profesori: <b>Prof. Dr. Avni Rexhepi</b></p>
      <p>Asistenti i lëndës: <b>PhD C. Adrian Ymeri</b></p>
      <p>Lënda: <b>Inteligjenca Artificiale</b></p>
    </td>
 </tr>
</table>

# Artificial Intelligence — Assignments 2025/26

## Overview

Ky repository përmban punimet e lëndës **Inteligjenca Artificiale (Artificial Intelligence)** dhe është i organizuar në **tre detyra (assignments)**, ku secila detyrë fokusohet në një temë specifike të IA.

**Përmbledhje e detyrave:**

- **Detyra 1 — Uninformed Search Techniques**
  - Latin Square Problem
  - Sudoku Problem
  - Social Golfer Problem

- **Detyra 2 — Advanced Search & SAT**
  - Blocked N-Queens Problem
  - Guest Seating Problem as SAT
  - Killer Sudoku Variant Problem

- **Detyra 3 — Adversarial Search**
  - Chess: Minimax Algorithm + Alpha-Beta Pruning

Çdo problem është implementuar në **Python**, dhe secili ka folder-in e vet me:
- skripte ekzekutuese
- dhe një **README.md** të veçantë me dokumentim të plotë për atë problem.

---

## Technical Details

### Konceptet kryesore të mbuluara

**Detyra 1 (Uninformed search)**
- Modelimi i hapësirës së gjendjeve (state-space): state, action, transition
- Strategji të kërkimit pa informim (p.sh. BFS/DFS/IDDFS – varësisht implementimit)
- Kontroll i kufizimeve (pruning/validim i gjendjeve)

**Detyra 2 (Blocked N-Queens, SAT, Killer Sudoku)**
- Kërkim me kufizime dhe qeliza të bllokuara (Blocked N-Queens)
- SAT encoding: variabla, klauzola, CNF constraints (p.sh. exactly-one, at-most-k, pair constraints)
- Workflow SAT: encoding → solving → decoding (shndërrimi i zgjidhjes në format të kuptueshëm)

**Detyra 3 (Minimax në shah)**
- Game-tree search me minimax
- Alpha-beta pruning
- Heuristic evaluation (p.sh. material + elemente pozicionale, në formë të thjeshtuar)
- Depth limits + ekzekutim deterministik

---

## Repository Structure

Struktura është e ndarë sipas detyrave dhe problemeve:

```text
detyra1/
  latin_square/
    README.md
    ... (python scripts, inputs)
  sudoku/
    README.md
    ...
  social_golfer/
    README.md
    ...

detyra2/
  blocked_n_queens/
    README.md
    ...
  sat_guest_seating/
    README.md
    ...
  killer_sudoku_variant/
    README.md
    ...

detyra3/
  chess_minimax_alpha_beta/
    README.md
    ... (engine, evaluation, runner)
```

> Emrat e saktë të skripteve dhe komandat për ekzekutim dokumentohen brenda README.md të secilit problem.

---

## How to Run

### Requirements
- **Python 3.10+** (rekomandohet)
- `pip` dhe një virtual environment (`venv`)

### Setup (Recommended)

```bash
git clone <REPO_URL>
cd <REPO_FOLDER>

python -m venv .venv
```

### Run një problem specifik

Shkoni në folder-in e problemit dhe ndiqni README.md të atij folder-i. Shembull (pattern):


```bash
python <script_name>.py
```

---

## Documentation

- **README kryesor (ky file):** overview + navigim nëpër detyra.
- **README për secilin problem:** dokumentim (ku kërkohet) i detajuar (algoritme, formate input/output, shembuj ekzekutimi, etj.).
  - Dokumentimi gjendet brenda folderëve përkatës, p.sh.:
    - `detyra2/sat_guest_seating/README.md`
    - `detyra3/chess_minimax_alpha_beta/README.md`

---

## Contributors

- [Adonis Xhemajli](https://github.com/adonisthedev) 
- [Florian Saqipi](https://github.com/floriansaqipi) 
- [Gent Zhushi](https://github.com/gentzhushi)


---

## Acknowledgments

- **Profesori:** Adrian Ymeri — për udhëzimet dhe kriteret e vlerësimit të detyrave në lëndën **Inteligjenca Artificiale**
- Universiteti i Prishtinës — FIEK

---
