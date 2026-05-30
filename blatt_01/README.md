# Übungsblatt 1 – Grundlagen der Informatik (SimTech)

**Universität Stuttgart – IPVS / Scientific Computing**  
Prof. Dirk Pflüger, Stefan Zimmer – WS 2025/26

Musterlösungen und Converter-Tool für Aufgaben zu **Ausdrücken und Zuweisungen** sowie **booleschen Ausdrücken**.

---

## Skripte ausführen

Aus dem Projektverzeichnis (`blatt_01/`):

| Skript | Befehl (macOS / Linux) | Befehl (Windows) |
|--------|----------------------|-------------------|
| Musterlösungen anzeigen | `python3 main.py` | `python main.py` |
| Trainingsspiel starten | `python3 game.py` | `python game.py` |
| Tests ausführen | `python3 -m pytest tests/ -v` | `python -m pytest tests/ -v` |

Von außerhalb (`/Users/.../HADY/`):

| Skript | Befehl (macOS / Linux) | Befehl (Windows) |
|--------|----------------------|-------------------|
| Musterlösungen anzeigen | `python3 blatt_01/main.py` | `python blatt_01/main.py` |
| Trainingsspiel starten | `python3 blatt_01/game.py` | `python blatt_01/game.py` |
| Tests ausführen | `python3 -m pytest blatt_01/tests/ -v` | `python -m pytest blatt_01/tests/ -v` |

Zuerst ins Verzeichnis wechseln:
```bash
cd blatt_01
python3 main.py
python3 game.py
```

---

## Projektstruktur

```
blatt_01/
├── game.py                 # Trainingsspiel für Studierende
├── main.py                 # Demo: zeigt alle Lösungen und Converter-Funktionen
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── aufgabe_1_1.py      # Musterlösungen Aufgabe 1.1 (4 Formen)
│   ├── aufgabe_1_2.py      # Musterlösungen Aufgabe 1.2 (boolesche Vereinfachungen)
│   └── converter.py        # Converter-Tool zwischen allen 4 Formen
└── tests/
    ├── __init__.py
    ├── test_aufgabe_1_1.py
    ├── test_aufgabe_1_2.py
    └── test_converter.py
```

---

## Aufgabe 1.1 – Ausdrücke und Zuweisungen

Vier Darstellungsformen für Berechnungen sollen ineinander umgewandelt werden.

### Die 4 Formen

| Form | Beschreibung | Beispiel |
|------|-------------|---------|
| **1** | Allgemeine Zuweisung mit Operatoren und Klammern | `a = (b + 2) * (c + 3)` |
| **2** | Dreiadress-Code (max. eine Operation pro Zeile) | `t1 = b + 2`<br>`t2 = c + 3`<br>`a = t1 * t2` |
| **3** | Funktionsaufrufe (`add`, `sub`, `mul`, `floordiv`, `neg`) | `a = mul(add(b, 2), add(c, 3))` |
| **4** | Methodenaufrufe (`__add__`, `__sub__`, `__mul__`, `__floordiv__`, `__neg__`) | `a = b.__add__(2).__mul__(c.__add__(3))` |

### Teil a) Gegeben: Form 2

```
t1 = b + c
a  = t1 * 2
```

**Form 1:** `a = (b + c) * 2` — Die beiden Zeilen werden zu einem Ausdruck zusammengefasst.

**Form 2:** bleibt wie gegeben.

**Form 3:** `a = mul(add(b, c), 2)` — `+` wird zu `add(b, c)`, `*` wird zu `mul(... , 2)`.

**Form 4:** `a = b.__add__(c).__mul__(2)` — `b + c` wird zu `b.__add__(c)`, das Ergebnis `.mul(2)`.

### Teil b) Gegeben: Form 1

```
a = (b + 2) * (c + 3)
```

**Form 1:** bleibt wie gegeben.

**Form 2:** Aufspalten in elementare Operationen: erst `b + 2`, dann `c + 3`, dann multiplizieren.
```
t1 = b + 2
t2 = c + 3
a  = t1 * t2
```

**Form 3:** Jeden Operator durch den entsprechenden Funktionsaufruf ersetzen:
```
a = mul(add(b, 2), add(c, 3))
```

**Form 4:** Jeden Operator durch den entsprechenden Methodenaufruf ersetzen:
```
a = b.__add__(2).__mul__(c.__add__(3))
```

### Teil c) Gegeben: Form 3

```
a = sub(b, sub(sub(c, d), e))
```

Dies entspricht: `a = b - ((c - d) - e)`

**Form 1:** `a = b - ((c - d) - e)` — die Funktionsaufrufe werden zurück in Operatoren übersetzt.

**Form 2:** Von innen nach außen in Einzelschritte zerlegen:
```
t1 = c - d
t2 = t1 - e
a  = b - t2
```

**Form 3:** bleibt wie gegeben.

**Form 4:** Jede Funktion wird zur entsprechenden Methode. Die Klammerung bleibt gleich:
```
a = b.__sub__(c.__sub__(d).__sub__(e))
```

### Teil d) Gegeben: Form 4

```
a = c.__mul__(d.__neg__().__add__(2))
```

Dies entspricht: `c * ((-d) + 2)` = `c * (2 - d)`

**Form 1:** `a = c * (2 - d)` — Methodenaufrufe zurück in Operatoren.

**Form 2:** Negation zuerst, dann Addition, dann Multiplikation:
```
t1 = -d
t2 = t1 + 2
a  = c * t2
```

**Form 3:** Methoden werden zu Funktionen:
```
a = mul(c, add(neg(d), 2))
```

**Form 4:** bleibt wie gegeben.

### Verifikation

Alle vier Formen liefern für gleiche Variablenwerte identische Ergebnisse:

| Teil | b | c | d | e | Ergebnis |
|------|---|---|---|---|----------|
| a | 3 | 7 | – | – | 20 |
| b | 3 | 7 | – | – | 50 |
| c | 10 | 8 | 3 | 2 | 7 |
| d | – | 5 | 3 | – | -5 |

---

## Aufgabe 1.2 – Mehr Ausdrücke

Boolesche Ausdrücke mit `int`-Variablen sollen logisch vereinfacht werden.

### a) `True and False`

→ `False`

Die Konjunktion (`and`) ist nur wahr, wenn beide Operanden wahr sind. Da `False` beteiligt ist, ist das Ergebnis immer `False`.

### b) `a < b or a == b`

→ `a <= b`

Die Aussage "a ist kleiner als b oder a ist gleich b" bedeutet genau: a ist kleiner oder gleich b. Der `<=`-Operator fasst beide Fälle zusammen.

### c) `a < b or a > b`

→ `a != b`

Wenn a kleiner oder größer als b ist, dann ist a ungleich b. Der einzige Fall, in dem die Aussage falsch ist, ist `a == b`.

### d) `not (a <= b and a >= b)`

→ `a != b`

`a <= b and a >= b` bedeutet `a == b` (a ist sowohl ≤ b als auch ≥ b). Die Negation davon ist `a != b`.

### e) `a > b == True`

→ `a > b`

Der Vergleich `a > b` liefert bereits einen booleschen Wert (`True` oder `False`). Der zusätzliche Vergleich mit `True` ist redundant. (Achtung: Python behandelt `a > b == True` als *chained comparison*, also `(a > b) and (b == True)`. Mathematisch-logisch ist aber `(a > b) == True` gemeint, was zu `a > b` vereinfacht.)

### f) `a < b and c > 0 or a > b and c > 0`

→ `a != b and c > 0`

`c > 0` kommt in beiden Teilausdrücken vor und kann ausgeklammert werden:

```
c > 0 and (a < b or a > b)
```

Der Klammerausdruck `a < b or a > b` vereinfacht (wie in c) zu `a != b`. Also insgesamt:

```
c > 0 and a != b
```

### Wahrheitstafeln

Für die Teile b–f ergibt sich:

| a | b | c | b) `a<=b` | c) `a!=b` | d) `a!=b` | e) `a>b` | f) `a!=b ∧ c>0` |
|---|---|---|-----------|-----------|-----------|----------|-----------------|
| 3 | 5 | 1 | ✅ True | ✅ True | ✅ True | ❌ False | ✅ True |
| 3 | 5 | -1| ✅ True | ✅ True | ✅ True | ❌ False | ❌ False |
| 5 | 5 | 1 | ✅ True | ❌ False | ❌ False | ❌ False | ❌ False |
| 7 | 5 | 1 | ❌ False | ✅ True | ✅ True | ✅ True | ✅ True |
| 7 | 5 | -1| ❌ False | ✅ True | ✅ True | ✅ True | ❌ False |

---

## Converter-Tool

Das Tool in `src/converter.py` kann automatisch zwischen den Formen konvertieren.

| Form → Form | Funktion |
|-------------|----------|
| 1 → 2 | `form1_to_form2(expr)` |
| 1 → 3 | `form1_to_form3(expr)` |
| 1 → 4 | `form1_to_form4(expr)` |
| 3 → 1 | `form3_to_form1(func_expr)` |
| 4 → 1 | `form4_to_form1(method_expr)` |

Das Tool arbeitet mit Pythons `ast`-Modul und wandelt den Ausdrucksbaum in die Zielform um.
