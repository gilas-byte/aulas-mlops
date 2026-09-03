"""
threshold_analysis.py
Ajuste Dinamico do Threshold de Decisao com base em custo financeiro.

Ideia: o threshold 0,5 do sklearn eh uma escolha estatistica arbitraria, nao
uma escolha de negocio. Numa planta fabril os dois erros custam valores muito
diferentes:

    Custo Total (t) = FN(t) * CUSTO_FN + FP(t) * CUSTO_FP

Varremos t de 0,01 a 0,99 e escolhemos o t que minimiza o custo total.
"""

import numpy as np
import pandas as pd

from src.config import CUSTO_FN, CUSTO_FP, THRESHOLD_PADRAO
from src.metrics import calcular_metricas
from src.modeling import aplicar_threshold


def varrer_thresholds(
    y_real,
    y_prob,
    custo_fn: float = CUSTO_FN,
    custo_fp: float = CUSTO_FP,
    n_pontos: int = 99,
) -> pd.DataFrame:
    """Tabela com uma linha por threshold testado."""
    thresholds = np.linspace(0.01, 0.99, n_pontos)
    linhas = []

    for t in thresholds:
        y_pred = aplicar_threshold(y_prob, t)
        m = calcular_metricas(y_real, y_pred)
        custo_total = m["FN"] * custo_fn + m["FP"] * custo_fp
        linhas.append(
            {
                "threshold": float(t),
                "TP": m["TP"],
                "TN": m["TN"],
                "FP": m["FP"],
                "FN": m["FN"],
                "precisao": m["precisao"],
                "recall": m["recall"],
                "f1": m["f1"],
                "f2": m["f2"],
                "custo_total": float(custo_total),
            }
        )

    return pd.DataFrame(linhas)


def encontrar_melhor_threshold(df_thresholds: pd.DataFrame) -> dict:
    """Linha de menor custo + comparacao com o threshold padrao 0,5."""
    melhor = df_thresholds.loc[df_thresholds["custo_total"].idxmin()]

    # Linha mais proxima de 0,5 na varredura
    idx_padrao = (df_thresholds["threshold"] - THRESHOLD_PADRAO).abs().idxmin()
    padrao = df_thresholds.loc[idx_padrao]

    economia = float(padrao["custo_total"] - melhor["custo_total"])
    perc = (economia / padrao["custo_total"] * 100) if padrao["custo_total"] else 0.0

    return {
        "threshold_otimo": float(melhor["threshold"]),
        "custo_otimo": float(melhor["custo_total"]),
        "linha_otima": melhor.to_dict(),
        "threshold_padrao": float(padrao["threshold"]),
        "custo_padrao": float(padrao["custo_total"]),
        "linha_padrao": padrao.to_dict(),
        "economia_reais": economia,
        "economia_percentual": float(perc),
    }
