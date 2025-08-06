# app/utils/gpt_logic_checker.py

import ast
import re
from typing import List

def detect_logic_flaws(code: str) -> List[str]:
    """
    Heuristic “logic flaw” detector:
      - Flags functions called with wrong number of args
      - Marks unreachable code after a return
      - Detects assignments in `if` instead of comparisons

    Returns a list of human-friendly messages.
    """
    flaws: List[str] = []

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return ["❌ Syntax error in code; unable to analyze logic."]

    # 1) Map each function name → expected arg count
    func_arg_counts = {
        node.name: len(node.args.args)
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    }

    # 2) Scan for calls with wrong arg count
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if name in func_arg_counts:
                expected = func_arg_counts[name]
                actual = len(node.args)
                if actual != expected:
                    flaws.append(
                        f"🤖 Logic flaw: function '{name}' called with {actual} args "
                        f"(expected {expected})."
                    )

    # 3) Unreachable code after a return inside functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # find first return
            for i, stmt in enumerate(node.body[:-1]):
                if isinstance(stmt, ast.Return):
                    flaws.append(
                        f"🤖 Unreachable code detected after `return` in function '{node.name}'."
                    )
                    break  # only report once per function

    # 4) Assignment in if (common typo: = instead of ==)
    if re.search(r"\bif\s+[^=]+=[^=].*:", code):
        flaws.append(
            "🤖 Possible assignment in `if` statement (did you mean '==' instead of '='?)."
        )

    return flaws
