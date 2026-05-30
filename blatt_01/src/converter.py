import ast
import operator as op_mod
from io import StringIO
from contextlib import redirect_stdout

OP_MAP = {
    ast.Add: ("+", "add", "__add__"),
    ast.Sub: ("-", "sub", "__sub__"),
    ast.Mult: ("*", "mul", "__mul__"),
    ast.FloorDiv: ("//", "floordiv", "__floordiv__"),
    ast.USub: ("-", "neg", "__neg__"),
}

FUNC_TO_OP = {
    "add": ast.Add,
    "sub": ast.Sub,
    "mul": ast.Mult,
    "floordiv": ast.FloorDiv,
    "neg": ast.USub,
}

METHOD_TO_OP = {
    "__add__": ast.Add,
    "__sub__": ast.Sub,
    "__mul__": ast.Mult,
    "__floordiv__": ast.FloorDiv,
    "__neg__": ast.USub,
}


class Form1Parser:
    @staticmethod
    def parse(expr: str) -> ast.Expr:
        return ast.parse(expr, mode="eval")

    @staticmethod
    def expr_to_str(node: ast.AST) -> str:
        if isinstance(node, ast.Constant):
            return repr(node.value)
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.UnaryOp):
            op_str = OP_MAP[type(node.op)][0]
            operand = Form1Parser.expr_to_str(node.operand)
            return f"{op_str}{operand}"
        if isinstance(node, ast.BinOp):
            left = Form1Parser.expr_to_str(node.left)
            right = Form1Parser.expr_to_str(node.right)
            op_str = OP_MAP[type(node.op)][0]
            return f"({left} {op_str} {right})"
        raise ValueError(f"Unknown node: {type(node).__name__}")


def form1_to_form2(expr: str, target_var: str = "a") -> list[str]:
    node = Form1Parser.parse(expr).body
    stmts = []
    _gen_tac(node, stmts, target_var)
    return stmts


_tac_counter = 0


def _fresh_temp():
    global _tac_counter
    _tac_counter += 1
    return f"t{_tac_counter}"


def _tac_expr(node: ast.AST, stmts: list[str]) -> str:
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.UnaryOp):
        op_char = OP_MAP[type(node.op)][0]
        operand = _tac_expr(node.operand, stmts)
        temp = _fresh_temp()
        stmts.append(f"{temp} = {op_char}{operand}")
        return temp
    if isinstance(node, ast.BinOp):
        op_char = OP_MAP[type(node.op)][0]
        left = _tac_expr(node.left, stmts)
        right = _tac_expr(node.right, stmts)
        temp = _fresh_temp()
        stmts.append(f"{temp} = {left} {op_char} {right}")
        return temp
    raise ValueError(f"Unknown node: {type(node).__name__}")


def _gen_tac(node: ast.AST, stmts: list[str], target: str) -> None:
    expr = _tac_expr(node, stmts)
    stmts.append(f"{target} = {expr}")


def form1_to_form3(expr: str) -> str:
    node = Form1Parser.parse(expr).body
    return _to_func_call(node)


def _to_func_call(node: ast.AST) -> str:
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.UnaryOp):
        func_name = OP_MAP[type(node.op)][1]
        operand = _to_func_call(node.operand)
        return f"{func_name}({operand})"
    if isinstance(node, ast.BinOp):
        func_name = OP_MAP[type(node.op)][1]
        left = _to_func_call(node.left)
        right = _to_func_call(node.right)
        return f"{func_name}({left}, {right})"
    raise ValueError(f"Unknown node: {type(node).__name__}")


def form1_to_form4(expr: str) -> str:
    node = Form1Parser.parse(expr).body
    return _to_method_call(node)


def _to_method_call(node: ast.AST) -> str:
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.UnaryOp):
        method_name = OP_MAP[type(node.op)][2]
        operand = _to_method_call(node.operand)
        return f"{operand}.{method_name}()"
    if isinstance(node, ast.BinOp):
        method_name = OP_MAP[type(node.op)][2]
        left = _to_method_call(node.left)
        right = _to_method_call(node.right)
        return f"{left}.{method_name}({right})"
    raise ValueError(f"Unknown node: {type(node).__name__}")


def form3_to_form1(func_expr: str) -> str:
    result = _parse_func_call(ast.parse(func_expr, mode="eval").body)
    return Form1Parser.expr_to_str(result)


def _parse_func_call(node: ast.AST) -> ast.AST:
    if isinstance(node, ast.Constant):
        return node
    if isinstance(node, ast.Name):
        return node
    if isinstance(node, ast.Call):
        func_name = node.func.id if isinstance(node.func, ast.Name) else None
        if func_name not in FUNC_TO_OP:
            raise ValueError(f"Unknown function: {func_name}")
        op_type = FUNC_TO_OP[func_name]

        if func_name == "neg":
            if len(node.args) != 1:
                raise ValueError("neg expects 1 argument")
            operand = _parse_func_call(node.args[0])
            return ast.UnaryOp(op=op_type(), operand=operand)

        if len(node.args) != 2:
            raise ValueError(f"{func_name} expects 2 arguments")
        left = _parse_func_call(node.args[0])
        right = _parse_func_call(node.args[1])
        return ast.BinOp(left=left, op=op_type(), right=right)
    raise ValueError(f"Unknown node: {type(node).__name__}")


def form4_to_form1(method_expr: str) -> str:
    result = _parse_method_chain(method_expr)
    return Form1Parser.expr_to_str(result)


def _parse_method_chain(expr_str: str) -> ast.AST:
    parsed = ast.parse(expr_str.strip(), mode="eval").body
    return _walk_method_chain(parsed)


def _walk_method_chain(node: ast.AST) -> ast.AST:
    if isinstance(node, ast.Constant):
        return node
    if isinstance(node, ast.Name):
        return node
    if isinstance(node, ast.Call):
        method_name = node.func.attr if isinstance(node.func, ast.Attribute) else None
        if method_name not in METHOD_TO_OP:
            raise ValueError(f"Unknown method: {method_name}")
        op_type = METHOD_TO_OP[method_name]

        obj = _walk_method_chain(node.func.value)

        if method_name == "__neg__":
            return ast.UnaryOp(op=op_type(), operand=obj)

        if len(node.args) != 1:
            raise ValueError(f"{method_name} expects 1 argument")
        arg = _walk_method_chain(node.args[0])
        return ast.BinOp(left=obj, op=op_type(), right=arg)
    raise ValueError(f"Unknown node: {type(node).__name__}")


def evaluate_form3(func_expr: str, **vars) -> int:
    def make_evaluator(expr_str):
        safe_ops = {
            "add": op_mod.add,
            "sub": op_mod.sub,
            "mul": op_mod.mul,
            "floordiv": op_mod.floordiv,
            "neg": op_mod.neg,
        }
        tree = ast.parse(expr_str, mode="eval")
        def _eval(node):
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.Name):
                if node.id in safe_ops:
                    return safe_ops[node.id]
                return vars[node.id]
            if isinstance(node, ast.Call):
                func = _eval(node.func)
                args = [_eval(a) for a in node.args]
                return func(*args)
            raise ValueError(f"Unknown node: {type(node).__name__}")
        return _eval(tree.body)
    return make_evaluator(func_expr)


def evaluate_form4(method_expr: str, **vars) -> int:
    return eval(method_expr, {"__builtins__": {}}, vars)


def evaluate_form1(expr: str, **vars) -> int:
    return eval(expr, {"__builtins__": {}}, vars)


def reset_temp_counter():
    global _tac_counter
    _tac_counter = 0
