from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import ast

router = APIRouter()

class StyleCheckRequest(BaseModel):
    code: str

class StyleCheckResponse(BaseModel):
    issues: List[str]

@router.post("/check-style", response_model=StyleCheckResponse)
async def check_style(request: StyleCheckRequest):
    code = request.code
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Syntax error in code: {e}")
    
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not ast.get_docstring(node):
                issues.append(f"Function '{node.name}' is missing a docstring.")
        elif isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                issues.append(f"Class '{node.name}' is missing a docstring.")
    
    return StyleCheckResponse(issues=issues)
