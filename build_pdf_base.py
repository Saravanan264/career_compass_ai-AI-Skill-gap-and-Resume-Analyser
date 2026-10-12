import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define Palette
NAVY = colors.HexColor("#0F172A")       # Slate 900
INDIGO = colors.HexColor("#4F46E5")     # Indigo 600
TEAL = colors.HexColor("#0D9488")       # Teal 600
SLATE_BG = colors.HexColor("#F8FAFC")   # Slate 50
TEXT_DARK = colors.HexColor("#1E293B")  # Slate 800
BORDER_COLOR = colors.HexColor("#CBD5E1") # Slate 300
AMBER = colors.HexColor("#D97706")      # Amber 600
WHITE = colors.HexColor("#FFFFFF")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress header/footer on title page if needed, but here we include running header on page > 1
        if self._pageNumber > 1:
            # Header line and text
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(INDIGO)
            self.drawString(36, 762, "CAREER COMPASS AI")
            self.setFont("Helvetica", 8)
            self.setFillColor(TEXT_DARK)
            self.drawString(130, 762, "|  Complete Technical Interview Documentation")
            
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(36, 754, 576, 754)
            
            # Footer
            self.line(36, 45, 576, 45)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 32, "Confidential - Technical Interview Defense Guide")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(576, 32, page_text)
        else:
            # First page subtle footer
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(36, 45, 576, 45)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 32, "Career Compass AI Codebase Documentation")
            page_text = f"Page 1 of {page_count}"
            self.drawRightString(576, 32, page_text)

        self.restoreState()

print("NumberedCanvas class ready.")
