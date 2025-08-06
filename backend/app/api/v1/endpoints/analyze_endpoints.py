from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.utils.bug_detector import detect_bugs
from app.core.review_engine import analyze_python_code

router = APIRouter()

class CodeInput(BaseModel):
    code: str
    language: str = "python"

@router.post("/analyze/bugs")
def analyze_bugs(input: CodeInput):
    bugs = detect_bugs(input.code)
    return {"bugs": bugs}

@router.post("/analyze/optimize")
def analyze_optimizations(input: CodeInput):
    suggestions, warnings, optimizations = analyze_python_code(input.code)
    return {"optimizations": optimizations}
