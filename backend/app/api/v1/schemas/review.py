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
    score: int
    remark: str
    report_url: str  # 🆕 Add download link field
