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
