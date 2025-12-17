# 1. Blocked N-Queens Problem

# Problemi:

Përshkrimin e gjeni [këtu](https://dtai.cs.kuleuven.be/events/ASP-competition/Benchmarks/BlockedQueens.shtm).

Kërkesat e detyrës:
<ul>
  <li>Aplikoni A Star (A*) algoritmin për zgjidhjen e këtij problemi!</li>
  <li>Definoni te paktën tri heuristika për zgjidhjen e këtij problemi</li>
  <li>Propozoni nje “admissible” heuristic duke u bazuar ne rezultatet e ofruara nga #2!</li>
</ul>

# Zgjidhja:

## Algoritmi A*:

Për të përdorur këtë algoritëm, problemi duhet të reprezentohet sikur një graf ku nyjet V janë gjendje të tabelës, dhe degët E janë lëvizje. Lëvizjet e rradhës janë degët që të dërgojnë tek komshitë e gjendjes së çastit. 

### Gjendja e tabelës

Një varg i mbretëreshave të vendosura:

$$
  V_k = (Q_1, Q_2, Q_3, \dots, Q_k)
$$

Ku
<ul>
  <li><i>k &xrarr; indeksat e rreshtave që kanë mbretëreshë (distanca e gjendjes nga gjendja fillestare); k &le; N</i></li>
  <li><i>Q<sub>k</sub> &xrarr; indeksat e kolonave në të cilën është vendosur mbretëresha për k përkatëse; Q<sub>i</sub> &le; N</i></li>
  <li><i>N &xrarr; dimensioni i tabelës NxN</i></li>
  <li>As një mbretëreshë nuk e sulmon ndonjë mbretëreshë tjetër</li>
</ul>

### Gjendja fillestare:

$$
  V_0 = \emptyset
$$

### Gjendja finale:

$$
  |V| = N
$$

### Funksioni vlerësues (Evaluation function):

$$
 f(V_k) = g(V_k) + h(V_k)
$$

Ku
<ul>
  <li><i>f &xrarr; funksioni vlerësues (evaluation function)</i></li>
  <li><i>g &xrarr; funksioni i kostos (cost function)</i></li>
  <li><i>h &xrarr; funksioni heuristik (heuristic function)</i></li>
</ul>

<h3>Funksioni i kostos:</h3>

$$
  g(V_k) = |V_k|
$$

Çdo lëvizje valide shkakton gjendje të re.

## Definimi i 3 heuristikave 

### 1. Mbretëreshat e mbetura
$$
  h_1(V_k)=N-|V_k|
$$

### 2. Numri i rreshtave të bllokuar

$$
  h_2(V_k)=
  \begin{cases}
  \ \infty &amp; \text{nëse } \exists r \in R \text{ i tillë që } A(r) = 0 \\
  \ N-|V_k| &amp; \text{përndryshe}
  \end{cases}
$$

Ku:
<ul>
  <li>$R$ &xrarr; bashkësia e rreshtave të mbetur</li>
  <li>$L(r)$ &xrarr; numri i kolonave legale në rreshtin r; ku r \in R</li>
</ul>

### 3. Dendësia e fushave të sulmuara

$$
  h_3(V_k)=\frac{\displaystyle \sum_{i=1}^{N} |E| - |F_b| - |F_s|}{|E| - |F_b|}
$$

Ku:
<ul>
  <li>$E$ &xrarr; bashkësia e degëve</li>
  <li>$F_b$ &xrarr; bashkësia e fushave të bllokuara</li>
  <li>$F_b$ &xrarr; bashkësia e fushave të sigurta (pasulmuara)</li>
</ul>

## Përzgjedhja e heuristikës të pranueshme (admissible)

Heuristika e pranueshme e përzgjedhur është $h_2$.

$$
  h_2(V_k)=
  \begin{cases}
  \ \infty &amp; \text{nëse } \exists r \in R \text{ i tillë që } A(r) = 0 \\
  \ N-|V_k| &amp; \text{përndryshe}
  \end{cases}
$$

### Arsyetim:

Në mënyrë që të jetë një heuristikë e pranueshme, ajo duhet të mos e mbivlerësoj ndëshkimin heuristik. Heuristika $h_2$ nuk e mbivlerëson atë asnjëhere. Thjeshtë e pamundson ndonjë levizje që then kushtin e konfliktit (Nuk është mbivlerësim). 
