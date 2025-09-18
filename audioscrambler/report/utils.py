from fpdf import FPDF

def line_space(pdf: FPDF, n_lines: int):
    for _ in range(n_lines):
        pdf.ln()