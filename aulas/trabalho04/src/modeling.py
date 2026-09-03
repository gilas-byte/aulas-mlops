"""
modeling.py
Treino do classificador e do baseline ingenuo.

O baseline (DummyClassifier 'most_frequent') existe para provar a
"armadilha da acuracia": ele nunca preve falha e ainda assim atinge ~99,5%
de acuracia, exatamente a taxa da classe majoritaria.
"""

import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression

from src.config import SEED


def treinar_modelo(X_treino, y_treino) -> LogisticRegression:
    """Regressao Logistica com class_weight='balanced'.

    O 'balanced' reponderiza a funcao de custo pelo inverso da frequencia da
    classe, fazendo o erro em uma falha pesar ~200x mais que o erro em uma
    leitura operacional. Sem isso o otimizador simplesmente ignoraria a
    classe minoritaria.
    """
    modelo = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=SEED,
    )
    modelo.fit(X_treino, y_treino)
    return modelo


def treinar_baseline(X_treino, y_treino) -> DummyClassifier:
    """Modelo burro: preve sempre a classe majoritaria (Operacional)."""
    baseline = DummyClassifier(strategy="most_frequent", random_state=SEED)
    baseline.fit(X_treino, y_treino)
    return baseline


def prever_probabilidades(modelo, X) -> np.ndarray:
    """Probabilidade da classe positiva (falha)."""
    return modelo.predict_proba(X)[:, 1]


def aplicar_threshold(probabilidades: np.ndarray, threshold: float) -> np.ndarray:
    """Converte probabilidade em rotulo 0/1 usando um corte customizado."""
    return (probabilidades >= threshold).astype(int)
