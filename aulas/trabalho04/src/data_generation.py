"""
data_generation.py
Cria um dataset sintetico e reprodutivel de sensores industriais.

Regra do trabalho: 99,5% Operacional (classe 0) vs 0,5% Falha (classe 1).

As distribuicoes das duas classes se sobrepoem de proposito. Se elas fossem
perfeitamente separaveis o modelo acertaria 100% e o estudo de metricas
perderia o sentido.
"""

import numpy as np
import pandas as pd

from src.config import ARQ_DATASET, N_AMOSTRAS, SEED, SENSORES, TAXA_FALHA


def gerar_dados(
    n_amostras: int = N_AMOSTRAS,
    taxa_falha: float = TAXA_FALHA,
    seed: int = SEED,
) -> pd.DataFrame:
    """Gera o DataFrame bruto de leituras de sensores.

    Retorna colunas dos sensores + coluna alvo 'falha' (0 = operacional, 1 = falha).
    """
    rng = np.random.default_rng(seed)

    n_falha = int(round(n_amostras * taxa_falha))
    n_ok = n_amostras - n_falha

    # (media, desvio) de cada sensor para a classe OPERACIONAL
    perfil_ok = {
        "vibracao_rms": (2.5, 0.60),
        "temperatura_c": (65.0, 5.00),
        "corrente_a": (14.0, 1.50),
        "pressao_bar": (7.0, 0.50),
        "rotacao_rpm": (1500.0, 60.0),
        "ruido_db": (72.0, 3.00),
    }

    # Na FALHA os equipamentos vibram e esquentam mais, a pressao cai e a
    # rotacao oscila. O desvio maior representa o comportamento erratico.
    perfil_falha = {
        "vibracao_rms": (4.3, 1.10),
        "temperatura_c": (78.0, 8.00),
        "corrente_a": (17.5, 2.60),
        "pressao_bar": (6.1, 0.90),
        "rotacao_rpm": (1420.0, 110.0),
        "ruido_db": (80.0, 5.50),
    }

    def _amostrar(perfil, n):
        return np.column_stack(
            [rng.normal(perfil[s][0], perfil[s][1], n) for s in SENSORES]
        )

    X_ok = _amostrar(perfil_ok, n_ok)
    X_falha = _amostrar(perfil_falha, n_falha)

    X = np.vstack([X_ok, X_falha])
    y = np.hstack([np.zeros(n_ok, dtype=int), np.ones(n_falha, dtype=int)])

    # Ruido de medicao generico em todos os sensores (imprecisao do hardware)
    X += rng.normal(0, 0.15, X.shape)

    df = pd.DataFrame(X, columns=SENSORES)
    df["falha"] = y

    # Embaralha para nao ficar tudo ordenado por classe
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df


def salvar_dados(df: pd.DataFrame, caminho=ARQ_DATASET) -> None:
    df.to_csv(caminho, index=False)


if __name__ == "__main__":
    dados = gerar_dados()
    salvar_dados(dados)
    print(dados["falha"].value_counts(normalize=True))
