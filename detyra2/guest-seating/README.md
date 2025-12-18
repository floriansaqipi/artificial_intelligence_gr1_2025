# Guest Seating Problem (SAT Encoding)

## Përshkrimi

Kemi **100 mysafirë** dhe **10 tavolina**, secila me **10 ulëse**. Qëllimi është të vendosen mysafirët në tavolina duke respektuar:

- çdo mysafir ulet **saktësisht në një tavolinë**;
- çdo tavolinë ka **saktësisht 10 mysafirë**;
- disa çifte mysafirësh **nuk guxojnë** të ulen në të njëjtën tavolinë (*not-together*);
- disa grupe mysafirësh **duhet** të ulen në të njëjtën tavolinë (*together*);
- **balanca e gjinisë**: ID-të **çift** janë meshkuj, ID-të **tek** janë femra, dhe për çdo tavolinë vlen  
  $|\#M - \#F| \le 3$. Me kapacitet 10, kjo lejon vetëm ndarjet: **4/6**, **5/5**, **6/4**.

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

Pse duhen **të dyja**? Sepse vetëm “$M_t\le 6$” do lejonte $M_t=0, F_t=10$, që shkel $|M-F|\le 3$. Duke vendosur edhe “$F_t\le 6$”, ekstremet ndalohen dhe mbeten vetëm ndarjet 4/6, 5/5, 6/4.

Në përgjithësi, për kapacitet $C$ dhe diferencë $d$, kufiri sipëror del:

$$
\text{upper} = \left\lfloor \frac{C + d}{2} \right\rfloor
$$

---

## Përkthimi në CNF (ideja)

SAT solver kërkon formulë në **CNF** (konjuksion klauzolash), pra:

$$
(\ell_{1,1}\vee \ell_{1,2}\vee\dots)\ \wedge\ (\ell_{2,1}\vee\dots)\ \wedge\ \cdots
$$

### A) AtLeastOne për një mysafir $g$
$$
x_{g,1} \vee x_{g,2} \vee \cdots \vee x_{g,10}
$$

### B) AtMostOne (versioni pairwise, konceptualisht i thjeshtë)
$$
\forall t_1 < t_2:\ (\neg x_{g,t_1} \vee \neg x_{g,t_2})
$$

### C) Not-together për $(a,b)$
Për çdo tavolinë $t$:
$$
(\neg x_{a,t} \vee \neg x_{b,t})
$$

### D) Together me lider $g_1$ dhe anëtar $k$
Për çdo tavolinë $t$:
$$
(\neg x_{g_1,t} \vee x_{k,t}) \ \wedge\ (\neg x_{k,t} \vee x_{g_1,t})
$$

### E) AtMostK (p.sh. “maksimumi 10 mysafirë në tavolinë”, “maksimumi 6 meshkuj”, etj.)
Këto janë **kufizime kardinaliteti** të formës:

$$
\sum_i y_i \le K
$$

Në CNF zakonisht kodohen me një **encoding standard** (p.sh. *sequential counter*, *totalizer*, *sorting network*), që shton variabla ndihmëse. Në praktikë, bibliotekat SAT i gjenerojnë automatikisht këto klauzola.

---

## Procesi i zgjidhjes (pipeline)

1. **Modelimi** i problemit me variablat $x_{g,t}$ dhe kufizimet e mësipërme.
2. **Gjenerimi i CNF** (klauzolat) + (opsionale) eksportimi në **DIMACS**.
3. **Ekzekutimi i SAT solver-it** për të gjetur një model (SAT) ose të provojë që është e pamundur (UNSAT).
4. **Dekodimi** i modelit: për çdo mysafir $g$, gjendet tavolina $t$ ku $x_{g,t}=1$.

---

## Shënime / Kujdes

- Nëse një grup “together” ka madhësi $>C$, problemi është **UNSAT**.
- Nëse futni një çift në të dyja listat (“together” dhe “not-together”), problemi bëhet **UNSAT**.
- Ka shumë simetri (tavolinat janë të padallueshme). Shpesh ndihmon një “symmetry breaking” p.sh.: “mysafiri 1 ulet në tavolinën 1”.
