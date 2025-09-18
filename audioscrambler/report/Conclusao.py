from fpdf import FPDF

from .text_styles import base_text, justify_text

def Conclusao(pdf: FPDF):
    pdf.add_page()
    
    base_text(pdf)
    pdf.start_section(f"{pdf.section_count}. Conclusão", 0)
    justify_text(pdf,
"""    O sistema de embaralhamento e desembaralhamento de sinais de áudio foi implementado com sucesso. \
Através da utilização de técnicas de processamento de sinais, foi possível atingir \
os objetivos propostos no início do projeto. Entretanto, dada a banda estreita em que o sistema opera, a qualidade do áudio processado é afetada, \
principalmente a parte instrumental ou eletrônica dos sinais de áudio. Assim, embora funcione corretamente (principalmente \
com vozes humanas), as frequências mais agudas do espectro não são preservadas e um ruído perceptível é introduzido.
    Enquanto os espectros dos sinais exibem diferenças notáveis após aplicação do embaralhamento e desembaralhamento, \
a representação de cada sinal no domínio do tempo permanece visualmente similar. 
    Ainda, os algoritmos de __upsampling__ e __downsampling__ implementados foram efetivos e possibilitaram, com \
áuxilio de ferramentas de codificação e decodificação de áudio, o tratamento local dos arquivos e seus sinais.""")