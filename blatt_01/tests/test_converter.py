import pytest
from src.converter import (
    form1_to_form2, form1_to_form3, form1_to_form4,
    form3_to_form1, form4_to_form1,
    evaluate_form1, evaluate_form3, evaluate_form4,
    reset_temp_counter,
)


class TestForm1ToForm2:
    def test_einfache_addition(self):
        reset_temp_counter()
        stmts = form1_to_form2("b + 2")
        assert len(stmts) == 2
        assert stmts[0] == "t1 = b + 2"
        assert stmts[1] == "a = t1"

    def test_verschachtelt(self):
        reset_temp_counter()
        stmts = form1_to_form2("(b + 2) * (c + 3)")
        assert len(stmts) == 4
        assert "t3 = t1 * t2" in stmts[:-1]

    def test_unary_minus(self):
        reset_temp_counter()
        stmts = form1_to_form2("-b")
        assert len(stmts) == 2
        assert stmts[0] == "t1 = -b"
        assert stmts[1] == "a = t1"


class TestForm1ToForm3:
    def test_addition(self):
        result = form1_to_form3("b + 2")
        assert result == "add(b, 2)"

    def test_verschachtelt(self):
        result = form1_to_form3("(b + 2) * (c + 3)")
        assert result == "mul(add(b, 2), add(c, 3))"

    def test_negation(self):
        result = form1_to_form3("-b")
        assert result == "neg(b)"

    def test_komplex(self):
        result = form1_to_form3("b - ((c - d) - e)")
        assert result == "sub(b, sub(sub(c, d), e))"


class TestForm1ToForm4:
    def test_addition(self):
        result = form1_to_form4("b + 2")
        assert result == "b.__add__(2)"

    def test_verschachtelt(self):
        result = form1_to_form4("(b + 2) * (c + 3)")
        assert result == "b.__add__(2).__mul__(c.__add__(3))"

    def test_negation(self):
        result = form1_to_form4("-d")
        assert result == "d.__neg__()"

    def test_komplex(self):
        result = form1_to_form4("b - ((c - d) - e)")
        assert result == "b.__sub__(c.__sub__(d).__sub__(e))"


class TestForm3ToForm1:
    def test_add(self):
        result = form3_to_form1("add(b, 2)")
        assert result == "(b + 2)"

    def test_verschachtelt(self):
        result = form3_to_form1("mul(add(b, 2), add(c, 3))")
        assert result == "((b + 2) * (c + 3))"

    def test_neg(self):
        result = form3_to_form1("neg(b)")
        assert result == "-b"

    def test_komplex(self):
        result = form3_to_form1("sub(b, sub(sub(c, d), e))")
        assert result == "(b - ((c - d) - e))"


class TestForm4ToForm1:
    def test_add(self):
        result = form4_to_form1("b.__add__(2)")
        assert result == "(b + 2)"

    def test_verschachtelt(self):
        result = form4_to_form1("b.__add__(2).__mul__(c.__add__(3))")
        assert result == "((b + 2) * (c + 3))"

    def test_neg(self):
        result = form4_to_form1("d.__neg__()")
        assert result == "-d"

    def test_komplex(self):
        result = form4_to_form1("b.__sub__(c.__sub__(d).__sub__(e))")
        assert result == "(b - ((c - d) - e))"


class TestEvaluateFunctions:
    def test_form3(self):
        result = evaluate_form3("add(mul(b, 2), neg(c))", b=3, c=5)
        assert result == 1
        assert result == (3 * 2 + (-5))

    def test_form4(self):
        result = evaluate_form4("b.__add__(2).__mul__(c.__add__(3))", b=3, c=7)
        assert result == 50
        assert result == (3 + 2) * (7 + 3)

    def test_form1(self):
        result = evaluate_form1("(b + 2) * (c + 3)", b=3, c=7)
        assert result == 50
