import re

# Cache dictionary to store results
style_cache = {}

# Local app imports (after standard library imports)
from app.utils.formatter import format_issues


def format_issues(raw_issues: list[str]) -> list[str]:
    formatted = []
    for issue in raw_issues:
        if "exceeds 79 characters" in issue:
            formatted.append("📏 Line too long: Try keeping lines under 79 characters for better readability.")
        elif "tab character" in issue:
            formatted.append("🔧 Replace tab characters with 4 spaces for consistent indentation.")
        elif "Add a space after '#'" in issue:
            formatted.append("💡 Consider adding a space after '#' to improve comment readability.")
        elif "File should end with a newline" in issue:
            formatted.append("📄 Add a newline at the end of the file to follow POSIX standards.")
        elif "snake_case" in issue:
            formatted.append("🔧 Rename variable or function to snake_case for consistency.")
        elif "Indentation not a multiple of 4" in issue:
            formatted.append("⚠️ Use consistent indentation of 4 spaces.")
        else:
            formatted.append(issue)
    return formatted


def check_code_style(code: str, language: str) -> dict:
    # ✅ Return cached result if code was already checked
    if code in style_cache:
        return style_cache[code]

    suggestions = []
    warnings = []
    optimizations = []

    if language.lower() == "python":
        lines = code.split("\n")
        for i, line in enumerate(lines):
            if len(line) > 79:
                warnings.append(f"Line {i+1}: exceeds 79 characters.")
            if "\t" in line:
                warnings.append(f"Line {i+1}: contains tab character. Use 4 spaces instead.")
            if line.strip().startswith("#") and not line.strip().startswith("# "):
                suggestions.append(f"Line {i+1}: Add a space after '#' in comments.")
            leading_spaces = len(line) - len(line.lstrip(' '))
            if leading_spaces and leading_spaces % 4 != 0:
                warnings.append(f"Line {i+1}: Indentation not a multiple of 4 spaces.")

        if not code.endswith("\n"):
            suggestions.append("File should end with a newline.")

        var_func_names = re.findall(r"def\s+([a-zA-Z0-9_]+)\s*\(|([a-zA-Z0-9_]+)\s*=", code)
        for func_name, var_name in var_func_names:
            name = func_name or var_name
            if name and not re.match(r"^[a-z_][a-z0-9_]*$", name):
                suggestions.append(f"🔧 Rename '{name}' to follow snake_case.")

    else:
        warnings.append(f"Style check for {language} not supported yet.")

    formatted_suggestions = format_issues(suggestions)
    formatted_warnings = format_issues(warnings)
    formatted_optimizations = format_issues(optimizations)

    result = {
        "suggestions": formatted_suggestions,
        "warnings": formatted_warnings,
        "optimizations": formatted_optimizations,
        "score": max(0, 100 - (len(suggestions)*2 + len(warnings)*3)),
        "remark": "Good job!" if len(suggestions) + len(warnings) <= 2 else "Needs improvement"
    }

    # ✅ Store result in cache
    style_cache[code] = result
    return result



