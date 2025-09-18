from pathlib import Path

from fpdf import FPDF
from fpdf.enums import Align

from .text_styles import base_text, link_text, justify_text, center_text

def Sinal(pdf: FPDF, path: str|Path):
    path = Path(path)

    pdf.add_page()
    base_text(pdf)
    pdf.start_section(f"{pdf.section_count}. {path.stem}", 0)
    justify_text(pdf, f"Visualizações referentes ao arquivo {path.stem}.", 0)
    pdf.ln(0)
    pdf.image(path / "time_plot.png", Align.C, h=10, keep_aspect_ratio=True)
    pdf.image(path / "spectograms.png", pdf.epw / 2 - 4.8, h=11, keep_aspect_ratio=True)
    justify_text(pdf, "Os áudios podem ser ouvidos clicando nos links abaixo:")
    link_text(pdf)
    pdf.cell(text="Áudio Original", link=f"file://{path / 'original.mp3'}", align='C')
    pdf.set_x(pdf.x + 2.2)
    pdf.cell(text="Áudio Embaralhado", link=f"file://{path / 'scrambled.mp3'}", align='C')
    pdf.set_x(pdf.x + 2.2)
    pdf.cell(text="Áudio Desembaralhado", link=f"file://{path / 'descrambled.mp3'}", align='C')
    base_text(pdf)