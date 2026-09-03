"""
report.py
Monta o Relatorio Executivo em PDF com ReportLab (Platypus).
"""

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.config import ARQ_RELATORIO, CUSTO_FN, CUSTO_FP, N_AMOSTRAS, TAXA_FALHA

AZUL = colors.HexColor("#1f4e79")
CINZA = colors.HexColor("#f0f2f5")


def _estilos():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle("Titulo", parent=s["Title"], fontSize=20, textColor=AZUL, spaceAfter=6))
    s.add(ParagraphStyle("Sub", parent=s["Normal"], fontSize=11, alignment=1, textColor=colors.grey))
    s.add(ParagraphStyle("H1", parent=s["Heading1"], fontSize=14, textColor=AZUL, spaceBefore=14, spaceAfter=6))
    s.add(ParagraphStyle("H2", parent=s["Heading2"], fontSize=11.5, textColor=colors.HexColor("#333333"), spaceBefore=10, spaceAfter=4))
    s.add(ParagraphStyle("Corpo", parent=s["Normal"], fontSize=9.5, leading=14, alignment=TA_JUSTIFY, spaceAfter=6))
    s.add(ParagraphStyle("Nota", parent=s["Normal"], fontSize=8, textColor=colors.grey, spaceAfter=10))
    return s


def _brl(v: float) -> str:
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _num(v: int) -> str:
    return f"{v:,}".replace(",", ".")


def _tabela(dados, larguras, alinhar_direita_apartir=1):
    t = Table(dados, colWidths=larguras, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), AZUL),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("ALIGN", (alinhar_direita_apartir, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CINZA]),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9ced6")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def gerar_relatorio(contexto: dict, caminho=ARQ_RELATORIO):
    """contexto vem do main.py com todos os numeros e caminhos de figuras."""
    s = _estilos()
    doc = SimpleDocTemplate(
        str(caminho),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Relatorio Executivo - Avaliacao de Metricas em Modelos de Classificacao",
    )

    m = contexto["metricas_otimo"]
    m05 = contexto["metricas_padrao"]
    base = contexto["metricas_baseline"]
    split = contexto["split"]
    th = contexto["resumo_threshold"]

    e = []

    # ---------------- CAPA / CABECALHO ----------------
    e.append(Paragraph("Relatório Executivo", s["Titulo"]))
    e.append(Paragraph("Avaliação de Métricas em Modelos de Classificação", s["Sub"]))
    e.append(Paragraph("Detecção de Falhas em Sensores Industriais — Indústria 4.0", s["Sub"]))
    e.append(Spacer(1, 8))
    e.append(
        Paragraph(
            "Unidade Curricular: Engenharia de Dados e MLOps &nbsp;|&nbsp; "
            f"Prof. MSc. Hugo Menezes Barra &nbsp;|&nbsp; Gerado em {datetime.now():%d/%m/%Y %H:%M}",
            s["Nota"],
        )
    )

    # ---------------- 1. ARQUITETURA ----------------
    e.append(Paragraph("1. Arquitetura da Solução e Prevenção de Data Leakage", s["H1"]))
    e.append(
        Paragraph(
            "O pipeline foi construído em módulos independentes "
            "(<b>data_generation → preprocessing → modeling → metrics → threshold_analysis → report</b>), "
            f"partindo de um dataset sintético reprodutível de {_num(N_AMOSTRAS)} leituras de seis sensores "
            f"(vibração, temperatura, corrente, pressão, rotação e ruído), com {TAXA_FALHA * 100:.1f}% de eventos de falha. "
            "A semente aleatória fixa garante que qualquer execução reproduza exatamente os mesmos resultados.",
            s["Corpo"],
        )
    )
    e.append(Paragraph("1.1 Como o isolamento preveniu o Data Leakage", s["H2"]))
    e.append(
        Paragraph(
            "<b>Data Leakage</b> ocorre quando informação do conjunto de teste influencia, direta ou indiretamente, "
            "o treinamento. O erro clássico é aplicar o <i>StandardScaler</i> no dataset completo antes do split: "
            "média e desvio-padrão passariam a carregar estatística das amostras de teste, e a métrica final ficaria "
            "otimista demais — um modelo que parece ótimo no notebook e falha na planta.",
            s["Corpo"],
        )
    )
    e.append(
        Paragraph(
            "Neste projeto a ordem foi rigorosamente invertida: <b>(1)</b> o <i>train_test_split</i> estratificado é a "
            "primeira operação sobre os dados; <b>(2)</b> o <i>StandardScaler</i> executa <b>fit_transform</b> apenas no "
            "treino; <b>(3)</b> no teste é chamado somente <b>transform</b>, reaproveitando os parâmetros aprendidos. "
            "A estratificação é indispensável: com apenas 0,5% de positivos, um split puramente aleatório poderia "
            "concentrar quase todas as falhas de um lado só.",
            s["Corpo"],
        )
    )

    e.append(
        _tabela(
            [
                ["Conjunto", "Amostras", "Falhas", "% de falha"],
                ["Treino", _num(split["n_treino"]), _num(split["falhas_treino"]), f"{split['perc_falha_treino']:.3f}%"],
                ["Teste", _num(split["n_teste"]), _num(split["falhas_teste"]), f"{split['perc_falha_teste']:.3f}%"],
            ],
            [4.5 * cm, 3.5 * cm, 3.0 * cm, 3.0 * cm],
        )
    )
    e.append(Spacer(1, 10))
    e.append(Image(str(contexto["fig_distribuicao"]), width=11 * cm, height=6.6 * cm))
    e.append(Paragraph("Figura 1 — Distribuição das classes no dataset gerado.", s["Nota"]))

    e.append(Paragraph("1.2 Modelo", s["H2"]))
    e.append(
        Paragraph(
            "Foi utilizada uma <b>Regressão Logística</b> com <b>class_weight='balanced'</b>. O parâmetro reponderiza a "
            "função de custo pelo inverso da frequência de cada classe, fazendo um erro sobre uma falha pesar cerca de "
            "200× mais do que um erro sobre uma leitura operacional. Sem esse ajuste, o otimizador convergiria para a "
            "solução trivial de nunca prever falha.",
            s["Corpo"],
        )
    )

    e.append(PageBreak())

    # ---------------- 2. METRICAS ----------------
    e.append(Paragraph("2. Quadro Comparativo de Métricas", s["H1"]))
    e.append(
        Paragraph(
            "A tabela compara três configurações sobre o <b>mesmo conjunto de teste isolado</b>: o baseline ingênuo "
            "(prevê sempre 'Operacional'), o modelo no threshold padrão de 0,50 e o modelo no threshold otimizado por custo.",
            s["Corpo"],
        )
    )

    linhas = [
        ["Métrica", "Baseline ingênuo", f"Modelo (t = 0,50)", f"Modelo (t = {th['threshold_otimo']:.2f})"],
        ["Acurácia", f"{base['acuracia']:.4f}", f"{m05['acuracia']:.4f}", f"{m['acuracia']:.4f}"],
        ["Verdadeiros Positivos (TP)", _num(base["TP"]), _num(m05["TP"]), _num(m["TP"])],
        ["Verdadeiros Negativos (TN)", _num(base["TN"]), _num(m05["TN"]), _num(m["TN"])],
        ["Falsos Positivos (FP)", _num(base["FP"]), _num(m05["FP"]), _num(m["FP"])],
        ["Falsos Negativos (FN)", _num(base["FN"]), _num(m05["FN"]), _num(m["FN"])],
        ["Precisão", f"{base['precisao']:.4f}", f"{m05['precisao']:.4f}", f"{m['precisao']:.4f}"],
        ["Recall (Sensibilidade)", f"{base['recall']:.4f}", f"{m05['recall']:.4f}", f"{m['recall']:.4f}"],
        ["Especificidade", f"{base['especificidade']:.4f}", f"{m05['especificidade']:.4f}", f"{m['especificidade']:.4f}"],
        ["F<sub>1</sub>-Score", f"{base['f1']:.4f}", f"{m05['f1']:.4f}", f"{m['f1']:.4f}"],
        ["F<sub>2</sub>-Score", f"{base['f2']:.4f}", f"{m05['f2']:.4f}", f"{m['f2']:.4f}"],
        ["F<sub>0.5</sub>-Score", f"{base['f05']:.4f}", f"{m05['f05']:.4f}", f"{m['f05']:.4f}"],
        ["AUC-ROC", f"{base['auc_roc']:.4f}", f"{m05['auc_roc']:.4f}", f"{m['auc_roc']:.4f}"],
    ]
    # Converte a primeira coluna em Paragraph para renderizar os subscritos
    est_cel = ParagraphStyle("Cel", parent=s["Normal"], fontSize=8.5, leading=10)
    dados_tab = [linhas[0]] + [[Paragraph(l[0], est_cel), l[1], l[2], l[3]] for l in linhas[1:]]
    e.append(_tabela(dados_tab, [5.6 * cm, 3.4 * cm, 3.4 * cm, 4.0 * cm]))
    e.append(Spacer(1, 8))

    e.append(Paragraph("2.1 A armadilha da Acurácia", s["H2"]))
    e.append(
        Paragraph(
            f"O baseline ingênuo atinge <b>{base['acuracia'] * 100:.2f}% de acurácia</b> sem detectar uma única falha "
            f"(TP = 0, Recall = 0). Ele simplesmente reproduz a frequência da classe majoritária. Na prática, esse modelo "
            f"deixaria passar as {_num(base['FN'])} falhas do conjunto de teste, o que representaria "
            f"<b>{_brl(base['FN'] * CUSTO_FN)}</b> em paradas não planejadas. Isso demonstra por que a acurácia é uma "
            "métrica inútil — e perigosa — em cenários com 0,5% de positivos.",
            s["Corpo"],
        )
    )

    e.append(Paragraph("2.2 Interpretação da família F-beta", s["H2"]))
    e.append(
        Paragraph(
            "A família F<sub>β</sub> = (1 + β<super>2</super>) &#215; (P &#215; R) / (β<super>2</super> &#215; P + R) permite escolher "
            "o peso relativo entre precisão e recall. "
            "<b>F<sub>1</sub></b> trata as duas igualmente; <b>F<sub>2</sub></b> dá peso 4× maior ao recall e é a métrica "
            "adequada para manutenção preditiva, onde deixar de detectar uma falha (FN) custa muito mais caro que um alarme "
            "falso; <b>F<sub>0.5</sub></b> privilegia a precisão e seria preferível apenas se cada inspeção fosse "
            "extremamente cara ou disruptiva.",
            s["Corpo"],
        )
    )
    e.append(
        Paragraph(
            f"A <b>AUC-ROC de {m['auc_roc']:.4f}</b> mede a capacidade de ordenação do modelo independentemente do corte "
            "escolhido — por isso é idêntica nos dois thresholds. Ela indica a probabilidade de o modelo atribuir score "
            "maior a uma falha real do que a uma leitura operacional escolhida ao acaso.",
            s["Corpo"],
        )
    )

    e.append(Spacer(1, 6))
    tab_figs = Table(
        [[Image(str(contexto["fig_cm_padrao"]), width=7.2 * cm, height=6.3 * cm),
          Image(str(contexto["fig_roc"]), width=8.0 * cm, height=6.7 * cm)]],
        hAlign="LEFT",
    )
    e.append(tab_figs)
    e.append(Paragraph("Figura 2 — Matriz de confusão (t = 0,50) e Curva ROC no conjunto de teste.", s["Nota"]))

    # ---------------- 3. ANALISE FINANCEIRA ----------------
    e.append(Paragraph("3. Análise Financeira do Threshold", s["H1"]))
    e.append(
        Paragraph(
            "O threshold 0,50 é uma convenção estatística, não uma decisão de negócio. Numa planta fabril os dois erros "
            f"têm custos assimétricos: um <b>Falso Negativo</b> (falha não detectada) gera parada não planejada de linha, "
            f"estimada em <b>{_brl(CUSTO_FN)}</b>; um <b>Falso Positivo</b> (alarme falso) gera apenas uma inspeção "
            f"preventiva desnecessária, estimada em <b>{_brl(CUSTO_FP)}</b> — uma razão de "
            f"{CUSTO_FN / CUSTO_FP:.0f}:1.",
            s["Corpo"],
        )
    )
    e.append(
        Paragraph(
            "A rotina de ajuste dinâmico varre 99 thresholds entre 0,01 e 0,99 e minimiza a função de custo: "
            "<b>Custo Total(t) = FN(t) × custo_FN + FP(t) × custo_FP</b>.",
            s["Corpo"],
        )
    )

    e.append(Image(str(contexto["fig_custo"]), width=15 * cm, height=8.7 * cm))
    e.append(Paragraph("Figura 3 — Curva de Custo Total vs. Threshold, com o ponto de menor custo destacado.", s["Nota"]))

    lp, lo = th["linha_padrao"], th["linha_otima"]
    e.append(
        _tabela(
            [
                ["Cenário", "Threshold", "FN", "FP", "Recall", "Custo Total"],
                ["Padrão", f"{th['threshold_padrao']:.2f}", _num(int(lp["FN"])), _num(int(lp["FP"])), f"{lp['recall']:.4f}", _brl(th["custo_padrao"])],
                ["Otimizado", f"{th['threshold_otimo']:.2f}", _num(int(lo["FN"])), _num(int(lo["FP"])), f"{lo['recall']:.4f}", _brl(th["custo_otimo"])],
                ["Economia", "—", "—", "—", "—", _brl(th["economia_reais"])],
            ],
            [3.0 * cm, 2.4 * cm, 2.0 * cm, 2.0 * cm, 2.4 * cm, 4.2 * cm],
        )
    )
    e.append(Spacer(1, 8))
    e.append(
        Paragraph(
            f"<b>Resultado:</b> o threshold ótimo é <b>{th['threshold_otimo']:.2f}</b>, com custo total de "
            f"<b>{_brl(th['custo_otimo'])}</b> contra <b>{_brl(th['custo_padrao'])}</b> no threshold padrão — uma "
            f"economia de <b>{_brl(th['economia_reais'])}</b> ({th['economia_percentual']:.1f}%) sobre o conjunto de teste "
            f"de {_num(split['n_teste'])} leituras. O ajuste desloca o modelo para um regime mais sensível: aceita mais "
            "alarmes falsos (baratos) para eliminar falhas não detectadas (caras).",
            s["Corpo"],
        )
    )
    e.append(Spacer(1, 6))
    e.append(Image(str(contexto["fig_metricas_threshold"]), width=15 * cm, height=8.3 * cm))
    e.append(Paragraph("Figura 4 — Trade-off entre precisão, recall, F1 e F2 ao longo do threshold.", s["Nota"]))

    e.append(PageBreak())

    # ---------------- 4. MLOPS ----------------
    e.append(Paragraph("4. Recomendações MLOps para Produção", s["H1"]))
    e.append(Paragraph("4.1 Monitoramento", s["H2"]))
    for item in [
        "<b>Métricas de negócio, não acurácia:</b> o painel de produção deve acompanhar Recall, Precisão, F2 e o custo "
        "acumulado estimado (FN × custo_FN + FP × custo_FP). Acurácia não deve aparecer como indicador principal.",
        "<b>Data drift:</b> comparar semanalmente a distribuição de cada sensor em produção com a do treino "
        "(teste de Kolmogorov-Smirnov ou PSI). Desgaste mecânico e troca de matéria-prima deslocam as leituras.",
        "<b>Concept drift:</b> após a manutenção confirmar (ou não) cada alerta, recalcular Recall e Precisão em janela "
        "móvel de 30 dias e disparar alerta se o Recall cair abaixo de um limiar contratado.",
        "<b>Monitoramento da taxa de alertas:</b> se o volume de predições positivas sair muito da faixa histórica, é "
        "sinal de problema no pipeline de ingestão antes mesmo de haver rótulo disponível.",
    ]:
        e.append(Paragraph("• " + item, s["Corpo"]))

    e.append(Paragraph("4.2 Governança e reprodutibilidade", s["H2"]))
    for item in [
        "<b>Versionamento:</b> código em Git, dados e artefatos (modelo + scaler) versionados juntos, com a semente "
        "aleatória registrada. O scaler deve ser serializado com o modelo — usar um scaler diferente em produção é "
        "outra forma de leakage.",
        "<b>Threshold como parâmetro de configuração:</b> o valor ótimo depende dos custos de FN e FP, que mudam com o "
        "contrato de manutenção. Deve ficar em arquivo de configuração e ser recalculado periodicamente, nunca "
        "codificado no meio do script.",
        "<b>Retreino:</b> agendar retreino periódico (mensal) ou disparado por gatilho de drift, sempre repetindo o "
        "isolamento do conjunto de teste antes de qualquer transformação.",
        "<b>Validação pré-deploy:</b> nenhum modelo novo sobe sem superar o modelo em produção no conjunto de teste "
        "congelado, avaliado por custo total e não por acurácia.",
    ]:
        e.append(Paragraph("• " + item, s["Corpo"]))

    e.append(Paragraph("5. Conclusão", s["H1"]))
    e.append(
        Paragraph(
            f"Em um cenário com {TAXA_FALHA * 100:.1f}% de eventos raros, a acurácia é uma armadilha: um modelo que nunca "
            f"detecta falha alcança {base['acuracia'] * 100:.2f}% e ainda assim é inútil. A avaliação correta exige a "
            "matriz de confusão como base, métricas derivadas coerentes com o custo do erro (F2 e Recall neste caso), a "
            "AUC-ROC para medir a capacidade de ordenação independente do corte e, sobretudo, o ajuste do threshold "
            f"segundo a realidade financeira da operação — o que gerou uma economia estimada de {_brl(th['economia_reais'])} "
            "apenas no conjunto de teste.",
            s["Corpo"],
        )
    )

    doc.build(e)
    return caminho
