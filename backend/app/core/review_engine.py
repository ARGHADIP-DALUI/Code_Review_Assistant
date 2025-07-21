import re
from typing import List, Dict

def analyze_python_code(code: str) -> Dict[str, List[str]]:
    """
    Analyze Python code for common issues and suggestions.

    Args:
        code (str): The Python source code.

    Returns:
        Dict[str, List[str]]: Contains lists of suggestions, warnings, and optimizations.
    """
    suggestions = []
    warnings = []
    optimizations = []

    # --- Python Rules ---
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
                warnings.append(f"⚠️ Unused import detected: {imp}")

    if re.search(r"for\s+\w+\s+in\s+\w+:\s+\n+\s+\w+\.append\(", code):
        optimizations.append("💡 Consider using list comprehension for better performance.")

    functions = re.findall(r"def\s+\w+\(.*\):", code)
    for fn in functions:
        fn_line_index = code.splitlines().index(fn)
        if not code.splitlines()[fn_line_index + 1].strip().startswith('"""'):
            suggestions.append(f"✅ Add a docstring to function: `{fn.strip()}`")

    return suggestions, warnings, optimizations


def analyze_javascript_code(code: str) -> Dict[str, List[str]]:
    """
    Analyze JavaScript code for common issues and suggestions.

    Args:
        code (str): The JavaScript source code.

    Returns:
        Dict[str, List[str]]: Contains lists of suggestions, warnings, and optimizations.
    """
    suggestions = []
    warnings = []
    optimizations = []

    # --- JavaScript Rules ---
    if "var " in code:
        suggestions.append("✅ Consider using 'let' or 'const' instead of 'var'.")

    if re.search(r"==[^=]", code):
        warnings.append("⚠️ Use '===' for strict equality in JavaScript.")

    if "console.log(" in code:
        optimizations.append("💡 Remove console.log statements in production code.")

    return suggestions, warnings, optimizations


def analyze_code(language: str, code: str) -> Dict[str, List[str] | int | str]:
    """
    Perform a static analysis on code based on its language.

    Args:
        language (str): Programming language ('python' or 'javascript').
        code (str): Source code to review.

    Returns:
        Dict[str, List[str] | int | str]: Suggestions, warnings, optimizations, score, and remark.
    """
    if language.lower() == "python":
        suggestions, warnings, optimizations = analyze_python_code(code)
    elif language.lower() == "javascript":
        suggestions, warnings, optimizations = analyze_javascript_code(code)
    else:
        return {
            "suggestions": ["❌ Language not supported yet."],
            "warnings": [],
            "optimizations": [],
            "score": 0,
            "remark": "Unsupported"
        }

    # Score Calculation
    total = len(suggestions) + len(warnings) + len(optimizations)
    deductions = len(warnings) * 5 + len(suggestions) * 2 + len(optimizations) * 1
    score = max(0, 100 - deductions)

    remark = "Excellent" if score >= 90 else (
        "Good" if score >= 75 else "Needs Improvement"
    )

    return {
        "suggestions": suggestions,
        "warnings": warnings,
        "optimizations": optimizations,
        "score": score,
        "remark": remark
    }
