"""
preprocessing.py
Isolamento do conjunto de teste ANTES de qualquer transformacao.

Prevencao de Data Leakage:
  1. train_test_split estratificado eh a PRIMEIRA operacao sobre os dados.
  2. O StandardScaler faz .fit_transform() APENAS no treino.
  3. No teste usamos somente .transform(), reaproveitando media e desvio
     aprendidos no treino. O teste nunca influencia a estatistica do scaler.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.config import SEED, SENSORES, TEST_SIZE


def separar_treino_teste(df: pd.DataFrame, test_size: float = TEST_SIZE, seed: int = SEED):
    """Split estratificado. Estratificar eh obrigatorio aqui: com 0,5% de
    positivos, um split aleatorio comum poderia deixar o teste quase sem falhas.
    """
    X = df[SENSORES]
    y = df["falha"]

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=seed,
        stratify=y,  # mantem a proporcao 99,5 / 0,5 nos dois lados
    )
    return X_treino, X_teste, y_treino, y_teste


def escalonar(X_treino: pd.DataFrame, X_teste: pd.DataFrame):
    """Padroniza as features sem vazar informacao do teste."""
    scaler = StandardScaler()
    X_treino_esc = scaler.fit_transform(X_treino)  # aprende SO no treino
    X_teste_esc = scaler.transform(X_teste)        # apenas aplica no teste
    return X_treino_esc, X_teste_esc, scaler


def resumo_split(y_treino: pd.Series, y_teste: pd.Series) -> dict:
    """Numeros usados no relatorio para provar o isolamento."""
    return {
        "n_treino": int(len(y_treino)),
        "n_teste": int(len(y_teste)),
        "falhas_treino": int(y_treino.sum()),
        "falhas_teste": int(y_teste.sum()),
        "perc_falha_treino": float(y_treino.mean() * 100),
        "perc_falha_teste": float(y_teste.mean() * 100),
    }
