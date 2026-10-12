import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from build_pdf_base import NumberedCanvas, NAVY, INDIGO, TEAL, SLATE_BG, TEXT_DARK, BORDER_COLOR, AMBER, WHITE
from pdf_sections_part1 import add_part1_sections
from pdf_sections_part2 import add_part2_sections
from pdf_sections_part3 import add_part3_sections

def build_pdf():
    pdf_filename = "Career_Compass_AI_Technical_Interview_Documentation.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Paragraph Styles
    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=NAVY,
        spaceAfter=4
    ))
    
    styles.add(ParagraphStyle(
        name='SecHeading',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=INDIGO,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='NormalText',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='CalloutText',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK
    ))

    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=WHITE
    ))

    styles.add(ParagraphStyle(
        name='TableText',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    ))

    styles.add(ParagraphStyle(
        name='CodeText',
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    ))

    story = []

    print("Adding Part 1 (Sections 1-10)...")
    add_part1_sections(story, styles, NAVY, INDIGO, TEAL, SLATE_BG, TEXT_DARK, BORDER_COLOR, AMBER, WHITE)

    print("Adding Part 2 (Sections 11-20)...")
    add_part2_sections(story, styles, NAVY, INDIGO, TEAL, SLATE_BG, TEXT_DARK, BORDER_COLOR, AMBER, WHITE)

    print("Adding Part 3 (Sections 21-31)...")
    add_part3_sections(story, styles, NAVY, INDIGO, TEAL, SLATE_BG, TEXT_DARK, BORDER_COLOR, AMBER, WHITE)

    print("Building Document Canvas...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
