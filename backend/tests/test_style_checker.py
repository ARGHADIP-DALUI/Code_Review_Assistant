import pytest
from app.utils.style_checker import check_code_style, style_cache

def test_clean_code():
    code = "def add(a, b):\n    return a + b\n"
    result = check_code_style(code, "python")
    assert result["suggestions"] == []
    assert result["warnings"] == []
    assert result["score"] == 100
    assert result["remark"] == "Good job!"

def test_code_with_warnings_and_suggestions():
    code = (
        "def Add(a,b):\n"
        "  return a+b\n"
        "#badcomment\n"
        "print(Add(3,4))\n"
    )
    result = check_code_style(code, "python")
    assert any("🔧 Rename" in s for s in result["suggestions"])
    assert any("💡 Consider adding a space" in s for s in result["suggestions"])
    assert any("⚠️ Use consistent indentation" in w for w in result["warnings"])
    assert result["score"] < 100
    assert result["remark"] == "Needs improvement"

def test_long_lines_and_tabs():
    code = (
        "def test():\n"
        "\tprint('This is a very long line that exceeds seventy-nine characters for testing purposes...')\n"
    )
    result = check_code_style(code, "python")
    assert any("📏 Line too long" in w for w in result["warnings"])
    assert any("🔧 Replace tab characters" in w for w in result["warnings"])

def test_style_cache():
    code = "def cached_func():\n    return 42\n"
    style_cache.clear()  # Clear cache before test
    first = check_code_style(code, "python")
    assert code in style_cache
    second = check_code_style(code, "python")
    assert first == second  # Cached result matches
