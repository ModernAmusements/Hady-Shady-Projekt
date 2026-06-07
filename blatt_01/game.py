import ast
import random
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.converter import (
    Form1Parser,
    form1_to_form2, form1_to_form3, form1_to_form4,
    form3_to_form1, form4_to_form1,
    reset_temp_counter,
)


EXPRESSIONS = [
    "b + 2",
    "c - 3",
    "-d",
    "a + b",
    "(b + 2) * (c + 3)",
    "b - (c - d)",
    "b - ((c - d) - e)",
    "c * (2 - d)",
    "a + b * c",
    "(a + b) * c",
    "x - y - z",
    "a // b + c",
    "-(a + b)",
    "b + c * d",
    "(b + c) * d",
    "d - e - f",
    "a + (b - c)",
    "(a - b) - c",
]

FORM_NAMES = {
    1: "Form 1 (Standard)",
    2: "Form 2 (Dreiadress-Code)",
    3: "Form 3 (Funktionsaufrufe)",
    4: "Form 4 (Methodenaufrufe)",
}

FORM_SHORT = {1: "Form 1", 2: "Form 2", 3: "Form 3", 4: "Form 4"}


def convert(expr: str, from_form: int, to_form: int) -> str:
    if from_form == 1 and to_form == 2:
        reset_temp_counter()
        stmts = form1_to_form2(expr)
        return "; ".join(stmts)
    if from_form == 1 and to_form == 3:
        return form1_to_form3(expr)
    if from_form == 1 and to_form == 4:
        return form1_to_form4(expr)
    if from_form == 3 and to_form == 1:
        return form3_to_form1(expr)
    if from_form == 4 and to_form == 1:
        return form4_to_form1(expr)
    if from_form == 2 and to_form == 1:
        stmts = [s.strip() for s in expr.split(";")]
        last = stmts[-1]
        target, rhs = last.split(" = ", 1)
        return rhs
    raise ValueError(f"Conversion {from_form}->{to_form} not supported")


def generate_distractors(correct: str, expr: str, from_form: int, to_form: int, count: int = 3) -> list[str]:
    distractors = set()
    ops = ["+", "-", "*", "//"]
    funcs = ["add", "sub", "mul", "floordiv"]
    methods = ["__add__", "__sub__", "__mul__", "__floordiv__"]

    strategies = []
    if to_form == 1:
        if from_form == 2:
            strategies.append(lambda: _dist_form2_as_form1(expr))
        elif from_form == 3:
            strategies.append(lambda: _dist_func_swap(expr))
            strategies.append(lambda: _dist_func_to_form1_wrong(expr))
        elif from_form == 4:
            strategies.append(lambda: _dist_method_swap(expr))
    if to_form == 2:
        strategies.append(lambda: _dist_form1_wrong_op(expr, ops))
        strategies.append(lambda: _dist_form1_swap(expr))
    if to_form == 3:
        strategies.append(lambda: _dist_func_swap(correct))
        strategies.append(lambda: _dist_func_wrong_name(correct))
    if to_form == 4:
        strategies.append(lambda: _dist_method_swap(correct))

    for s in strategies:
        try:
            d = s()
            if d and d != correct and d not in distractors:
                distractors.add(d)
                if len(distractors) >= count:
                    break
        except Exception:
            pass

    result = list(distractors)[:count]
    max_attempts = 50
    attempts = 0
    while len(result) < count and attempts < max_attempts:
        attempts += 1
        for s in strategies:
            if len(result) >= count or attempts >= max_attempts:
                break
            try:
                d = s()
                if d and d != correct and d not in result:
                    result.append(d)
            except Exception:
                pass
    while len(result) < count:
        result.append(correct)
    return result


def _dist_form1_swap(expr: str):
    parsed = ast.parse(expr, mode="eval").body
    if isinstance(parsed, ast.BinOp):
        return Form1Parser.expr_to_str(ast.BinOp(
            left=parsed.right, op=parsed.op, right=parsed.left
        ))


def _dist_form1_wrong_op(expr: str, ops: list[str]):
    for op in ops:
        if op in expr:
            other = random.choice([o for o in ops if o != op])
            alt = expr.replace(op, other, 1)
            reset_temp_counter()
            stmts = form1_to_form2(alt)
            return "; ".join(stmts)


def _dist_form2_as_form1(expr: str):
    stmts = [s.strip() for s in expr.split(";")]
    last = stmts[-1]
    _, rhs = last.split(" = ", 1)
    parsed = ast.parse(rhs, mode="eval").body
    if isinstance(parsed, ast.BinOp):
        return Form1Parser.expr_to_str(ast.BinOp(
            left=parsed.right, op=parsed.op, right=parsed.left
        ))


def _dist_func_swap(expr: str):
    result = expr
    swaps = [("add", "sub"), ("sub", "add"), ("mul", "floordiv"), ("floordiv", "mul")]
    random.shuffle(swaps)
    for old, new in swaps:
        if old in result:
            return result.replace(old, new, 1)


def _dist_func_wrong_name(expr: str):
    result = expr
    for old, new in [("add", "mul"), ("sub", "floordiv"), ("mul", "sub"), ("floordiv", "add"), ("neg", "add")]:
        if old in result:
            return result.replace(old, new, 1)


def _dist_func_to_form1_wrong(expr: str):
    result = expr
    for old, new in [("add", "sub"), ("sub", "add")]:
        if old in result:
            alt = result.replace(old, new, 1)
            return form3_to_form1(alt)


def _dist_method_swap(expr: str):
    result = expr
    swaps = [("__add__", "__sub__"), ("__sub__", "__add__"),
             ("__mul__", "__floordiv__"), ("__floordiv__", "__mul__"),
             ("__add__", "__mul__"), ("__sub__", "__floordiv__")]
    random.shuffle(swaps)
    for old, new in swaps:
        if old in result:
            return result.replace(old, new, 1)


def run_round(round_num: int, total: int) -> bool:
    expr = random.choice(EXPRESSIONS)
    forms = [1, 2, 3, 4]
    random.shuffle(forms)
    from_f = forms[0]
    to_f = forms[1]
    while _needs_converter_not_supported(from_f, to_f):
        random.shuffle(forms)
        from_f = forms[0]
        to_f = forms[1]

    try:
        correct = convert(expr, from_f, to_f)
    except Exception:
        return run_round(round_num, total)

    distractors = generate_distractors(correct, expr, from_f, to_f, 3)
    options = [correct] + distractors
    random.shuffle(options)

    print()
    print("=" * 62)
    print(f"  Runde {round_num}/{total}")
    print(f"  Wandle um:  {FORM_NAMES[from_f]}  →  {FORM_NAMES[to_f]}")
    print(f"  Ausdruck:   {expr}")
    print("=" * 62)
    print()

    for i, opt in enumerate(options):
        display = _format_option(opt, to_f)
        print(f"    {chr(97 + i)})  {display}")
    print()

    while True:
        choice = input("  Deine Antwort (a-d): ").strip().lower()
        if choice in ("a", "b", "c", "d"):
            break
        print("  Bitte a, b, c oder d eingeben.")

    idx = ord(choice) - 97
    if options[idx] == correct:
        print(f"  ✅  Richtig!  🎉")
        return True
    else:
        print(f"  ❌  Falsch.")
        print(f"  Richtig wäre:  {_format_option(correct, to_f)}")
        return False


def _needs_converter_not_supported(from_f, to_f):
    unsupported = [(2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (2, 2), (3, 3), (4, 4), (1, 1), (2, 1), (3, 1), (4, 1)]
    return (from_f, to_f) in unsupported


def _format_option(opt: str, to_form: int) -> str:
    if to_form == 2:
        return opt.replace("; ", "\n           ")
    return opt


def main():
    print()
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║    Formen-Konverter – Trainingsspiel             ║")
    print("  ║    Übungsblatt 1 – Grundlagen der Informatik    ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print()
    print("  Wandle Ausdrücke zwischen den 4 Darstellungsformen um.")
    print("  Wähle die richtige Antwort (a-d).")
    print()

    while True:
        try:
            total = input("  Wie viele Runden möchtest du spielen? ")
            total = int(total)
            if total > 0:
                break
        except ValueError:
            pass

    correct_count = 0
    for r in range(1, total + 1):
        if run_round(r, total):
            correct_count += 1

    pct = round(100 * correct_count / total)
    score = "★" * (pct // 20) + "☆" * (5 - pct // 20)

    print()
    print("=" * 62)
    print(f"  Spiel beendet!")
    print(f"  Punkte:  {correct_count}/{total}  ({pct}%)")
    print(f"  {score}")
    if pct >= 80:
        print("  Sehr gut! Du hast die Formen verstanden. 🏆")
    elif pct >= 60:
        print("  Gut gemacht! Noch etwas üben? 💪")
    else:
        print("  Weiter üben – du schaffst das! 📚")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()
