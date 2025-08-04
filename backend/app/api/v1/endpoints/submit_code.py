from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.schemas.review import CodeReviewRequest, CodeReviewResponse
from app.core.review_engine import analyze_code
from app.core.pdf_generator import generate_review_pdf  # ✅ Updated import
from app.core.database import SessionLocal
from app.models.code_review import CodeReview

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/review", response_model=CodeReviewResponse)
def review_code(request: CodeReviewRequest, db: Session = Depends(get_db)):
    result = analyze_code(request.language, request.code)

    # ✅ Generate PDF report using the new function
    pdf_filename = generate_review_pdf(
        code=request.code,
        language=request.language,
        suggestions=result["suggestions"],
        warnings=result["warnings"],
        optimizations=result["optimizations"],
        score=result["score"],
        remark=result["remark"]
    )

    # ✅ Save review to database
    review_record = CodeReview(
        code=request.code,
        language=request.language,
        suggestions="\n".join(result["suggestions"]),
        warnings="\n".join(result["warnings"]),
        optimizations="\n".join(result["optimizations"]),
        score=result["score"],
        remark=result["remark"]
    )
    db.add(review_record)
    db.commit()

    # ✅ Include PDF file path in API response
    result["report_url"] = f"/static/{pdf_filename}"
    return CodeReviewResponse(**result)

