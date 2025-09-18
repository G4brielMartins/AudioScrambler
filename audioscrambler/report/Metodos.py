from fpdf import FPDF, Align

from .text_styles import base_text, justify_text

def Metodos(pdf: FPDF):
    pdf.add_page()
    
    base_text(pdf)
    pdf.start_section(f"{pdf.section_count}. Metodologia", 0)
    justify_text(pdf,
"""    Para aplicar as devidas transformações nos sinais de áudio, foi desenvolvida a \
ferramenta Audio Scrambler, que é distribuída junto a este relatório.
    Para utilizar a ferramenta, basta adicionar os arquivos de áudio de interesse no \
diretório "./samples" e executar o script "run.py". Após a execução, imagens e áudios dos \
sinais serão gerados na pasta "./output", organizados por arquivo de áudio de referência. \
Os links para arquivos locais presentes neste PDF podem deixar de funcionar caso o PDF seja \
aberto em um __browser__ e, neste caso, os áudios gerados devem ser acessados diretamente em "./output".
    Os arquivos gerados serão espectograma, representação no tempo e áudios em formato ".wav". \
Cada arquivo terá informações referentes ao sinal original após __upsampling__ (m(t)), sinal \
embaralhado (y(t)) e sinal desembaralhado (m_rec(t)). Ainda, este relatório será atualizado \
após o processamento, incluindo seções referentes a cada arquivo de entrada.
    Atente-se que algumas etapas de processamento exigem filtros de ordem elevada, o que, \
combinado com a alta taxa de amostragem, pode levar a um processamento lento - proporcional \
a quantidade de áudios a serem processados.""")
    
    pdf.start_section(f"{pdf.actual_section}.1 Importação", 1)
    justify_text(pdf,
"""    A importação dos áudios é realizada com auxílio da ferramenta __ffmpeg__, de modo \
que formatos de áudio diversos são aceitos. Caso haja algum problema com os arquivos de \
entrada, por favor converta o arquivo para um dos formatos testados durante o desenvolvimento: \
MP3 ou WAV.""")
    
    pdf.start_section(f"{pdf.actual_section}.2 Upscaling", 1)
    justify_text(pdf,
"""    Para realizar o __upscaling__ do áudio de entrada, o filtro de interpolação \
utilizado foi uma arquitetura Butterworth passa baixas de quinta ordem, projetado para a \
frequência de Nyquist do sinal de entrada. Como a banda efetiva para aplicação do embaralhamento \
(0-5kHz) ocorre distante da frequência de corte do filtro (geralmente 22kHz), sua seletividade \
é reduzida e sua ordem pode ser pequena.
    A ferramenta desenvolvida é configurada por padrão para realizar o __upscaling__ para \
96kHz, mas também pode trabalhar com outras taxas de amostragem. A configuração desta taxa \
pode ser realizada no arquivo "run.py".""")
    
    pdf.start_section(f"{pdf.actual_section}.3 Embaralhamento - Modulação", 1)
    justify_text(pdf,
"""    Para aplicar o sistema de embaralhamento, foram gerados cossenos de 20kHz e 25kHz a partir \
de um vetor de tempo. O deslocamento de frequências foi obtido pela multiplicação direta dos sinais \
com esses cossenos.
    Quanto aos filtros projetados, a arquitetura utilizada foi Butterworth com frequência de corte 20kHz \
tanto para o filtro passa baixas quanto passa altas. Entretanto, diferente do filtro de interpolação, a \
seletividade deste filtro é alta, devendo atenuar frequências imediamente após a frequência de corte.
    Diferentes configurações foram testadas e, a partir da observação de espectogramas dos sinais gerados \
pelo sistema a partir de uma função chirp, resultados aceitáveis foram obtidos da ordem 100 em diante. Foi \
escolhido um filtro Butterworth de ordem 150 para reduzir ainda mais a banda de transição.
    A partir dos sinais e filtros descritos, as etapas do sistema de embaralhamento foram aplicadas:
    0. Utilizando uma função __chirp__ de 20 a 5kHz como sinal de entrada m(t):""")
    pdf.image("figures/m_t.png", Align.C, w=pdf.epw)
    pdf.ln()
    justify_text(pdf, "1. Multiplicação do sinal m(t) pelo cosseno de 20kHz, obtendo o sinal x1(t):")
    pdf.image("figures/x1_t.png", Align.C, w=pdf.epw)
    pdf.ln()
    justify_text(pdf, "2. Filtragem de x1(t) pelo filtro passa altas com frequência de corte 20kHz, obtendo o sinal x2(t):")
    pdf.image("figures/x2_t.png", Align.C, w=pdf.epw)
    pdf.ln()
    justify_text(pdf, "3. Multiplicação do sinal m(t) pelo cosseno de 25kHz, obtendo o sinal x3(t):")
    pdf.image("figures/x3_t.png", Align.C, w=pdf.epw)
    pdf.ln()
    justify_text(pdf, "4. Filtragem de x3(t) pelo filtro passa baixas com frequência de corte 20kHz, obtendo o sinal y(t):")
    pdf.image("figures/y_t.png", Align.C, w=pdf.epw)
    pdf.ln()
    pdf.start_section(f"{pdf.actual_section}.4 Desembaralhamento - Demodulação", 1)
    justify_text(pdf,
"""    A demodulação dos sinais embaralhados é realizada de forma análoga à modulação, dado que o sistema é \
auto inversor. Assim, os mesmos cossenos e filtros são utilizados para deslocar as frequências de volta à banda original \
e reconstruir o sinal, aplicados na mesma ordem.""")
    
    pdf.start_section(f"{pdf.actual_section}.5 Visualizações", 1)
    justify_text(pdf,
"""    Os sinais de áudio utilizados internamente são gerados diretamente dos sinais processados em 96kHz. Contudo, a plotagem do sinal \
ao longo do tempo e espectogramas demandam muito processamento e memória, de modo que a geração destas visualizações, bem como a escrita dos arquivos de áudio de saída, \
ocorrem após realizar __downsampling__ do sinal processado para 44,1kHz.
""")