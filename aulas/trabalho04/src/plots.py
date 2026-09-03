"""
plots.py
Gera as figuras usadas no relatorio executivo (salvas em PNG).
"""

import matplotlib

matplotlib.use("Agg")  # backend sem interface grafica (roda em qualquer maquina)

import matplotlib.pyplot as plt
import numpy as np

from src.config import PASTA_SAIDA

COR_PRINCIPAL = "#1f4e79"
COR_ALERTA = "#c0392b"
COR_OK = "#27ae60"


def _salvar(fig, nome: str):
    caminho = PASTA_SAIDA / nome
    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return caminho


def plot_distribuicao_classes(df, nome="fig_distribuicao.png"):
    contagem = df["falha"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6, 3.6))
    barras = ax.bar(
        ["Operacional (0)", "Falha (1)"],
        contagem.values,
        color=[COR_PRINCIPAL, COR_ALERTA],
    )
    ax.set_ylabel("Nº de amostras")
    ax.set_title("Desbalanceamento do dataset")
    total = contagem.sum()
    for b, v in zip(barras, contagem.values):
        ax.text(
            b.get_x() + b.get_width() / 2,
            v,
            f"{v:,} ({v / total * 100:.2f}%)".replace(",", "."),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_ylim(0, contagem.max() * 1.15)
    ax.spines[["top", "right"]].set_visible(False)
    return _salvar(fig, nome)


def plot_matriz_confusao(cm: dict, titulo: str, nome: str):
    matriz = np.array([[cm["TN"], cm["FP"]], [cm["FN"], cm["TP"]]])
    fig, ax = plt.subplots(figsize=(4.6, 4.0))
    ax.imshow(matriz, cmap="Blues")

    rotulos = [["TN", "FP"], ["FN", "TP"]]
    limite = matriz.max() / 2
    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                f"{rotulos[i][j]}\n{matriz[i, j]:,}".replace(",", "."),
                ha="center",
                va="center",
                fontsize=11,
                color="white" if matriz[i, j] > limite else "black",
            )

    ax.set_xticks([0, 1], ["Previsto: OK", "Previsto: Falha"])
    ax.set_yticks([0, 1], ["Real: OK", "Real: Falha"])
    ax.set_title(titulo, fontsize=10)
    return _salvar(fig, nome)


def plot_curva_roc(fpr, tpr, auc: float, nome="fig_roc.png"):
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    ax.plot(fpr, tpr, color=COR_PRINCIPAL, lw=2, label=f"Modelo (AUC = {auc:.4f})")
    ax.plot([0, 1], [0, 1], "--", color="gray", lw=1, label="Aleatorio (AUC = 0,50)")
    ax.set_xlabel("Taxa de Falso Positivo (FPR)")
    ax.set_ylabel("Taxa de Verdadeiro Positivo (Recall)")
    ax.set_title("Curva ROC - conjunto de teste")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(alpha=0.3)
    return _salvar(fig, nome)


def plot_custo_threshold(df_th, resumo, nome="fig_custo.png"):
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(df_th["threshold"], df_th["custo_total"], color=COR_PRINCIPAL, lw=2)

    ax.axvline(
        resumo["threshold_padrao"],
        color="gray",
        ls="--",
        lw=1.4,
        label=f"Padrao 0,50 - R$ {resumo['custo_padrao']:,.0f}".replace(",", "."),
    )
    ax.scatter(
        [resumo["threshold_otimo"]],
        [resumo["custo_otimo"]],
        color=COR_OK,
        s=90,
        zorder=5,
        label=f"Otimo {resumo['threshold_otimo']:.2f} - R$ {resumo['custo_otimo']:,.0f}".replace(",", "."),
    )

    ax.set_xlabel("Threshold de decisao")
    ax.set_ylabel("Custo total estimado (R$)")
    ax.set_title("Custo Total vs. Threshold de Decisao")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.ticklabel_format(style="plain", axis="y")
    return _salvar(fig, nome)


def plot_metricas_threshold(df_th, resumo, nome="fig_metricas_threshold.png"):
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(df_th["threshold"], df_th["precisao"], label="Precisao", color=COR_ALERTA)
    ax.plot(df_th["threshold"], df_th["recall"], label="Recall", color=COR_PRINCIPAL)
    ax.plot(df_th["threshold"], df_th["f1"], label="F1", color=COR_OK, ls="--")
    ax.plot(df_th["threshold"], df_th["f2"], label="F2", color="#8e44ad", ls=":")
    ax.axvline(resumo["threshold_otimo"], color="black", lw=1, alpha=0.5)
    ax.set_xlabel("Threshold de decisao")
    ax.set_ylabel("Valor da metrica")
    ax.set_title("Trade-off Precisao x Recall ao longo do threshold")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    return _salvar(fig, nome)
