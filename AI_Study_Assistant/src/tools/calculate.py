from langchain.tools import tool
import ast
import operator

@tool
def calculate(expression: str) -> float:
    """Oblicz proste działanie matematyczne, np. 12 * (4 + 3)."""
    print("TOOL calculate został wywołany")

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Wykładnik jest za duży.")

            return allowed_operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))

        raise ValueError("Niedozwolone działanie matematyczne.")

    tree = ast.parse(expression, mode="eval")
    result = evaluate(tree.body)

    if isinstance(result, (int, float)) and abs(result) > 1e100:
        raise ValueError("Wynik jest za duży.")

    return result