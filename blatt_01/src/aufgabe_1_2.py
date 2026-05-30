AUFGABE = "1.2 Mehr Ausdrücke"


loesungen = {
    "a": {
        "ausdruck": "True and False",
        "vereinfacht": "False",
        "erklaerung": "True and False ergibt immer False (Konjunktion).",
    },
    "b": {
        "ausdruck": "a < b or a == b",
        "vereinfacht": "a <= b",
        "erklaerung": "a < b oder a == b ist äquivalent zu a <= b.",
    },
    "c": {
        "ausdruck": "a < b or a > b",
        "vereinfacht": "a != b",
        "erklaerung": "a < b oder a > b bedeutet a ist ungleich b.",
    },
    "d": {
        "ausdruck": "not (a <= b and a >= b)",
        "vereinfacht": "a != b",
        "erklaerung": "a <= b und a >= b bedeutet a == b; die Negation ergibt a != b.",
    },
    "e": {
        "ausdruck": "a > b == True",
        "vereinfacht": "a > b",
        "erklaerung": "Der Vergleich a > b liefert bereits einen booleschen Wert; == True ist redundant.",
    },
    "f": {
        "ausdruck": "a < b and c > 0 or a > b and c > 0",
        "vereinfacht": "a != b and c > 0",
        "erklaerung": "c > 0 kann ausgeklammert werden: c > 0 and (a < b or a > b) = c > 0 and a != b.",
    },
}


def zeige_loesung(teil: str):
    l = loesungen[teil]
    print(f"  Teil {teil})  {l['ausdruck']}")
    print(f"    → {l['vereinfacht']}")
    print(f"    ({l['erklaerung']})")
    print()


def ueberpruefe_loesungen():
    testfaelle = {
        "a": [],
        "b": [(3, 5), (5, 5), (7, 5)],
        "c": [(3, 5), (5, 5), (7, 5)],
        "d": [(3, 5), (5, 5), (7, 5)],
        "e": [(3, 5), (5, 5), (7, 5)],
        "f": [(3, 5, 1), (3, 5, -1), (7, 5, 1), (5, 5, 1)],
    }

    for teil, tests in testfaelle.items():
        l = loesungen[teil]
        if teil == "a":
            orig = eval(l["ausdruck"])
            simp = eval(l["vereinfacht"])
            assert orig == simp, f"{teil}: {orig} != {simp}"
            print(f"  ✓ Teil a: {l['ausdruck']} = {simp}")
        elif teil in ("b", "c", "d"):
            for a, b in tests:
                orig_vars = {"a": a, "b": b}
                orig = eval(l["ausdruck"], {"__builtins__": {}}, orig_vars)
                simp = eval(l["vereinfacht"], {"__builtins__": {}}, orig_vars)
                assert orig == simp, f"{teil} (a={a},b={b}): {orig} != {simp}"
            print(f"  ✓ Teil {teil}: {l['ausdruck']} → {l['vereinfacht']}")
        elif teil == "e":
            for a, b in tests:
                orig_vars = {"a": a, "b": b}
                orig = eval(l["ausdruck"], {"__builtins__": {}}, orig_vars)
                simp = eval(l["vereinfacht"], {"__builtins__": {}}, orig_vars)
                orig_logisch = orig_vars["a"] > orig_vars["b"]
                assert simp == orig_logisch, f"{teil} (a={a},b={b}): Vereinfachung {simp} sollte {orig_logisch} sein"
            print(f"  ✓ Teil e: {l['ausdruck']} → {l['vereinfacht']}")
        elif teil == "f":
            for vals in tests:
                a, b, c = vals
                orig_vars = {"a": a, "b": b, "c": c}
                orig = eval(l["ausdruck"], {"__builtins__": {}}, orig_vars)
                simp = eval(l["vereinfacht"], {"__builtins__": {}}, orig_vars)
                assert orig == simp, f"{teil} (a={a},b={b},c={c}): {orig} != {simp}"
            print(f"  ✓ Teil f: {l['ausdruck']} → {l['vereinfacht']}")
