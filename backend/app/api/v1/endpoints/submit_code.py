from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.schemas.review import CodeReviewRequest, CodeReviewResponse
from app.core.review_engine import analyze_code
from app.core.pdf_generator import generate_pdf
from app.core.database import SessionLocal
from app.models.code_review import CodeReview

router = APIRouter()

def get_db():
    """
    Provides a SQLAlchemy database session.
    Ensures the session is closed after request handling.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/review", response_model=CodeReviewResponse)
def review_code(request: CodeReviewRequest, db: Session = Depends(get_db)):
    """
    Accepts code, language, and review type from the frontend.
    Performs code analysis using the review engine.
    Generates a PDF report and saves review data to the database.
    
    Args:
        request (CodeReviewRequest): Incoming request with code and metadata.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        CodeReviewResponse: Structured result with suggestions, warnings, score, and downloadable report link.
    """
    result = analyze_code(request.language, request.code)

    # Generate PDF
    pdf_filename = generate_pdf(
        code=request.code,
        language=request.language,
        suggestions=result["suggestions"],
        warnings=result["warnings"],
        optimizations=result["optimizations"],
        score=result["score"],
        remark=result["remark"]
    )

    # Save to DB
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

    result["report_url"] = f"/static/{pdf_filename}"
    return CodeReviewResponse(**result)
