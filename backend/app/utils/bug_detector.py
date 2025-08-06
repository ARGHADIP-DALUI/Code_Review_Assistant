# app/utils/bug_detector.py

import ast
from typing import List, Dict

def detect_bugs(code: str) -> List[Dict[str, str]]:
    bugs = []

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            # Bug 1: Using 'sum' as variable
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'sum':
                        bugs.append({
                            "message": "Avoid using 'sum' as a variable (shadows built-in).",
                            "severity": "medium",
                            "tip": "Using 'sum' as a variable name overrides Python’s built-in sum() function, which can cause unexpected behavior."
                        })

            # Bug 2: Unused pass
            if isinstance(node, ast.Pass):
                bugs.append({
                    "message": "Consider removing unused 'pass' statement (possible dead code).",
                    "severity": "low",
                    "tip": "'pass' can be removed unless you're using it as a placeholder for future code."
                })

    except SyntaxError:
        bugs.append({
            "message": "Syntax Error in code. Unable to parse.",
            "severity": "high",
            "tip": "Check for typos or indentation issues in your code."
        })

    return bugs
