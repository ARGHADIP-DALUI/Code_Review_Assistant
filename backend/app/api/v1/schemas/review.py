from pydantic import BaseModel
from typing import List

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    review_type: str = "basic"

class CodeReviewResponse(BaseModel):
    suggestions: List[str]
    warnings: List[str]
    optimizations: List[str]
    bugs: List[str]  # ✅ Added bug list to response schema
    score: int
    remark: str
    report_url: str  # ✅ Link to download PDF report

