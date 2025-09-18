from pathlib import Path

from fpdf import FPDF
from fpdf.outline import TableOfContents

from .Capa import Capa
from .Sumario import Sumario
from .Intro import Intro
from .Metodos import Metodos
from .Sinal import Sinal
from .Conclusao import Conclusao
from .text_styles import section_title_text

class Report(FPDF):
    def __init__(self, author: str, title: str):
        super().__init__(format="A4", unit="cm")
        self.toc = TableOfContents(level_indent=.5, use_section_title_styles=True)
        self.author = author
        self.title = title
        self._section_count = 0

        self.set_title(title)
        self.set_author(author)
        self.set_lang("pt-BR")
        self.set_auto_page_break(auto=True, margin=2)
        section_title_text(self)

        Capa(self)
        Sumario(self)
        Intro(self)
        Metodos(self)
        
        Sinal(self, Path("outputs/Chirp").absolute())
        for out_dir in filter(lambda x: x.stem != "Chirp", sorted(Path("outputs").glob("*"))):
            Sinal(self, out_dir.absolute())
        
        Conclusao(self)
        
    @property
    def section_count(self):
        self._section_count += 1
        return self._section_count
    
    @property
    def actual_section(self):
        return self._section_count

    def header(self):
        label = self.get_page_label()
        if (self.page_no() == 1) or (label.startswith("Sum")):
            return
        self.set_xy(-3, 1.5)
        self.set_font("times", size=12)
        self.write(text=f"{label}")
    
    def add_page(self, label_style = None, label_prefix = None, label_start = None, **kwargs):
        super().add_page(
            label_style=label_style,
            label_prefix=label_prefix,
            label_start=label_start,
            **kwargs
        )
        self.set_top_margin(3)
        self.set_left_margin(3)
        self.set_right_margin(2)
        self.set_y(3)