from operator import add, sub, mul, floordiv, neg


AUFGABE = "1.1 Ausdrücke und Zuweisungen"


loesungen = {}

loesungen["a"] = {
    "gegeben": "t1 = b + c\na = t1 * 2",
    "form": 2,
    "form1": "a = (b + c) * 2",
    "form2": ["t1 = b + c", "a = t1 * 2"],
    "form3": "a = mul(add(b, c), 2)",
    "form4": "a = b.__add__(c).__mul__(2)",
}

loesungen["b"] = {
    "gegeben": "a = (b + 2) * (c + 3)",
    "form": 1,
    "form1": "a = (b + 2) * (c + 3)",
    "form2": ["t1 = b + 2", "t2 = c + 3", "a = t1 * t2"],
    "form3": "a = mul(add(b, 2), add(c, 3))",
    "form4": "a = b.__add__(2).__mul__(c.__add__(3))",
}

loesungen["c"] = {
    "gegeben": "a = sub(b, sub(sub(c, d), e))",
    "form": 3,
    "form1": "a = b - ((c - d) - e)",
    "form2": ["t1 = c - d", "t2 = t1 - e", "a = b - t2"],
    "form3": "a = sub(b, sub(sub(c, d), e))",
    "form4": "a = b.__sub__(c.__sub__(d).__sub__(e))",
}

loesungen["d"] = {
    "gegeben": "a = c.__mul__(d.__neg__().__add__(2))",
    "form": 4,
    "form1": "a = c * (2 - d)",
    "form2": ["t1 = -d", "t2 = t1 + 2", "a = c * t2"],
    "form3": "a = mul(c, add(neg(d), 2))",
    "form4": "a = c.__mul__(d.__neg__().__add__(2))",
}


def zeige_loesung(teil: str):
    l = loesungen[teil]
    print(f"  Teil {teil})  (gegeben: Form {l['form']})")
    print(f"    Gegeben:  {l['gegeben']}")
    print(f"    Form 1:   {l['form1']}")
    print("    Form 2:   " + ", ".join(l['form2']))
    print(f"    Form 3:   {l['form3']}")
    print(f"    Form 4:   {l['form4']}")
    print()


def ueberpruefe_loesungen():
    testfaelle = {
        "a": {"b": 3, "c": 7},
        "b": {"b": 3, "c": 7},
        "c": {"b": 10, "c": 8, "d": 3, "e": 2},
        "d": {"c": 5, "d": 3},
    }

    for teil, vars in testfaelle.items():
        l = loesungen[teil]
        expected = evaluate_form1_safe(l["form1"], vars)

        f1 = evaluate_form1_safe(l["form1"], vars)
        assert f1 == expected, f"{teil} form1: {f1} != {expected}"

        f2_val = _eval_form2(l["form2"], vars)
        assert f2_val == expected, f"{teil} form2: {f2_val} != {expected}"

        f3_val = _eval_func(l["form3"], vars)
        assert f3_val == expected, f"{teil} form3: {f3_val} != {expected}"

        f4_val = _eval_method(l["form4"], vars)
        assert f4_val == expected, f"{teil} form4: {f4_val} != {expected}"

        print(f"  ✓ Teil {teil}: alle Formen liefern {expected}")


def evaluate_form1_safe(expr: str, vars: dict) -> int:
    return eval(expr.split("=", 1)[1].strip(), {"__builtins__": {}}, vars)


def _eval_form2(stmts: list[str], vars: dict) -> int:
    local_vars = dict(vars)
    for stmt in stmts:
        target, expr = stmt.split("=", 1)
        target = target.strip()
        val = eval(expr.strip(), {"__builtins__": {}}, local_vars)
        local_vars[target] = val
    return local_vars["a"]


def _eval_func(expr: str, vars: dict) -> int:
    safe_ops = {"add": add, "sub": sub, "mul": mul, "floordiv": floordiv, "neg": neg}
    env = {**safe_ops, **vars}
    target, call = expr.split("=", 1)
    return eval(call.strip(), {"__builtins__": {}}, env)


def _eval_method(expr: str, vars: dict) -> int:
    target, call = expr.split("=", 1)
    return eval(call.strip(), {"__builtins__": {}}, vars)
