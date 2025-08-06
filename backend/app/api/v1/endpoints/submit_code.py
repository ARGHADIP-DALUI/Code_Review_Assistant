# app/api/v1/endpoints/submit_code.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.schemas.review import CodeReviewRequest, CodeReviewResponse
from app.core.review_engine import analyze_code
from app.core.pdf_generator import generate_review_pdf
from app.core.database import SessionLocal
from app.models.code_review import CodeReview
from app.utils.bug_detector import detect_bugs
from app.utils.gpt_logic_checker import detect_logic_flaws  # ✅ NEW: Logic flaw detector

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/review", response_model=CodeReviewResponse)
def review_code(request: CodeReviewRequest, db: Session = Depends(get_db)):
    # 🔍 Static + Style analysis
    result = analyze_code(request.language, request.code)

    # 🐞 Detect bugs
    bugs = detect_bugs(request.code)

    # 🤖 Detect logic flaws
    logic_flaws = detect_logic_flaws(request.code)

    # 📌 Keep bugs separate; merge logic flaws into warnings
    result["bugs"] = bugs
    result["warnings"].extend(logic_flaws)

    # 📝 Generate PDF report with bugs
    pdf_filename = generate_review_pdf(
        code=request.code,
        language=request.language,
        suggestions=result["suggestions"],
        warnings=result["warnings"],
        optimizations=result["optimizations"],
        bugs=result["bugs"],  # ✅ Include bug list in PDF
        score=result["score"],
        remark=result["remark"]
    )

    # 💾 Save to database
    review_record = CodeReview(
        code=request.code,
        language=request.language,
        suggestions="\n".join(result["suggestions"]),
        warnings="\n".join(result["warnings"]),
        optimizations="\n".join(result["optimizations"]),
        score=result["score"],
        remark=result["remark"]
        # Optional: Add bugs/logic_flaws in DB if needed
    )
    db.add(review_record)
    db.commit()

    # 🌐 Set downloadable PDF link
    result["report_url"] = f"/static/{pdf_filename}"

    # ✅ Return response with all fields
    return CodeReviewResponse(**result)
