from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import time
from typing import List

def generate_review_pdf(
    code: str,
    language: str,
    suggestions: List[str],
    warnings: List[str],
    optimizations: List[str],
    bugs: List[str],
    score: int,
    remark: str
) -> str:
    # ✅ Generate unique filename using timestamp
    timestamp = int(time.time())
    filename = f"code_review_report_{timestamp}.pdf"
    filepath = os.path.join("app", "static", filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Code Review Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Language: {language}")
    c.drawString(50, height - 100, f"Score: {score} ({remark})")

    y = height - 130

    def draw_section(title, items):
        nonlocal y
        if not items:
            return
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, title)
        y -= 20
        c.setFont("Helvetica", 12)
        for item in items:
            c.drawString(60, y, f"- {item}")
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50

    draw_section("Suggestions", suggestions)
    draw_section("Warnings", warnings)
    draw_section("Optimizations", optimizations)
    draw_section("Detected Bugs", bugs)

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Submitted Code:")
    y -= 20
    c.setFont("Courier", 10)
    for line in code.splitlines():
        c.drawString(60, y, line)
        y -= 12
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return filename  # ✅ Return unique filename
