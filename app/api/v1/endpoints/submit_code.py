from fastapi import APIRouter
from app.api.v1.schemas.review import CodeReviewRequest, CodeReviewResponse
from app.core.review_engine import analyze_code
from app.core.pdf_generator import generate_pdf  # 🆕 Import PDF generator

router = APIRouter()

@router.post("/review", response_model=CodeReviewResponse)
def review_code(request: CodeReviewRequest):
    result = analyze_code(request.language, request.code)

    # 🆕 Generate PDF
    pdf_filename = generate_pdf(
        code=request.code,
        language=request.language,
        suggestions=result["suggestions"],
        warnings=result["warnings"],
        optimizations=result["optimizations"],
        score=result["score"],
        remark=result["remark"]
    )

    result["report_url"] = f"/static/{pdf_filename}"  # 🆕 Add report URL
    return CodeReviewResponse(**result)
