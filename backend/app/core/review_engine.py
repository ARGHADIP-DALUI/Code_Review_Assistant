import re
from typing import List, Dict, Union

from app.utils.formatter import format_issues  # ✅ Format issues for better UX
from app.utils.style_checker import check_code_style  # ✅ Week 2 integration


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
                warnings.append(f"⚠️ Unused import detected: {imp}")

    # --- List comprehension suggestion ---
    if re.search(r"for\s+\w+\s+in\s+\w+:\s+\n+\s+\w+\.append\(", code):
        optimizations.append("💡 Consider using list comprehension for better performance.")

    # --- Missing docstrings ---
    functions = re.findall(r"def\s+\w+\(.*\):", code)
    for fn in functions:
        fn_line_index = code.splitlines().index(fn)
        if fn_line_index + 1 < len(code.splitlines()):
            if not code.splitlines()[fn_line_index + 1].strip().startswith('"""'):
                suggestions.append(f"✅ Add a docstring to function: `{fn.strip()}`")

    return suggestions, warnings, optimizations


def analyze_javascript_code(code: str) -> Dict[str, List[str]]:
    suggestions = []
    warnings = []
    optimizations = []

    if "var " in code:
        suggestions.append("✅ Consider using 'let' or 'const' instead of 'var'.")
    if re.search(r"==[^=]", code):
        warnings.append("⚠️ Use '===' for strict equality in JavaScript.")
    if "console.log(" in code:
        optimizations.append("💡 Remove console.log statements in production code.")

    return suggestions, warnings, optimizations


def analyze_code(language: str, code: str) -> Dict[str, Union[List[str], int, str]]:
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

    # ✅ Add style issues
    style_result = check_code_style(code, language)
    suggestions += style_result["suggestions"]
    warnings += style_result["warnings"]
    optimizations += style_result["optimizations"]

    # ✅ Format all issues
    formatted_suggestions = format_issues(suggestions)
    formatted_warnings = format_issues(warnings)
    formatted_optimizations = format_issues(optimizations)

    # ✅ Score calculation
    deductions = len(formatted_warnings) * 5 + len(formatted_suggestions) * 2 + len(formatted_optimizations) * 1
    score = max(0, 100 - deductions)

    remark = "Excellent" if score >= 90 else (
        "Good" if score >= 75 else "Needs Improvement"
    )

    return {
        "suggestions": formatted_suggestions,
        "warnings": formatted_warnings,
        "optimizations": formatted_optimizations,
        "score": score,
        "remark": remark
    }

