import pytest
from src.aufgabe_1_1 import (
    loesungen,
    evaluate_form1_safe,
    _eval_form2,
    _eval_func,
    _eval_method,
)


TESTFAELLE = {
    "a": {"b": 3, "c": 7},
    "b": {"b": 3, "c": 7},
    "c": {"b": 10, "c": 8, "d": 3, "e": 2},
    "d": {"c": 5, "d": 3},
}


@pytest.mark.parametrize("teil", ["a", "b", "c", "d"])
def test_alle_formen_identisch(teil):
    l = loesungen[teil]
    vars = TESTFAELLE[teil]

    expected = evaluate_form1_safe(l["form1"], vars)

    f1 = evaluate_form1_safe(l["form1"], vars)
    assert f1 == expected

    f2 = _eval_form2(l["form2"], vars)
    assert f2 == expected

    f3 = _eval_func(l["form3"], vars)
    assert f3 == expected

    f4 = _eval_method(l["form4"], vars)
    assert f4 == expected


def test_verschiedene_werte():
    varianten = [
        ("a", {"b": 0, "c": 0}),
        ("a", {"b": -5, "c": 10}),
        ("b", {"b": 0, "c": 0}),
        ("b", {"b": -3, "c": -7}),
        ("c", {"b": 5, "c": 3, "d": 1, "e": 2}),
        ("d", {"c": 0, "d": 0}),
    ]

    for teil, vars in varianten:
        l = loesungen[teil]
        expected = evaluate_form1_safe(l["form1"], vars)
        for form_name, val in [
            ("form1", evaluate_form1_safe(l["form1"], vars)),
            ("form2", _eval_form2(l["form2"], vars)),
            ("form3", _eval_func(l["form3"], vars)),
            ("form4", _eval_method(l["form4"], vars)),
        ]:
            assert val == expected, (
                f"{teil} {form_name}: {val} != {expected} mit vars={vars}"
            )
