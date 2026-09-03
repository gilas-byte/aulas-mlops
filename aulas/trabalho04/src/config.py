"""
config.py
Parametros centrais do projeto. Deixar tudo em um lugar so facilita
reproduzir o experimento (mesma SEED = mesmo resultado sempre).
"""

from pathlib import Path

# ---------------------------------------------------------------
# Reprodutibilidade
# ---------------------------------------------------------------
SEED = 42

# ---------------------------------------------------------------
# Geracao dos dados sinteticos
# ---------------------------------------------------------------
N_AMOSTRAS = 20_000          # total de leituras de sensores
TAXA_FALHA = 0.005           # 0,5% falha  /  99,5% operacional
TEST_SIZE = 0.30             # 30% separado para teste

SENSORES = [
    "vibracao_rms",          # vibracao do braco robotico (mm/s)
    "temperatura_c",         # temperatura do mancal (C)
    "corrente_a",            # corrente do motor (A)
    "pressao_bar",           # pressao hidraulica (bar)
    "rotacao_rpm",           # rotacao do eixo (rpm)
    "ruido_db",              # ruido acustico (dB)
]

# ---------------------------------------------------------------
# Cenario financeiro da planta fabril (valores em R$)
# ---------------------------------------------------------------
# FN = falha real que o modelo NAO detectou -> parada nao planejada de linha
CUSTO_FN = 50_000.00
# FP = alarme falso -> equipe para a maquina e inspeciona sem necessidade
CUSTO_FP = 800.00

THRESHOLD_PADRAO = 0.50      # threshold default do sklearn

# ---------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
PASTA_SAIDA = RAIZ / "outputs"
PASTA_SAIDA.mkdir(exist_ok=True)

ARQ_DATASET = PASTA_SAIDA / "dados_sensores.csv"
ARQ_RELATORIO = PASTA_SAIDA / "relatorio_executivo.pdf"
