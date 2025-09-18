import os
import sys
import gc
from pathlib import Path

from removeaccents import remove_accents
import matplotlib.pyplot as plt

from audioscrambler import Scrambler
from audioscrambler.report import Report

# Configurações de processamento
#---------------------------------
AMOSTRAGEM_PROCESSAMENTO = 96_000
AMOSTRAGEM_PLOTAGEM = 44_100
OUTPUT_PDF = "Demonstracao.pdf"
FORCE_REPROCESS = False  # Se True, força a reexecução do processamento mesmo que os arquivos de saída já existam
#---------------------------------

# Desativa warnings
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# Define o diretório de trabalho como o diretório do script
os.chdir(Path(__file__).parent)

# Processa os arquivos de áudio e gera figuras para o relatório
n_files = len(list(Path("samples").glob("*")))
for i, audio in enumerate(Path("samples").glob("*")):
    # Cria o diretório de saída para o áudio atual
    out_path = Path("outputs") / remove_accents(audio.stem)
    if out_path.exists() and not FORCE_REPROCESS:
        print(f"O diretório {out_path} já existe. Pulando processamento.")
        continue
    print(f"Processando {i+1}/{n_files}: {audio.stem}...")

    out_path.mkdir(exist_ok=True)

    # Inicializa o objeto Scrambler e processa o áudio
    scrambler = Scrambler(audio, AMOSTRAGEM_PROCESSAMENTO, out_path)
    scrambler.export_audio()
    scrambler.plot_spectrograms(sample_rate=AMOSTRAGEM_PLOTAGEM)
    scrambler.plot_signals(sample_rate=AMOSTRAGEM_PLOTAGEM)

    # Encerra o objeto Scrambler para liberar memória
    plt.close('all')
    del scrambler
    gc.collect()

# Gera o relatório em PDF
print("Gerando relatório...")
rep = Report("Gabriel Martins dos Santos Cunico", "Embaralhador de Voz")
rep.output(OUTPUT_PDF)
print(f"Relatório gerado em '{OUTPUT_PDF}'")