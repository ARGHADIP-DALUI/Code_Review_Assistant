import re
from typing import List, Dict

def analyze_python_code(code: str) -> Dict[str, List[str]]:
    suggestions = []
    warnings = []
    optimizations = []

    # Rule 1: Check for unused imports
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

    # Rule 2: Suggest using list comprehension
    if re.search(r"for\s+\w+\s+in\s+\w+:\s+\n+\s+\w+\.append\(", code):
        optimizations.append("💡 Consider using list comprehension for better performance.")

    # Rule 3: Missing function docstrings
    functions = re.findall(r"def\s+\w+\(.*\):", code)
    for fn in functions:
        fn_line_index = code.splitlines().index(fn)
        if not code.splitlines()[fn_line_index + 1].strip().startswith('"""'):
            suggestions.append(f"✅ Add a docstring to function: `{fn.strip()}`")

    return {
        "suggestions": suggestions,
        "warnings": warnings,
        "optimizations": optimizations
    }
