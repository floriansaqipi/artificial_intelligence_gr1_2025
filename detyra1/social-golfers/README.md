# Write an SGP README in Markdown using $...$ LaTeX-style math (GitHub-compatible) and save it for download
content = r"""# Social Golfer Problem (SGP)

## Modelimi i Problemit

Le të jenë:
- $G$ — numri i grupeve çdo javë  
- $S$ — madhësia e grupit (lojtarë për grup)  
- $W$ — numri i javëve  
- $N = G \cdot S$ — numri i përgjithshëm i lojtarëve  
- $D = \{1, 2, \dots, N\}$ — domeni i identifikuesve të lojtarëve

Ndërtojmë një planifikim $L$ si një strukturë tridimensionale me përmasa $(W \times G \times S)$,
ku $L(w, g, s)$ tregon lojtarin (nga $D$) i cili luan në ulësen $s$ të grupit $g$ në javën $w$.

### Kufizimet e Problemit

1. **Domeni i vlerave:**
   $$
   L(w,g,s) \in D, \quad D = \{1, 2, \dots, N\}
   $$

2. **Saktësisht një herë për javë (ndarje/particion i $D$ në çdo javë):**
   $$
   \forall\, w \in \{1,\dots,W\},\ \forall\, i \in D:\ \exists!\ g \in \{1,\dots,G\},\ \exists!\ s \in \{1,\dots,S\}:\ L(w,g,s)=i
   $$

3. **Dallueshmëria e lojtarëve brenda grupit:**
   $$
   \forall\, w,g,\ \forall\, s_1 \neq s_2:\ L(w,g,s_1) \neq L(w,g,s_2)
   $$

4. **Kufizimi i çifteve (pairwise):**
   $$
   \forall\, i \neq j \in D:\ \left| \left\{ (w,g)\ \middle|\ \exists\, s_1 \neq s_2:\ L(w,g,s_1)=i \land L(w,g,s_2)=j \right\} \right| \le 1
   $$

---

## Reprezentimi i Problemit

1. **Variablat:**  
   Çdo element $L(w,g,s)$ është një variabël që tregon se cili lojtar ndodhet në atë pozitë.

2. **Domeni:**  
   $D = \{1, 2, \dots, N\}$ — numrat që identifikojnë lojtarët.

3. **Kufizimet funksionale:**  
   - Secili lojtar shfaqet një herë për javë.  
   - Të gjithë lojtarët në një grup janë të ndryshëm.  
   - Çdo çift lojtarësh luan bashkë maksimum një herë gjatë gjithë planifikimit.

---

- ### Implementimi në python me Depth-First Search (DFS) depth limited:
- Varianti me symmetry breaking është në fajllin `social_golfer_symmetry_breaking.py` të folderit `social-golfers` në root të projektit.

- Varianti me forward checking është në fajllin `social_golfer_forward_checking.py` të folderit `social-golfers` në root të projektit.

#### Ekzekutimi:
##### Në Linux/MacOS apo shumë platforma të bazuara në UNIX:
Në terminalin tuaj, nga ky direktorium, ekzekutoni:
```bash
./social-golfers/social_golfer_symmetry_breaking.py
./social-golfers/social_golfer_forward_checking.py
```

##### Në Windows:
Në terminalin tuaj, nga ky direktorium, ekzekutoni:
```powershell
python .\social-golfers\social_golfer_symmetry_breaking.py
python .\social-golfers\social_golfer_forward_checking.py
```