from fpdf import FPDF, TextStyle

from .utils import line_space

def base_text(pdf: FPDF):
    pdf.set_font("times", size=12)
    pdf.set_text_color(0, 0, 0)

def title_text(pdf: FPDF):
    pdf.set_font("times", style="B", size=16)

def link_text(pdf: FPDF):
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("times", style="U", size=12)

def section_title_text(pdf: FPDF):
    pdf.set_section_title_styles(
        TextStyle('times', 'B', 12, l_margin=0),
        TextStyle('times', 'B', 12, l_margin=0),
        TextStyle('times', 'B', 12, l_margin=0)
    )

def center_text(pdf: FPDF, text: str, ln: int = 1):
    pdf.multi_cell(0, 1.5*pdf.font_size, text, align="C", markdown=True)
    line_space(pdf, ln)

def justify_text(pdf: FPDF, text: str, ln: int = 1):
    pdf.multi_cell(0, 1.5*pdf.font_size, text, align="J", markdown=True)
    line_space(pdf, ln)