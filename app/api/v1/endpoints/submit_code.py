from fastapi import APIRouter
from app.api.v1.schemas.review import CodeReviewRequest, CodeReviewResponse
from app.core.review_engine import analyze_code

router = APIRouter()

@router.post("/review", response_model=CodeReviewResponse)
def review_code(request: CodeReviewRequest):
    result = analyze_code(request.language, request.code)
    return CodeReviewResponse(**result)
