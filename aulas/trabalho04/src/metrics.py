"""
metrics.py
Metricas calculadas na mao a partir da Matriz de Confusao, com conferencia
contra o sklearn.

Formulas usadas:
    Acuracia  = (TP + TN) / (TP + TN + FP + FN)
    Precisao  = TP / (TP + FP)
    Recall    = TP / (TP + FN)
    F-beta    = (1 + b^2) * (P * R) / (b^2 * P + R)
        b = 1.0 -> F1   (equilibrio entre precisao e recall)
        b = 2.0 -> F2   (peso 4x maior no recall - o que importa em manutencao)
        b = 0.5 -> F0.5 (favorece precisao - evitar alarme falso)
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


def matriz_confusao(y_real, y_pred) -> dict:
    """Retorna TP, TN, FP, FN contados manualmente."""
    y_real = np.asarray(y_real)
    y_pred = np.asarray(y_pred)

    tp = int(np.sum((y_real == 1) & (y_pred == 1)))
    tn = int(np.sum((y_real == 0) & (y_pred == 0)))
    fp = int(np.sum((y_real == 0) & (y_pred == 1)))
    fn = int(np.sum((y_real == 1) & (y_pred == 0)))
    return {"TP": tp, "TN": tn, "FP": fp, "FN": fn}


def _div(numerador: float, denominador: float) -> float:
    """Divisao segura: retorna 0.0 quando o denominador eh zero.
    Acontece, por exemplo, quando o modelo nao preve nenhum positivo (precisao 0/0).
    """
    return numerador / denominador if denominador else 0.0


def f_beta(precisao: float, recall: float, beta: float) -> float:
    b2 = beta ** 2
    return _div((1 + b2) * precisao * recall, b2 * precisao + recall)


def calcular_metricas(y_real, y_pred, y_prob=None) -> dict:
    """Bloco completo de metricas para um conjunto de predicoes."""
    cm = matriz_confusao(y_real, y_pred)
    tp, tn, fp, fn = cm["TP"], cm["TN"], cm["FP"], cm["FN"]

    acuracia = _div(tp + tn, tp + tn + fp + fn)
    precisao = _div(tp, tp + fp)
    recall = _div(tp, tp + fn)
    especificidade = _div(tn, tn + fp)

    resultado = {
        **cm,
        "acuracia": acuracia,
        "precisao": precisao,
        "recall": recall,
        "especificidade": especificidade,
        "f1": f_beta(precisao, recall, 1.0),
        "f2": f_beta(precisao, recall, 2.0),
        "f05": f_beta(precisao, recall, 0.5),
    }

    # AUC-ROC depende da probabilidade continua, nao do rotulo final.
    # Por isso ela NAO muda quando alteramos o threshold.
    resultado["auc_roc"] = float(roc_auc_score(y_real, y_prob)) if y_prob is not None else float("nan")
    return resultado


def validar_contra_sklearn(y_real, y_pred) -> dict:
    """Conferencia: nossas contas manuais batem com a biblioteca?"""
    return {
        "acuracia_sklearn": float(accuracy_score(y_real, y_pred)),
        "precisao_sklearn": float(precision_score(y_real, y_pred, zero_division=0)),
        "recall_sklearn": float(recall_score(y_real, y_pred, zero_division=0)),
        "f1_sklearn": float(f1_score(y_real, y_pred, zero_division=0)),
    }


def dados_curva_roc(y_real, y_prob):
    """FPR, TPR e thresholds para plotar a curva ROC."""
    fpr, tpr, thresholds = roc_curve(y_real, y_prob)
    return fpr, tpr, thresholds
