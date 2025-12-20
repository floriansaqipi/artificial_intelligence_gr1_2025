# Guest Seating Problem (SAT Encoding)

## Përshkrimi

Kemi **100 mysafirë** dhe **10 tavolina**, secila me **10 ulëse**. Qëllimi është të vendosen mysafirët në tavolina duke respektuar:

- çdo mysafir ulet **saktësisht në një tavolinë**;
- çdo tavolinë ka **saktësisht 10 mysafirë**;
- disa çifte mysafirësh **nuk guxojnë** të ulen në të njëjtën tavolinë (*not-together*);
- disa grupe mysafirësh **duhet** të ulen në të njëjtën tavolinë (*together*);
- **balanca e gjinisë**: ID-të **çift** janë meshkuj, ID-të **tek** janë femra, dhe për çdo tavolinë vlen  
  $|M - F| \le 3$. Me kapacitet 10, kjo lejon vetëm ndarjet: **4/6**, **5/5**, **6/4**. (ku **M** = numri i meshkujve në tavolinë, **F** = numri i femrave)

---

## Modelimi i problemit

Le të jenë:

- $N = 100$ — numri i mysafirëve  
- $T = 10$ — numri i tavolinave  
- $C = 10$ — kapaciteti i tavolinës  
- $D = \{1,2,\dots,N\}$ — domeni i mysafirëve  
- $K = \{1,2,\dots,T\}$ — domeni i tavolinave  

### Variablat (SAT)

Përdorim variabla booleane:

$$
x_{g,t} \in \{0,1\}
$$

ku:

- $x_{g,t}=1$ **nëse dhe vetëm nëse** mysafiri $g$ ulet në tavolinën $t$.

---

## Kufizimet (në formë matematikore)

### 1) Saktësisht një tavolinë për çdo mysafir

$$
\forall g \in D:\quad \sum_{t \in K} x_{g,t} = 1
$$

Kjo ndahet në dy pjesë:

- **AtLeastOne**: $\sum x_{g,t} \ge 1$
- **AtMostOne**: $\sum x_{g,t} \le 1$

---

### 2) Saktësisht 10 mysafirë për çdo tavolinë

$$
\forall t \in K:\quad \sum_{g \in D} x_{g,t} = C
$$

Shënim praktik: nëse $N = T\cdot C$ (këtu 100 = 10·10), atëherë shpesh mjafton të vendoset vetëm:

$$
\forall t:\ \sum_{g} x_{g,t} \le C
$$

sepse nga “çdo mysafir ulet diku” dalin pikërisht 100 vendosje totale, dhe “kapaciteti” e kufizon maksimumin total në 100 — kështu çdo tavolinë del automatikisht e mbushur me 10.

---

### 3) Çiftet që **nuk ulen bashkë** (*not-together*)

Le të jetë $NT$ bashkësia e çifteve $(a,b)$ që nuk mund të jenë në të njëjtën tavolinë.

$$
\forall (a,b) \in NT,\ \forall t \in K:\quad \neg(x_{a,t} \wedge x_{b,t})
$$

---

### 4) Grupet që **duhet të ulen bashkë** (*together*)

Le të jetë $TG$ lista e grupeve $S=(g_1,g_2,\dots,g_m)$ që duhet të jenë në të njëjtën tavolinë (p.sh. çift, treshe, etj.).

Një mënyrë e thjeshtë është të zgjedhim një **lider** $g_1$ dhe të imponojmë që çdo anëtar $g_i$ të ketë të njëjtin “rresht tavolinash”:

$$
\forall g_i \in S,\ \forall t \in K:\quad x_{g_1,t} \leftrightarrow x_{g_i,t}
$$

Kjo, e kombinuar me “saktësisht një tavolinë për mysafir”, e detyron grupin të përfundojë në **të njëjtën tavolinë**.

---

### 5) Balanca e gjinisë: $|M-F| \le 3$

Definojmë:

- $M_t = \sum_{g\ \text{çift}} x_{g,t}$ — meshkujt në tavolinën $t$
- $F_t = \sum_{g\ \text{tek}} x_{g,t}$ — femrat në tavolinën $t$

Kërkohet:

$$
\forall t:\quad |M_t - F_t| \le 3
$$

Me $C=10$, kjo është ekuivalente me:

$$
\forall t:\quad 4 \le M_t \le 6 \quad (dhe\ po ashtu\ 4 \le F_t \le 6)
$$

Një kodim i thjeshtë SAT është të vendosim kufijtë sipërorë:

$$
\forall t:\quad M_t \le 6 \ \wedge\  F_t \le 6
$$

Pse duhen **të dyja**? Sepse vetëm $M_t\le 6$ do lejonte $M_t=0, F_t=10$, që shkel $|M-F|\le 3$. Duke vendosur edhe $F_t\le 6$, ekstremet ndalohen dhe mbeten vetëm ndarjet 4/6, 5/5, 6/4.

Në përgjithësi, për kapacitet $C$ dhe diferencë $d$, kufiri sipëror del:

$$
\text{upper} = \left\lfloor \frac{C + d}{2} \right\rfloor
$$

---

## Përkthimi në CNF (Rregullat konkrete)

SAT solver-i nuk “kupton” direkt shumën $\sum$ apo shprehje si “saktësisht 10 në tavolinë”.  
Ai kërkon formulë në **CNF** (*Conjunctive Normal Form*): një **AND** i shumë klauzolave, ku çdo klauzolë është një **OR** i literalëve.

- **Literal**: një variabël booleane (p.sh. $x_{g,t}$) ose negimi i saj (p.sh. $\neg x_{g,t}$)
- **Klauzolë**: $(\ell_1 \vee \ell_2 \vee \cdots \vee \ell_k)$
- **CNF**: $(\text{klauzola}_1)\ \wedge\ (\text{klauzola}_2)\ \wedge\ \cdots$

$$
(\ell_{1,1}\vee \ell_{1,2}\vee\cdots)\ \wedge\ (\ell_{2,1}\vee\cdots)\ \wedge\ \cdots
$$

Në problemin tonë, variablat kryesore janë:

- $x_{g,t}$ : “mysafiri $g$ ulet në tavolinën $t$”.

Më poshtë janë **rregullat** (çfarë duam) dhe **klauzolat CNF** (si shkruhen në SAT).

---

### 1) “Çdo mysafir ulet në saktësisht një tavolinë”

Kjo do të thotë:

- **të paktën një** tavolinë (AtLeastOne)
- **jo më shumë se një** tavolinë (AtMostOne)

#### 1A) AtLeastOne për mysafirin $g$

$g$ duhet të jetë diku:

$$
x_{g,1} \vee x_{g,2} \vee \cdots \vee x_{g,10}
$$

Këtë klauzolë e vendosim për **çdo** $g \in \{1,\dots,100\}$.

#### 1B) AtMostOne për mysafirin $g$ (pairwise)

$g$ nuk mund të jetë në dy tavolina njëkohësisht.

Për çdo palë tavolinash $t_1 < t_2$:

$$
(\neg x_{g,t_1} \vee \neg x_{g,t_2})
$$

Kjo është e njëjtë me: $\neg(x_{g,t_1}\wedge x_{g,t_2})$.

**Sa klauzola dalin këtu?**  
Me 10 tavolina kemi $\binom{10}{2}=45$ palë, pra **45 klauzola për çdo mysafir** (dhe 4500 për 100 mysafirë).

> Pairwise është shumë i qartë për ta kuptuar.  
> Në implementime tjera, shpesh përdoret një encoding kardinaliteti (p.sh. sequential counter).

---

### 2) “Çdo tavolinë ka saktësisht 10 mysafirë”

Në formë matematikore:

$$
\forall t:\ \sum_{g=1}^{100} x_{g,t} = 10
$$

Në SAT zakonisht ndahet në:

- $\sum_g x_{g,t} \le 10$  (**AtMost10**)
- $\sum_g x_{g,t} \ge 10$  (**AtLeast10**)

#### 2A) AtMost10 për çdo tavolinë $t$

“Jo më shumë se 10 ulëse”:

$$
\sum_{g=1}^{100} x_{g,t} \le 10
$$

Kjo është **kufizim kardinaliteti** (shih pika 6 më poshtë).

#### 2B) Pse në projektin tënd mjafton vetëm AtMost10?

Sepse ke **pikërisht** 100 mysafirë dhe **pikërisht** 100 ulëse totale (10 tavolina × 10 ulëse).

- Rregulli 1 (ExactlyOne për mysafir) jep **100 vendosje** totale.
- AtMost10 për secilën tavolinë jep maksimum **100 vendosje** totale.

Pra nuk ka “hapësirë” për tavolinë bosh: automatikisht del **saktësisht 10** në secilën tavolinë.

> Nëse nuk do të ishte $N=T\cdot C$, atëherë do duhej edhe AtLeast10 (ose një mënyrë tjetër) që tavolinat të mbushen siç duhet.

---

### 3) “Çiftet (a,b) nuk ulen bashkë” (not-together)

Nëse $(a,b)$ është çift i ndaluar, atëherë për **çdo** tavolinë $t$:

$$
(\neg x_{a,t} \vee \neg x_{b,t})
$$

Kjo ndalon që të dy të jenë në të njëjtën tavolinë.

---

### 4) “Grupet duhet të ulen bashkë” (together)

P.sh. grupi $(10,11,12)$ do të thotë: ata duhet të jenë në **të njëjtën** tavolinë.

Mënyra e thjeshtë është “lideri”:

- zgjedhim $g_1$ si lider (i pari në tuple)
- për çdo anëtar $k$ tjetër, i bëjmë **ekuivalentë** në çdo tavolinë

Për çdo tavolinë $t$:

$$
x_{g_1,t} \leftrightarrow x_{k,t}
$$

dhe kjo në CNF bëhet me dy klauzola (dy implikime):

$$
(\neg x_{g_1,t} \vee x_{k,t})\ \wedge\ (\neg x_{k,t} \vee x_{g_1,t})
$$

**Pse kjo e detyron “bashkë”?**  
Sepse secili mysafir ka “ExactlyOne table”. Nëse lideri është në tavolinën 7, atëherë ekuivalenca i detyron të gjithë anëtarët të kenë $x_{k,7}=1$, dhe s’mund të jenë diku tjetër.

---

### 5) Balanca e gjinisë: “maksimumi 6 meshkuj” dhe “maksimumi 6 femra”

Le të kemi:

- Meshkuj = ID çift (2,4,6,...)  
- Femra = ID tek (1,3,5,...)

Për një tavolinë $t$ le të jetë:

- $M_t = \sum_{\text{even } g} x_{g,t}$
- $F_t = \sum_{\text{odd } g} x_{g,t}$

Kërkesa është:

$$
|M_t - F_t| \le 3
$$

Me kapacitet 10 kjo lejon vetëm: 4/6, 5/5, 6/4.  
Një kodim i thjeshtë SAT është të vendosim **kufirin sipëror** për të dyja:

$$
M_t \le 6\quad \wedge\quad F_t \le 6
$$

**Pse duhen të dyja?**  
Nëse do kishim vetëm $M_t \le 6$, atëherë $M_t=0, F_t=10$ do ishte ende i lejuar (por është gabim).  
Duke vendosur edhe $F_t \le 6$, ekstremet ndalohen.

Në përgjithësi (kapacitet $C$, diferencë $d$):

$$
\text{upper}=\left\lfloor\frac{C+d}{2}\right\rfloor
$$

p.sh. $C=10$, $d=3$ ⇒ upper = 6.

---

### 6) Çfarë do të thotë AtMostK në CNF?

Një kufizim i formës:

$$
\sum_{i=1}^{n} y_i \le K
$$

do të thotë: “maksimumi $K$ prej këtyre $n$ variablave mund të jenë true”.

- Kur $K=1$, mund ta bësh me **pairwise**: për çdo $i<j$, $(\neg y_i \vee \neg y_j)$.
- Por kur $n$ është i madh (p.sh. $n=100$ mysafirë për një tavolinë) dhe $K$ nuk është 1, pairwise bëhet gjigante.
  Prandaj përdoret një **encoding standard** që shton **variabla ndihmëse**.

Më poshtë po e shpjegojmë konkretisht një encoding shumë të përdorur: **Sequential Counter** (*Sinz encoding*).

---

#### 6A) Ideja e “Sequential Counter”

Merr $y_1, y_2, \dots, y_n$ dhe duam:

$$
y_1 + y_2 + \cdots + y_n \le K
$$

Shtojmë variabla ndihmëse:

$$
s_{i,j}\quad \text{për}\quad i=1..(n-1),\ j=1..K
$$

Intuita:

- $s_{i,j}=1$ do të thotë: “në mes të $y_1,\dots,y_i$ kemi **të paktën $j$** të vërteta”.

Pra këto $s$ janë si “memorie” e një numëruesi që ecën nga $y_1$ te $y_n$ dhe “mbron” që të mos kalohet $K$.

Pse vetëm deri në $n-1$?  
Sepse variabla e fundit $y_n$ kontrollohet me një klauzolë “overflow” (poshtë), dhe nuk na duhet rreshti i plotë $i=n$.

---

#### 6B) Klauzolat e Sequential Counter (strukturë)

Klauzolat vijnë në 4 “blloqe” logjike:

**(1) Nëse $y_i$ është true, atëherë kemi arritur të paktën 1 deri aty**

Për $i=1..(n-1)$:

$$
(\neg y_i \vee s_{i,1})
$$

**(2) “Të paktën 1” (dhe përgjithësisht “të paktën j”) përcillet përpara**

Për $i=2..(n-1)$ dhe $j=1..K$:

$$
(\neg s_{i-1,j} \vee s_{i,j})
$$

**(3) Nëse $y_i$ ndizet dhe më parë kemi pasur të paktën $(j-1)$, atëherë tani kemi të paktën $j$**

Për $i=2..(n-1)$ dhe $j=2..K$:

$$
(\neg y_i \vee \neg s_{i-1,j-1} \vee s_{i,j})
$$

**(4) Klauzola “overflow” që ndalon të kalojmë mbi $K$**

Për variablën e fundit $y_n$:

$$
(\neg y_n \vee \neg s_{n-1,K})
$$

Kjo thotë: nëse deri te $y_{n-1}$ tashmë kemi arritur “të paktën $K$”, atëherë $y_n$ **nuk guxon** të jetë true (ndryshe do bëhej $K+1$).

---

#### 6C) Shembull i vogël: AtMost3 mbi 5 variabla


Kërkesa:

$$
y_1+y_2+y_3+y_4+y_5 \le 3
$$

**Sequential Counter** shton variabla ndihmëse $s_{i,j}$ për $i=1..4$ dhe $j=1..3$, ku
$s_{i,j}=1$ do të thotë: “në $y_1..y_i$ ka **të paktën** $j$ të vërteta”.

Tani supozojmë një caktim që do ta shkelte AtMost3 (pra 4 të vërteta):

$$
y_1=1,\quad y_2=1,\quad y_4=1,\quad y_5=1
$$

Do të shohim si CNF e ndalon $y_5$.

---

#### Hapi 1 — nga $y_1$ marrim “të paktën 1” deri te $i=4$

Nga klauzola e tipit (1):

$$
(\neg y_1 \vee s_{1,1})
$$

me $y_1=1$ del:

$$
s_{1,1}=1
$$

Pastaj nga “propagate” (tipi (2)) për $j=1$:

$$
(\neg s_{1,1}\vee s_{2,1}),\ (\neg s_{2,1}\vee s_{3,1}),\ (\neg s_{3,1}\vee s_{4,1})
$$

del zinxhiri:

$$
s_{1,1}=1 \Rightarrow s_{2,1}=1 \Rightarrow s_{3,1}=1 \Rightarrow s_{4,1}=1
$$

---

#### Hapi 2 — nga $y_2$ arrijmë “të paktën 2” deri te $i=4$

Klauzola e “increment” (tipi (3)) për $i=2, j=2$:

$$
(\neg y_2 \vee \neg s_{1,1} \vee s_{2,2})
$$

me $y_2=1$ dhe $s_{1,1}=1$ del:

$$
s_{2,2}=1
$$

Pastaj “propagate” për $j=2$:

$$
(\neg s_{2,2}\vee s_{3,2}),\ (\neg s_{3,2}\vee s_{4,2})
$$

pra:

$$
s_{2,2}=1 \Rightarrow s_{3,2}=1 \Rightarrow s_{4,2}=1
$$

---

#### Hapi 3 — nga $y_4$ arrijmë “të paktën 3” te $i=4$

Klauzola e “increment” (tipi (3)) për $i=4, j=3$:

$$
(\neg y_4 \vee \neg s_{3,2} \vee s_{4,3})
$$

me $y_4=1$ dhe $s_{3,2}=1$ (nga Hapi 2) del:

$$
s_{4,3}=1
$$

Kjo do të thotë: në $y_1..y_4$ kemi tashmë **të paktën 3** të vërteta.

---

#### Hapi 4 — “overflow” e ndalon $y_5$

Klauzola e “overflow” (tipi (4)) është:

$$
(\neg y_5 \vee \neg s_{4,3})
$$

Meqë kemi $s_{4,3}=1$, kjo klauzolë bëhet:

$$
(\neg y_5 \vee \neg 1) \equiv (\neg y_5 \vee 0) \equiv \neg y_5
$$

Pra SAT-i detyron:

$$
y_5=0
$$

Por ne supozuam $y_5=1$, prandaj del **kontradiktë** ⇒ çdo caktim me 4 “true” **refuzohet**.

---

#### 6D) Lidhja me problemin tonë

Në problemin e mysafirëve, AtMostK përdoret në disa vende:

- **Kapaciteti i tavolinës**: për çdo tavolinë $t$,

$$
\sum_{g=1}^{100} x_{g,t} \le 10
$$

- **Balanca e gjinisë**: për çdo tavolinë $t$,

$$
\sum_{\text{even } g} x_{g,t} \le 6
\quad\text{dhe}\quad
\sum_{\text{odd } g} x_{g,t} \le 6
$$

Në implementim, biblioteka (p.sh. PySAT) gjeneron klauzolat e tipit “Sequential Counter” (ose encoding tjetër) automatikisht.

---


## Procesi i zgjidhjes

1. **Modelimi** i problemit me variablat $x_{g,t}$ dhe kufizimet e mësipërme.
2. **Gjenerimi i CNF** (klauzolat) + (opsionale) eksportimi në **DIMACS**.
3. **Ekzekutimi i SAT solver-it** për të gjetur një model (SAT) ose të provojë që është e pamundur (UNSAT).
4. **Dekodimi** i modelit: për çdo mysafir $g$, gjendet tavolina $t$ ku $x_{g,t}=1$.

---

## Shembull: Inputet e instancës + Zgjidhja konkrete (SAT)

### Inputet (përmbledhje)

| Elementi | Vlera |
|---|---|
| Guests / Tables / Capacity | **100** guests, **10** tables, **10** per table |
| Gender rule | even = male, odd = female |
| Gender constraint | $|M - F| \le 3$ (lejon vetëm 4/6, 5/5, 6/4) |
| not_together pairs | **24** pairs |
| together_groups | **7** groups |

### together_groups (ku përfunduan në zgjidhje)
- `(10, 11, 12)` → Table **6**
- `(30, 31, 32)` → Table **10**
- `(50, 51, 52)` → Table **2**
- `(70, 71, 72)` → Table **10**
- `(90, 91, 92)` → Table **3**
- `(3, 4)` → Table **5**
- `(25, 26)` → Table **6**

### not_together pairs (lista e plotë)

```text
(1,5)  (1,7)  (2,9)  (2,10)
(3,14)  (4,16)  (6,8)  (11,13)
(15,20)  (17,19)  (18,21)  (22,25)
(23,24)  (26,30)  (27,29)  (28,31)
(32,35)  (33,34)  (36,40)  (37,39)
(41,45)  (42,44)  (46,50)  (47,49)
```

---

### Zgjidhja SAT (matrix 10×10)

Rreshti = tavolina, kolonat = 10 vendet. (Numrat janë ID-të e mysafirëve.)

| Table | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | 36 | 46 | 47 | 48 | 55 | 57 | 62 | 64 | 77 | 94 |
| T2 | 19 | 50 | 51 | 52 | 65 | 69 | 79 | 84 | 86 | 100 |
| T3 | 17 | 41 | 42 | 54 | 60 | 61 | 81 | 90 | 91 | 92 |
| T4 | 1 | 40 | 44 | 49 | 56 | 58 | 74 | 75 | 85 | 87 |
| T5 | 3 | 4 | 6 | 7 | 9 | 13 | 18 | 20 | 33 | 37 |
| T6 | 5 | 10 | 11 | 12 | 23 | 25 | 26 | 68 | 76 | 78 |
| T7 | 2 | 22 | 24 | 28 | 29 | 34 | 45 | 93 | 95 | 97 |
| T8 | 8 | 14 | 16 | 21 | 38 | 53 | 63 | 82 | 83 | 89 |
| T9 | 27 | 35 | 43 | 59 | 66 | 80 | 88 | 96 | 98 | 99 |
| T10 | 15 | 30 | 31 | 32 | 39 | 67 | 70 | 71 | 72 | 73 |

**Gender check (per table):**

- Table 1: M=6, F=4, Δ=2
- Table 2: M=5, F=5, Δ=0
- Table 3: M=5, F=5, Δ=0
- Table 4: M=5, F=5, Δ=0
- Table 5: M=4, F=6, Δ=2
- Table 6: M=6, F=4, Δ=2
- Table 7: M=5, F=5, Δ=0
- Table 8: M=5, F=5, Δ=0
- Table 9: M=5, F=5, Δ=0
- Table 10: M=4, F=6, Δ=2


## Shënime për rastet UNSAT

- Nëse një grup “together” ka madhësi $>C$, problemi është **UNSAT**.
- Nëse futni një çift në të dyja listat (“together” dhe “not-together”), problemi bëhet **UNSAT**.
