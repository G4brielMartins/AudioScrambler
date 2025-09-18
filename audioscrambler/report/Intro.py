from fpdf import FPDF

from .text_styles import base_text, justify_text

def Intro(pdf: type['Report']):
    base_text(pdf)
    pdf.ln(0)
    pdf.start_section(f"{pdf.section_count}. Introdução", level=0)
    justify_text(pdf,
"""    Este relatório apresenta o desenvolvimento e aplicação de um sistema de \
embaralhamento de voz. Serão descritos os métodos utilizados, a ferramenta \
desenvolvida e seu uso, os testes realizados e os resultados obtidos.""")
    pdf.start_section(f"{pdf.actual_section}.1 Sistema de Embaralhamento", level=1)
    justify_text(pdf, ln=0, text=
"""    O sistema de embaralhamento de voz utilizado baseia-se no deslocamento do \
sinal por frequências específicas, acompanhado da aplicação de filtros segundo \
o seguinte diagrama:""")
    pdf.ln(0)
    pdf.image("figures/diagrama_sistema.png", w=pdf.epw, keep_aspect_ratio=True)
    
    justify_text(pdf,
"""    Onde, considerando m(t) um sinal em banda base com largura 5kHz:
    - m(t) é deslocado até 20kHz;
    - A cópia do sinal m(t) vinda das frequências negativas é removida por um \
filtro passa altas em 20kHz;
    - O sinal é deslocado em 25kHz, trazendo o espelho de x2(t) das frequências \
negativas até o intervalo 0-5kHz;
    - Um filtro passa baixas elimina as altas frequências resultantes do \
deslocamento de 25kHz aplicado à parte do sinal em torno de 20kHz;
    - Por fim, obtém-se a faixa entre 0-5kHz de m(t), espelhada em relação ao \
eixo da amplitude.""")
    
    pdf.start_section(f"{pdf.actual_section}.2 Amostragem", level=1)
    justify_text(pdf,
"""    O sistema descrito para embaralhamento de sinais conta com multiplicações de \
sinais em torno de 25kHz. Entretanto, arquivos de áudio costumam ser salvos com amostragem na faixa \
de 44,1kHz, o que, pelo __Teorema da Amostragem__, pode gerar perdas de informação na \
aplicação do sistema (frequências acima de 22,05kHz são geradas durante as transformações). Portanto, \
é necessário empregar o processo de __upsampling__ para contornar o problema.
    Realizar __upsampling__ consiste em gerar amostras sintéticas entre os pontos \
conhecidos, de modo a aumentar a taxa de amostragem do sinal. Para isso, os seguintes \
passos são realizados sobre o sinal:
    1. Calcula-se a razão L entre a frequência atual e a desejada, arredondando para \
o inteiro imediamente superior;
    2. Inserem-se L - 1 zeros entre cada amostra do sinal original;
    3. Um filtro passa baixas é aplicado para suavizar as descontínuidades. Conhecido \
como filtro de interpolação, ele substitui os zeros com base em amostras vizinhas.""")