# artificial_intelligence_gr1_2025

## Latin Square:

- ### Modelimi i Problemit:

Le të jetë $$$n$$$ një numër i plotë dhe $$$L$$$ një matricë $$$n x n$$$. L themi se është katror latin atëherë dhe vetëm atëherë kur plotësohen kushtet në vijim:

1. Të gjitha elementet $$$l(i,j)$$$ të matricës $$$L$$$ janë elemente të domenit $$$D$$$. Ku $$$D$$$ është nënbashkësi e numrave natyral me vlerat nga $$$1$$$ deri tek $$$n$$$, pra, $$$D = {1, ..., n}$$$.
2. Të gjitha elementet $$$l(i,j1)$$$ të matricës $$$L$$$ janë të ndryshme nga elementet $$$l(i,j2)$$$ për j1 dhe j2 të ndryshme dhe elementet të domenit D, pra, janë në të njejtin rresht.
2. Të gjitha elementet $$$l(i1,j)$$$ të matricës $$$L$$$ janë të ndryshme nga elementet $$$l(i2,j)$$$ për i1 dhe i2 të ndryshme dhe elementet të domenit D, pra, janë në të njejtën kolonë.

Matematikisht:
1. $$$l(i,j) ∈ D, D = {1, ..., n}
2. $$$j1 != j2 -> l(i,j1) != l(i,j2) (∀i, j1, j2 ∈ D)$$$ 
3. $$$i1 != i2 -> l(i1,j) != l(i2,j) (∀i1, i2, j ∈ D)$$$ 

Pra:
- $$$L(n) = {l(i, j) | l(i, j) ∈ D ∧ l(i, j1) != l(i, j2) ∧ l(i1, j) != l(i2, j) (∀i, i1, i2, j, j1, j2 ∈ D) <=> D = {1, ..., n}}$$$

- ### Reprezentimi i Problemit:

1. Variablat:
- Në këtë kontekst matematikor; çdo qelizë e katrorit latin quhet variablël.

!!! kqyre & ni her qita !!!
2. Domeni i Problemit:
- Domeni tregon vlerat që mund të marrin variablat, pra numrat e plotë(natyral) nga 1 deri në n

- ### Implementimi në python me Iterative Deepening Depth-First Search (IDDFS):
- Është në fajllin ```main.py``` të folderit ```latin-square``` në root të projektit.

#### Ekzekutimi:
##### Në Linux/MacOS apo shumë plotforma tjera të bazuara ne UNIX:
Në terminalin tuaj, nga ky direktorium, ekzekutoni:
```bash
./latin-square/main.py
```
##### Në Windows:
Në terminalin tuaj, nga ky direktorium, ekzekutoni:
```powershell
python .\latin-square\main.py
```