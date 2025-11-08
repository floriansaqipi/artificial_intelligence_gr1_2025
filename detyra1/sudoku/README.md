# artificial_intelligence_gr1_2025

## Sudoku:

- ### Modelimi i Problemit:

Le të jetë $M$ një matricë $9 × 9$. Sudoku quhet e vlefshme nëse plotësohen kushtet në vijim:

1. Të gjithë elementet $m(i,j)$ janë elemente të domenit $D$, ku $D$ është nënbashkësi e numrave natyral me vlerat nga $1$ deri në $9$, pra, $D = {1, 2, ..., 9}$.
2. Të gjithë elementet $m(i,j1)$ të matricës $M$ janë të ndryshme nga elementet $m(i,j2)$ për $j1$ dhe $j2$ të ndryshme. Pra, elementet janë unik në rresht.
3. Të gjithë elementet $m(i1,j)$ të matricës $M$ janë të ndryshme nga elementet $m(i2,j)$ për $i1$ dhe $i2$ të ndryshme. Pra, elementet janë unik në kolonë.
4. Të gjitha blloqet $B(p,q)$ të matricës $M$ kanë numra unikë në qelitë e tyre.

Matematikisht:
1. $m(i,j) ∈ D, D = {1, 2, ..., 9}$ 
2. $∀i∈{0, 1, ..., 8}, ∀j1​,j2​ ∈ {0, 1, ..., 8}, j1≠j2 ​⇒ m(i,j1​)≠m(i,j2​)$
3. $∀j∈{0, 1, ..., 8}, ∀i1​,i2​ ∈ {0, 1, ..., 8}, i1≠i2 ​⇒ m(i1,j​)≠m(i2,j​)$
4. $B(p,q) = {m(i,j) | 3p ≤ i ≤ 3p+2, 3q ≤ j ≤ 3q+2}, p,q ∈ {0, 1, 2}
    $∀(i1,j1), (i2, j2) ∈ B(p,q), (i1,j1)≠(i2,j2) ​⇒ b(i1,j1)≠b(i2,j2)$

Pra:
- $M(9) = m(i,j) | m(i,j) ∈ D ∧ m(i,j1​)≠m(i,j2​) ∧ m(i1​,j)≠m(i2​,j) ∧ m(i1​,j1​)≠m(i2​,j2​), ∀ i,i1​,i2​, j,j1​,j2​ ∈ {1,...,9}$

- ### Reprezentimi i Problemit:

1. Variablat:
- Në këtë kontekst matematikor; çdo qeli e zbrazët e katrorit 9x9 quhet variabël.

2. Domeni i Problemit:
- Domeni tregon vlerat që mund të marrin variablat, pra numrat e plotë(natyral) nga 1 deri në 9

- ### Implementimi në python me Breadth First Search (BFS) dhe Backtracking:
- Është në fajllin ```sudoku_board.py``` të folderit ```sudoku``` në root të projektit.

#### Ekzekutimi:
##### Në Linux/MacOS apo shumë plotforma tjera të bazuara ne UNIX:
Në terminalin tuaj, nga ky direktorium, ekzekutoni:
```bash
./sudoku/sudoku_board.py
```
##### Në Windows:
Në terminalin tuaj, nga ky direktorium, ekzekutoni:
```powershell
python .\sudoku\sudoku_board.py
```