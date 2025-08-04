def format_suggestion(raw_msg: str) -> str:
    """
    Dummy formatter to convert technical linting messages into readable suggestions.
    """
    if "missing-function-docstring" in raw_msg:
        return "✏️ Add a docstring to describe the function’s purpose."
    elif "unused-import" in raw_msg:
        return "🧹 Remove unused import to keep the code clean."
    elif "line-too-long" in raw_msg:
        return "📏 Break long lines to keep under 79 characters."
    elif "invalid-name" in raw_msg:
        return "🔤 Consider renaming variables to follow naming conventions."
    else:
        return raw_msg  # fallback for unknown messages
