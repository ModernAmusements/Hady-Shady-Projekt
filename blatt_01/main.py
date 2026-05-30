from src import aufgabe_1_1, aufgabe_1_2
from src.converter import (
    form1_to_form2, form1_to_form3, form1_to_form4,
    form3_to_form1, form4_to_form1,
    reset_temp_counter,
)


def main():
    print("=" * 60)
    print("  Grundlagen der Informatik (SimTech) – WS 2025/26")
    print("  Übungsblatt 1 – Musterlösungen")
    print("=" * 60)

    print(f"\n{aufgabe_1_1.AUFGABE}")
    print("-" * 40)
    for teil in "abcd":
        aufgabe_1_1.zeige_loesung(teil)

    print("\nVerifikation (alle Formen liefern identische Ergebnisse):")
    aufgabe_1_1.ueberpruefe_loesungen()

    print(f"\n{aufgabe_1_2.AUFGABE}")
    print("-" * 40)
    for teil in "abcdef":
        aufgabe_1_2.zeige_loesung(teil)

    print("\nVerifikation:")
    aufgabe_1_2.ueberpruefe_loesungen()

    print(f"\n{'=' * 60}")
    print("  Converter-Tool – Demonstration")
    print(f"{'=' * 60}")

    beispiele = [
        ("(b + 2) * (c + 3)", "Form 1 → Form 2 (Dreiadress-Code)"),
        ("(b + 2) * (c + 3)", "Form 1 → Form 3 (Funktionsaufrufe)"),
        ("(b + 2) * (c + 3)", "Form 1 → Form 4 (Methodenaufrufe)"),
        ("mul(add(b, 2), add(c, 3))", "Form 3 → Form 1 (Standard-Ausdruck)"),
        ("c.__mul__(d.__neg__().__add__(2))", "Form 4 → Form 1 (Standard-Ausdruck)"),
    ]

    for expr, desc in beispiele:
        print(f"\n  {desc}:")
        print(f"    Eingabe:  {expr}")
        try:
            if desc.startswith("Form 1 → Form 2"):
                reset_temp_counter()
                stmts = form1_to_form2(expr)
                print(f"    Ausgabe:  {', '.join(stmts)}")
            elif desc.startswith("Form 1 → Form 3"):
                out = form1_to_form3(expr)
                print(f"    Ausgabe:  {out}")
            elif desc.startswith("Form 1 → Form 4"):
                out = form1_to_form4(expr)
                print(f"    Ausgabe:  {out}")
            elif desc.startswith("Form 3 → Form 1"):
                out = form3_to_form1(expr)
                print(f"    Ausgabe:  {out}")
            elif desc.startswith("Form 4 → Form 1"):
                out = form4_to_form1(expr)
                print(f"    Ausgabe:  {out}")
        except Exception as e:
            print(f"    Fehler: {e}")

    print()

if __name__ == "__main__":
    main()
