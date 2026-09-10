# 📚 Trabalho 06 - Pipeline Modularizado de Classificação (Churn) 🤖

> 🇬🇧 **English** below · 🇧🇷 **Português** [mais abaixo](#-trabalho-06---pipeline-modularizado-de-classificação-churn-pt-br-)
>
> 👥 **Group project (trio)** · 🔗 original repo: [GuiZamb32/ATV_06_Projeto_Modular_Trio](https://github.com/GuiZamb32/ATV_06_Projeto_Modular_Trio)

## 🤖 What is this about?

An online store wants to spot **inactive customers at risk of not buying again (churn)**. The assignment is to build that as a **modular Python pipeline**: raw transactions go in, a pivot table aggregates spending and purchase frequency per customer, a classification model is trained on it, and a new customer is scored at the end.

`The point of the work isn't the model — it's the modularization. Each person owns one file, the files only talk to each other through function calls, and the whole thing runs with a single "python main.py".`

## 👥 Task split

| Person | Module | Responsibility | Author |
|---|---|---|---|
| A — Data Engineering | `data_processing.py` | read the CSV, `pivot_table` by category, build the `churn` flag | Guilherme Zamboni |
| B — Data Science | `model_training.py` | 70/30 split, train a classifier, return model + metrics | **me** |
| C — MLOps & Integration | `main.py` | import both modules, run the flow, predict a new customer | Vinicius Joacir |

**I'm Person B** — `model_training.py` is mine. The other two modules were written by my classmates and are credited at the top of each file.

## 📂 Files

- `data/raw_transactions (1).csv` → the raw dataset: 460 transactions with `id_transacao`, `id_cliente`, `categoria`, `valor`.
- `data_processing.py` → *(Person A)* reads the CSV and returns the per-customer table with the churn label.
- `model_training.py` → *(Person B, mine)* trains the `LogisticRegression` and returns model, accuracy and confusion matrix.
- `main.py` → *(Person C)* orchestrates the three stages and runs the inference for a new customer.
- `docs/` → the assignment PDF.

## 📊 Result of a full run

```
[1/3] 50 customers aggregated, 13 columns generated
[2/3] LogisticRegression · 5 features (sum_alimentos, sum_casa, sum_eletronicos, sum_livros, sum_roupas)
      Test accuracy: 93.33%
      TN 7 · FP 1 · FN 0 · TP 7
[3/3] Default profile (high spend)  → ATIVO, 7.41% churn probability
      Alternative profile (low spend) → CHURN, 100.00% churn probability
```

## ⚙️ Some technical things explained

- **From transactions to customers (pivot table):** the raw CSV has one row per *purchase*, but the model needs one row per *customer*. [`pd.pivot_table`](data_processing.py#L19-L26) with `index='id_cliente'`, `columns='categoria'` and `aggfunc=['sum', 'count']` does that in one step, producing a `sum_<category>` and a `count_<category>` column for every category, with `fill_value=0` for the categories a customer never bought.
- **The churn rule:** it's not a real label, it's a business rule — [`churn = 1` when the customer's total purchase count is under 8](data_processing.py#L33-L36). That matters a lot for the next point.
- **Why I drop the `count_` columns before training** ([model_training.py#L6-L11](model_training.py#L6-L11)): `frequencia_total` is literally the sum of the `count_` columns, and `churn` is derived from `frequencia_total`. If I left them in `X`, the model would just re-learn the `if` that created the label — perfect accuracy and zero value. So the features are **only the amounts spent per category** (`sum_*`), and the model has to infer "is this customer going to churn?" from spending behavior alone.
- **Stratified split:** [`train_test_split(..., test_size=0.3, random_state=42, stratify=y)`](model_training.py#L14-L16) — `stratify=y` keeps the same churn/non-churn proportion in train and test. Without it, a random split could put almost every churn case on one side and the test metrics would be meaningless.
- **Logistic Regression:** the assignment allows any `scikit-learn` classifier. Logistic Regression fits here because the target is binary and the features are continuous amounts — plus it's the interpretable baseline you should always beat before reaching for something heavier.
- **Column order at inference time (training-serving skew):** [`montar_registro()`](main.py#L31-L42) doesn't build the input row from a hand-written list of columns — it reads the order from [`modelo.feature_names_in_`](main.py#L71) and fills any missing category with `0.0`. This is the sharpest detail in `main.py`: if the inference columns came in a different order than training, `scikit-learn` **wouldn't raise anything** — it would just predict wrong, silently.
- **Probability, not just the label:** the inference prints `predict()` *and* [`predict_proba()[0][1]`](main.py#L83-L84), so you get the confidence behind the decision instead of a bare 0/1. There are two demo profiles in the file ([lines 17-28](main.py#L17-L28)): the high-spend one comes back `ATIVO` at 7.41%, and the commented low-spend one comes back `CHURN` at 100.00%.
- **Reading the confusion matrix** (documented [inside the code](model_training.py#L27-L39), because it's the part that confused me the most at first, and unpacked into readable lines by [`exibir_metricas()`](main.py#L45-L55)):

  ```
  [[TN, FP]
   [FN, TP]]
  ```

  row 1 col 1 = True Negative · row 1 col 2 = False Positive · row 2 col 1 = False Negative · row 2 col 2 = True Positive.

## ▶️ How to run

```
pip install pandas scikit-learn

python main.py
```

⚠️ The dataset in this folder is named `raw_transactions (1).csv`, while the code expects `data/raw_transactions.csv` — rename it (or fix `CAMINHO_DADOS` in [main.py](main.py#L13)) before running.

---

# 📚 Trabalho 06 - Pipeline Modularizado de Classificação (Churn) (PT-BR) 🤖

> 👥 **Trabalho em grupo (trio)** · 🔗 repositório original: [GuiZamb32/ATV_06_Projeto_Modular_Trio](https://github.com/GuiZamb32/ATV_06_Projeto_Modular_Trio)

## 🤖 Sobre o que é esse trabalho?

Uma loja online quer identificar **clientes inativos com risco de não voltarem a comprar (churn)**. O trabalho é construir isso como um **pipeline modularizado em Python**: entram as transações brutas, uma tabela dinâmica agrega gasto e frequência de compra por cliente, um modelo de classificação é treinado em cima disso, e no final um cliente novo é pontuado.

`O ponto do trabalho não é o modelo — é a modularização. Cada pessoa é dona de um arquivo, os arquivos só conversam entre si por chamadas de função, e tudo roda com um único "python main.py".`

## 👥 Divisão de tarefas

| Pessoa | Módulo | Responsabilidade | Autor |
|---|---|---|---|
| A — Engenharia de Dados | `data_processing.py` | ler o CSV, `pivot_table` por categoria, gerar a flag `churn` | Guilherme Zamboni |
| B — Ciência de Dados | `model_training.py` | divisão 70/30, treinar um classificador, retornar modelo + métricas | **eu** |
| C — MLOps & Integração | `main.py` | importar os dois módulos, rodar o fluxo, prever um cliente novo | Vinicius Joacir |

**Eu sou a Pessoa B** — o `model_training.py` é meu. Os outros dois módulos foram feitos pelos meus colegas de classe e estão creditados no topo de cada arquivo.

## 📂 Arquivos

- `data/raw_transactions (1).csv` → o dataset bruto: 460 transações com `id_transacao`, `id_cliente`, `categoria`, `valor`.
- `data_processing.py` → *(Pessoa A)* lê o CSV e retorna a tabela por cliente com o rótulo de churn.
- `model_training.py` → *(Pessoa B, meu)* treina a `LogisticRegression` e retorna modelo, acurácia e matriz de confusão.
- `main.py` → *(Pessoa C)* orquestra as três etapas e roda a inferência para um cliente novo.
- `docs/` → o PDF do enunciado.

## 📊 Resultado de uma execução completa

```
[1/3] 50 clientes agregados, 13 colunas geradas
[2/3] LogisticRegression · 5 features (sum_alimentos, sum_casa, sum_eletronicos, sum_livros, sum_roupas)
      Acurácia no teste: 93,33%
      VN 7 · FP 1 · FN 0 · VP 7
[3/3] Perfil padrão (gasto alto)      → ATIVO, 7,41% de probabilidade de churn
      Perfil alternativo (gasto baixo) → CHURN, 100,00% de probabilidade de churn
```

## ⚙️ Algumas coisas técnicas explicadas

- **De transações para clientes (tabela dinâmica):** o CSV bruto tem uma linha por *compra*, mas o modelo precisa de uma linha por *cliente*. O [`pd.pivot_table`](data_processing.py#L19-L26) com `index='id_cliente'`, `columns='categoria'` e `aggfunc=['sum', 'count']` faz isso em um passo só, gerando uma coluna `sum_<categoria>` e uma `count_<categoria>` pra cada categoria, com `fill_value=0` pras categorias que o cliente nunca comprou.
- **A regra de churn:** não é um rótulo real, é uma regra de negócio — [`churn = 1` quando a contagem total de compras do cliente é menor que 8](data_processing.py#L33-L36). Isso importa muito pro próximo ponto.
- **Por que eu removo as colunas `count_` antes de treinar** ([model_training.py#L6-L11](model_training.py#L6-L11)): a `frequencia_total` é literalmente a soma das colunas `count_`, e o `churn` é derivado da `frequencia_total`. Se eu deixasse elas no `X`, o modelo só ia reaprender o `if` que criou o rótulo — acurácia perfeita e valor nenhum. Então as features são **só os valores gastos por categoria** (`sum_*`), e o modelo tem que inferir "esse cliente vai dar churn?" só pelo comportamento de gasto.
- **Divisão estratificada:** [`train_test_split(..., test_size=0.3, random_state=42, stratify=y)`](model_training.py#L14-L16) — o `stratify=y` mantém a mesma proporção de churn/não-churn no treino e no teste. Sem ele, uma divisão aleatória poderia jogar quase todos os casos de churn pra um lado só e as métricas de teste não significariam nada.
- **Regressão Logística:** o enunciado permite qualquer classificador do `scikit-learn`. A Regressão Logística encaixa aqui porque o alvo é binário e as features são valores contínuos — além de ser o baseline interpretável que você deveria sempre superar antes de partir pra algo mais pesado.
- **Ordem das colunas na inferência (training-serving skew):** a [`montar_registro()`](main.py#L31-L42) não monta a linha de entrada a partir de uma lista de colunas escrita na mão — ela lê a ordem do próprio [`modelo.feature_names_in_`](main.py#L71) e preenche com `0.0` qualquer categoria ausente. Esse é o detalhe mais afiado do `main.py`: se as colunas da inferência chegassem numa ordem diferente da do treino, o `scikit-learn` **não levantaria nada** — ele simplesmente preveria errado, em silêncio.
- **Probabilidade, não só o rótulo:** a inferência imprime o `predict()` *e* o [`predict_proba()[0][1]`](main.py#L83-L84), então você tem a confiança por trás da decisão em vez de um 0/1 seco. Tem dois perfis de demonstração no arquivo ([linhas 17-28](main.py#L17-L28)): o de gasto alto volta `ATIVO` com 7,41%, e o de gasto baixo (comentado) volta `CHURN` com 100,00%.
- **Como ler a matriz de confusão** (documentado [dentro do código](model_training.py#L27-L39), porque foi a parte que mais me confundiu no início, e desempacotado em linhas legíveis pela [`exibir_metricas()`](main.py#L45-L55)):

  ```
  [[VN, FP]
   [FN, VP]]
  ```

  linha 1 coluna 1 = Verdadeiro Negativo · linha 1 coluna 2 = Falso Positivo · linha 2 coluna 1 = Falso Negativo · linha 2 coluna 2 = Verdadeiro Positivo.

## ▶️ Como rodar

```
pip install pandas scikit-learn

python main.py
```

⚠️ O dataset nessa pasta se chama `raw_transactions (1).csv`, enquanto o código espera `data/raw_transactions.csv` — renomeia o arquivo (ou corrige o `CAMINHO_DADOS` no [main.py](main.py#L13)) antes de rodar.
