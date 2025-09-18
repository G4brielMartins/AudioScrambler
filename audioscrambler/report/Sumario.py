from fpdf import FPDF
from fpdf.outline import TableOfContents

from .text_styles import title_text, center_text

def Sumario(pdf: type['Report']):
    toc: TableOfContents = pdf.toc

    pdf.add_page("D", "Sumário - ", 1)
    title_text(pdf)
    center_text(pdf, "Sumário", ln=0)
    pdf.set_page_label("D", "", 2)
    pdf.insert_toc_placeholder(toc.render_toc, allow_extra_pages=True)