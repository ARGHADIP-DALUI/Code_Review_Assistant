from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(code: str, language: str, suggestions: list, warnings: list, optimizations: list, score: int, remark: str) -> str:
    filename = "code_review_report.pdf"
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
    return filename
