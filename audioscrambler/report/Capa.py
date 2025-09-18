import locale
from datetime import date

from fpdf import FPDF

from .utils import line_space
from .text_styles import base_text, title_text, center_text

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

def Capa(pdf: type['Report']):
    author = pdf.author
    title = pdf.title

    pdf.add_page(label_prefix="Capa")
    base_text(pdf)
    center_text(pdf, 
                "Universidade Federal de Santa Catarina - UFSC\n" +
                "Departamento de Engenharia Elétrica e Eletrônica"
    )
    line_space(pdf, 3)
    center_text(pdf, author)
    line_space(pdf, 8)

    title_text(pdf)
    center_text(pdf, title)
    line_space(pdf, 12)

    base_text(pdf)
    month_str = date.today().strftime("%b")
    month_str = month_str.title()
    center_text(pdf, 
                "Santa Catarina - SC\n" +
                date.today().strftime("%Y") + f"/{month_str}"
    )