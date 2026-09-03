# Avaliação de Métricas em Modelos de Classificação — Detecção de Falhas Industriais

Trabalho prático da unidade curricular **Engenharia de Dados e MLOps**
(Prof. MSc. Hugo Menezes Barra — UniSENAI).

Pipeline reprodutível de detecção de falhas em sensores industriais com **forte
desbalanceamento de classes (99,5% Operacional vs. 0,5% Falha)**, focado em
demonstrar por que a **Acurácia é uma armadilha** nesse cenário e como ajustar o
**threshold de decisão** segundo o custo financeiro real de uma planta fabril.

---

## Resultado resumido

| Cenário | Acurácia | Recall | F2 | Custo total estimado |
|---|---|---|---|---|
| Baseline ingênuo (prevê sempre "Operacional") | **0,9950** | 0,0000 | 0,0000 | R$ 1.500.000,00 |
| Modelo — threshold padrão 0,50 | 0,9798 | 0,9333 | 0,5243 | R$ 195.200,00 |
| Modelo — threshold otimizado 0,33 | 0,9728 | **1,0000** | 0,4792 | **R$ 130.400,00** |

O baseline atinge 99,50% de acurácia **sem detectar uma única falha**.
O ajuste do threshold de 0,50 para 0,33 gera **R$ 64.800,00 de economia (33,2%)**
apenas no conjunto de teste. AUC-ROC = 0,9971.

---

## Estrutura do projeto

```
.
├── main.py                     # orquestrador: roda o pipeline inteiro
├── requirements.txt
├── README.md
├── src/
│   ├── config.py               # parâmetros centrais (seed, custos, caminhos)
│   ├── data_generation.py      # dataset sintético 99,5% / 0,5%
│   ├── preprocessing.py        # split estratificado + scaler SEM data leakage
│   ├── modeling.py             # LogisticRegression + baseline ingênuo
│   ├── metrics.py              # matriz de confusão e métricas calculadas na mão
│   ├── threshold_analysis.py   # ajuste dinâmico do threshold por custo
│   ├── plots.py                # gráficos (matplotlib)
│   └── report.py               # relatório executivo em PDF (reportlab)
└── outputs/                    # gerado pela execução
    ├── relatorio_executivo.pdf
    ├── dados_sensores.csv
    ├── analise_threshold.csv
    └── fig_*.png
```

---

## Como executar

```bash
# 1. ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 2. dependências
pip install -r requirements.txt

# 3. rodar o pipeline completo
python main.py
```

O relatório final é gravado em `outputs/relatorio_executivo.pdf`.
A semente aleatória é fixa (`SEED = 42`), então qualquer execução reproduz
exatamente os mesmos números.

---

## Decisões técnicas

### 1. Prevenção de Data Leakage

A ordem das operações é o ponto central do trabalho:

1. `train_test_split(..., stratify=y)` é a **primeira** operação sobre os dados;
2. o `StandardScaler` chama `fit_transform()` **apenas no treino**;
3. no teste é chamado somente `transform()`, reaproveitando média e desvio-padrão
   aprendidos no treino.

Se o scaler fosse ajustado no dataset completo, a estatística das amostras de
teste vazaria para o treinamento e as métricas ficariam otimistas demais.

A **estratificação** é obrigatória aqui: com apenas 0,5% de positivos, um split
puramente aleatório poderia concentrar quase todas as falhas de um lado só.

### 2. `class_weight='balanced'`

Reponderiza a função de custo pelo inverso da frequência de cada classe, fazendo
um erro sobre uma falha pesar cerca de 200× mais que um erro sobre uma leitura
operacional. Sem isso, o otimizador convergiria para a solução trivial de nunca
prever falha.

### 3. Métricas calculadas manualmente

`src/metrics.py` deriva tudo a partir de TP/TN/FP/FN contados na mão:

- Acurácia = (TP + TN) / (TP + TN + FP + FN)
- Precisão = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F-beta = (1 + β²) · (P · R) / (β² · P + R), com β ∈ {1; 2; 0,5}

A função `validar_contra_sklearn()` confere os valores contra o `sklearn`.

### 4. Ajuste dinâmico do threshold

Os dois erros têm custos assimétricos na planta fabril:

- **Falso Negativo** (falha não detectada) → parada não planejada: **R$ 50.000**
- **Falso Positivo** (alarme falso) → inspeção desnecessária: **R$ 800**

A rotina varre 99 thresholds entre 0,01 e 0,99 e minimiza:

```
Custo Total(t) = FN(t) × custo_FN + FP(t) × custo_FP
```

Os custos ficam em `src/config.py` e podem ser alterados para simular outros
contratos de manutenção.

---

## Monitoramento em produção (resumo)

- Acompanhar **Recall, Precisão, F2 e custo acumulado** — nunca acurácia.
- Detectar **data drift** nos sensores (KS-test / PSI) semanalmente.
- Recalcular métricas em janela móvel de 30 dias conforme a manutenção confirma
  os alertas (**concept drift**).
- Versionar modelo **e scaler** juntos; usar um scaler diferente em produção é
  outra forma de leakage.
- Tratar o threshold como parâmetro de configuração, recalculado quando os
  custos de FN/FP mudarem.

---

## Stack

Python 3.11 · scikit-learn · pandas · numpy · matplotlib · reportlab
