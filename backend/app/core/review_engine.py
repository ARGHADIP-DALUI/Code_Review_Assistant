import re
import ast
from typing import List, Dict, Union

from app.utils.formatter import format_issues
from app.utils.style_checker import check_code_style
from app.utils.bug_detector import detect_bugs


def analyze_python_code(code: str) -> Dict[str, List[str]]:
    suggestions = []
    warnings = []
    optimizations = []

    # --- Unused imports ---
    if "import " in code:
        lines = code.split("\n")
        used_names = set()
        imports = {}
        for line in lines:
            if line.strip().startswith("import ") or line.strip().startswith("from "):
                import_name = line.split()[1]
                imports[import_name] = line
            else:
                for word in line.split():
                    used_names.add(word)
        for imp in list(imports.keys()):
            if imp not in used_names:
                warnings.append(f"⚠️ Unused import detected: {imp} (low impact)")

    # --- List comprehension suggestion ---
    if re.search(r"for\s+\w+\s+in\s+\w+:\s+\n+\s+\w+\.append\(", code):
        optimizations.append("💡 Use list comprehension instead of .append() — improves performance (medium impact)")

    # --- Missing docstrings ---
    functions = re.findall(r"def\s+\w+\(.*\):", code)
    for fn in functions:
        fn_line_index = code.splitlines().index(fn)
        if fn_line_index + 1 < len(code.splitlines()):
            if not code.splitlines()[fn_line_index + 1].strip().startswith('"""'):
                suggestions.append(f"✅ Add a docstring to function: `{fn.strip()}` (low impact)")

    # --- AST-based performance issues ---
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            # ✅ Nested loops
            if isinstance(node, ast.For):
                for inner in ast.iter_child_nodes(node):
                    if isinstance(inner, ast.For):
                        optimizations.append(
                            "💡 Nested loops detected — consider optimizing or using vectorized operations (high impact)"
                        )

            # ✅ Repeated computations inside loops
            if isinstance(node, ast.For):
                for stmt in node.body:
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.BinOp):
                        optimizations.append(
                            "💡 Repeated computation inside loop — move invariant code outside loop if possible (medium impact)"
                        )
                        break

            # ✅ Magic numbers
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)) and node.value not in (0, 1):
                    optimizations.append(
                        f"💡 Magic number `{node.value}` found — define as constant or config (low impact)"
                    )
                    break

    except Exception:
        warnings.append("⚠️ Unable to parse code fully for deep optimization suggestions. (low impact)")

    return suggestions, warnings, optimizations


def analyze_javascript_code(code: str) -> Dict[str, List[str]]:
    suggestions = []
    warnings = []
    optimizations = []

    if "var " in code:
        suggestions.append("✅ Consider using 'let' or 'const' instead of 'var' (medium impact)")
    if re.search(r"==[^=]", code):
        warnings.append("⚠️ Use '===' for strict equality in JavaScript (medium impact)")
    if "console.log(" in code:
        optimizations.append("💡 Remove console.log statements in production code (low impact)")

    return suggestions, warnings, optimizations


def analyze_code(language: str, code: str) -> Dict[str, Union[List[str], int, str]]:
    if language.lower() == "python":
        suggestions, warnings, optimizations = analyze_python_code(code)
        bugs = detect_bugs(code)
    elif language.lower() == "javascript":
        suggestions, warnings, optimizations = analyze_javascript_code(code)
        bugs = []  # JS bug detection not implemented
    else:
        return {
            "suggestions": ["❌ Language not supported yet."],
            "warnings": [],
            "optimizations": [],
            "bugs": [],
            "score": 0,
            "remark": "Unsupported"
        }

    # ✅ Style check
    style_result = check_code_style(code, language)
    suggestions += [s + " (low impact)" for s in style_result["suggestions"]]
    warnings += [w + " (medium impact)" for w in style_result["warnings"]]
    optimizations += [o + " (low impact)" for o in style_result["optimizations"]]

    # ✅ Format all
    formatted_suggestions = format_issues(suggestions)
    formatted_warnings = format_issues(warnings)
    formatted_optimizations = format_issues(optimizations)
    formatted_bugs = format_issues(bugs)

    # ✅ Score calculation
    deductions = (
        len(formatted_warnings) * 5 +
        len(formatted_suggestions) * 2 +
        len(formatted_optimizations) * 1 +
        len(formatted_bugs) * 3
    )
    score = max(0, 100 - deductions)

    remark = (
        "Excellent" if score >= 90 else
        "Good" if score >= 75 else
        "Average" if score >= 60 else
        "Needs Improvement"
    )

    return {
        "suggestions": formatted_suggestions,
        "warnings": formatted_warnings,
        "optimizations": formatted_optimizations,
        "bugs": formatted_bugs,
        "score": score,
        "remark": remark
    }
