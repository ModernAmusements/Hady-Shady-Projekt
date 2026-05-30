import pytest
from src.aufgabe_1_2 import loesungen


def test_a_true_and_false():
    assert eval(loesungen["a"]["ausdruck"]) == eval(loesungen["a"]["vereinfacht"])


@pytest.mark.parametrize("a,b,expected", [
    (3, 5, True),
    (5, 5, True),
    (7, 5, False),
])
def test_b_a_lt_b_or_a_eq_b(a, b, expected):
    vars = {"a": a, "b": b}
    orig = eval(loesungen["b"]["ausdruck"], {"__builtins__": {}}, vars)
    simp = eval(loesungen["b"]["vereinfacht"], {"__builtins__": {}}, vars)
    assert orig == simp == expected


@pytest.mark.parametrize("a,b,expected", [
    (3, 5, True),
    (5, 5, False),
    (7, 5, True),
])
def test_c_a_lt_b_or_a_gt_b(a, b, expected):
    vars = {"a": a, "b": b}
    orig = eval(loesungen["c"]["ausdruck"], {"__builtins__": {}}, vars)
    simp = eval(loesungen["c"]["vereinfacht"], {"__builtins__": {}}, vars)
    assert orig == simp == expected


@pytest.mark.parametrize("a,b,expected", [
    (3, 5, True),
    (5, 5, False),
    (7, 5, True),
])
def test_d_not_a_le_b_and_a_ge_b(a, b, expected):
    vars = {"a": a, "b": b}
    orig = eval(loesungen["d"]["ausdruck"], {"__builtins__": {}}, vars)
    simp = eval(loesungen["d"]["vereinfacht"], {"__builtins__": {}}, vars)
    assert orig == simp == expected


@pytest.mark.parametrize("a,b,expected", [
    (3, 5, False),
    (5, 5, False),
    (7, 5, True),
])
def test_e_a_gt_b_eq_true(a, b, expected):
    vars = {"a": a, "b": b}
    orig = eval(loesungen["e"]["ausdruck"], {"__builtins__": {}}, vars)
    simp = eval(loesungen["e"]["vereinfacht"], {"__builtins__": {}}, vars)
    assert simp == expected
    if "== True" in loesungen["e"]["ausdruck"]:
        mathematisch = eval(
            loesungen["e"]["ausdruck"].replace("== True", ""),
            {"__builtins__": {}}, vars
        )
        assert mathematisch == simp


@pytest.mark.parametrize("a,b,c,expected", [
    (3, 5, 1, True),
    (3, 5, -1, False),
    (7, 5, 1, True),
    (7, 5, -1, False),
    (5, 5, 1, False),
    (5, 5, -1, False),
])
def test_f_combined(a, b, c, expected):
    vars = {"a": a, "b": b, "c": c}
    orig = eval(loesungen["f"]["ausdruck"], {"__builtins__": {}}, vars)
    simp = eval(loesungen["f"]["vereinfacht"], {"__builtins__": {}}, vars)
    assert orig == simp == expected
