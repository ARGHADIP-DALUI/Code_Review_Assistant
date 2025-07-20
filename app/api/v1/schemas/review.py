from pydantic import BaseModel

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    review_type: str = "basic"
