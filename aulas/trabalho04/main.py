"""
main.py
Orquestrador do pipeline. Executa tudo na ordem correta e gera o PDF.

Uso:
    python main.py
"""

from src import plots
from src.config import ARQ_DATASET, PASTA_SAIDA, THRESHOLD_PADRAO
from src.data_generation import gerar_dados, salvar_dados
from src.metrics import (
    calcular_metricas,
    dados_curva_roc,
    matriz_confusao,
    validar_contra_sklearn,
)
from src.modeling import (
    aplicar_threshold,
    prever_probabilidades,
    treinar_baseline,
    treinar_modelo,
)
from src.preprocessing import escalonar, resumo_split, separar_treino_teste
from src.report import gerar_relatorio
from src.threshold_analysis import encontrar_melhor_threshold, varrer_thresholds


def main():
    print("=" * 62)
    print("PIPELINE - AVALIACAO DE METRICAS EM CLASSIFICACAO DESBALANCEADA")
    print("=" * 62)

    # 1) Dados -----------------------------------------------------
    print("\n[1/6] Gerando dados sinteticos de sensores...")
    df = gerar_dados()
    salvar_dados(df)
    print(f"      {len(df)} amostras | falhas: {int(df['falha'].sum())} "
          f"({df['falha'].mean() * 100:.3f}%) -> {ARQ_DATASET.name}")

    # 2) Isolamento do teste ANTES do pre-processamento -------------
    print("\n[2/6] Separando treino/teste (estratificado) e escalonando...")
    X_treino, X_teste, y_treino, y_teste = separar_treino_teste(df)
    X_treino_esc, X_teste_esc, scaler = escalonar(X_treino, X_teste)
    split = resumo_split(y_treino, y_teste)
    print(f"      treino: {split['n_treino']} ({split['falhas_treino']} falhas) | "
          f"teste: {split['n_teste']} ({split['falhas_teste']} falhas)")
    print("      StandardScaler ajustado APENAS no treino (sem data leakage).")

    # 3) Modelos ----------------------------------------------------
    print("\n[3/6] Treinando modelos...")
    modelo = treinar_modelo(X_treino_esc, y_treino)
    baseline = treinar_baseline(X_treino_esc, y_treino)
    y_prob = prever_probabilidades(modelo, X_teste_esc)
    y_prob_base = prever_probabilidades(baseline, X_teste_esc)

    # 4) Metricas ---------------------------------------------------
    print("\n[4/6] Calculando metricas no conjunto de teste...")
    y_pred_05 = aplicar_threshold(y_prob, THRESHOLD_PADRAO)
    y_pred_base = baseline.predict(X_teste_esc)

    met_padrao = calcular_metricas(y_teste, y_pred_05, y_prob)
    met_baseline = calcular_metricas(y_teste, y_pred_base, y_prob_base)

    print(f"      Baseline ingenuo -> acuracia {met_baseline['acuracia']:.4f} | "
          f"recall {met_baseline['recall']:.4f}  (a armadilha da acuracia)")
    print(f"      Modelo (t=0.50)  -> acuracia {met_padrao['acuracia']:.4f} | "
          f"recall {met_padrao['recall']:.4f} | F2 {met_padrao['f2']:.4f} | "
          f"AUC {met_padrao['auc_roc']:.4f}")
    print(f"      Conferencia sklearn: {validar_contra_sklearn(y_teste, y_pred_05)}")

    # 5) Ajuste dinamico do threshold -------------------------------
    print("\n[5/6] Ajuste dinamico do threshold por custo financeiro...")
    df_th = varrer_thresholds(y_teste, y_prob)
    df_th.to_csv(PASTA_SAIDA / "analise_threshold.csv", index=False)
    resumo_th = encontrar_melhor_threshold(df_th)

    y_pred_otimo = aplicar_threshold(y_prob, resumo_th["threshold_otimo"])
    met_otimo = calcular_metricas(y_teste, y_pred_otimo, y_prob)

    print(f"      threshold otimo: {resumo_th['threshold_otimo']:.2f} | "
          f"custo R$ {resumo_th['custo_otimo']:,.2f}")
    print(f"      threshold padrao 0.50 | custo R$ {resumo_th['custo_padrao']:,.2f}")
    print(f"      economia: R$ {resumo_th['economia_reais']:,.2f} "
          f"({resumo_th['economia_percentual']:.1f}%)")

    # 6) Graficos + PDF ---------------------------------------------
    print("\n[6/6] Gerando graficos e relatorio PDF...")
    fpr, tpr, _ = dados_curva_roc(y_teste, y_prob)

    contexto = {
        "split": split,
        "metricas_padrao": met_padrao,
        "metricas_otimo": met_otimo,
        "metricas_baseline": met_baseline,
        "resumo_threshold": resumo_th,
        "fig_distribuicao": plots.plot_distribuicao_classes(df),
        "fig_cm_padrao": plots.plot_matriz_confusao(
            matriz_confusao(y_teste, y_pred_05),
            "Matriz de Confusao (t = 0,50)",
            "fig_cm_padrao.png",
        ),
        "fig_cm_otimo": plots.plot_matriz_confusao(
            matriz_confusao(y_teste, y_pred_otimo),
            f"Matriz de Confusao (t = {resumo_th['threshold_otimo']:.2f})",
            "fig_cm_otimo.png",
        ),
        "fig_roc": plots.plot_curva_roc(fpr, tpr, met_padrao["auc_roc"]),
        "fig_custo": plots.plot_custo_threshold(df_th, resumo_th),
        "fig_metricas_threshold": plots.plot_metricas_threshold(df_th, resumo_th),
    }

    caminho = gerar_relatorio(contexto)
    print(f"\nOK! Relatorio gerado em: {caminho}")
    print("=" * 62)


if __name__ == "__main__":
    main()
