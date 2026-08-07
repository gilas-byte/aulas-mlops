# 📚 Aula 01 - Simulador de Pipeline de MLOps 🤖

> 🇬🇧 **English** below · 🇧🇷 **Português** [mais abaixo](#-aula-01---simulador-de-pipeline-de-mlops-pt-br-)

## 🤖 What is this class about?

This class simulates a full **MLOps pipeline** in a single script, going through data ingestion, data cleaning (ETL), model training and a final deploy decision.

`The idea is to see, step by step, how a dirty dataset can ruin a model, and how a config file can control the whole pipeline behavior.`

## 📂 Files

- `simulador_mlops.py` → the pipeline itself, split in 4 stages (ingestion, ETL, training, MLOps/deploy).
- `config.json` → controls the pipeline: student name, if null data gets cleaned, % of data used for training and a "model quality factor".

## ⚙️ Some technical things explained

- **ETL (Extract, Transform, Load):** here it's the step that removes dirty records (`None` values) before training. If `limpar_dados_nulos` is `false`, the corrupted data goes straight to the model.
- **Accuracy simulation:** it's not a real model, it's a simplified formula using the training % and the quality factor from `config.json`, just to show that more/better data usually means better accuracy.
- **Deploy gate:** the script only "approves" the model for production if accuracy is `>= 75%`, simulating a real quality gate before deploy.

## ▶️ How to run

```
python simulador_mlops.py
```

**Try changing `limpar_dados_nulos` to `false` in `config.json` and run it again to see the difference!**

## 🛠️​ A fix that i did

The old code didn't have a proper approach for dirty records (`None` values), so I made a function called [`limparDados()`](simulador_mlops.py#L17-L19) that returns a list with only the clean records. Then, in the ETL step, I added an early-return gate: if [the percentage of dirty data is too high](simulador_mlops.py#L47-L54), the pipeline stops right there instead of training on bad data.

---

# 📚 Aula 01 - Simulador de Pipeline de MLOps (PT-BR) 🤖

## 🤖 Sobre o que é essa aula?

Essa aula simula um pipeline completo de **MLOps** em um único script, passando por ingestão de dados, limpeza de dados (ETL), treinamento do modelo e uma decisão final de deploy.

`A ideia é ver, passo a passo, como um dataset sujo pode arruinar um modelo, e como um arquivo de config pode controlar todo o comportamento do pipeline.`

## 📂 Arquivos

- `simulador_mlops.py` → o pipeline em si, dividido em 4 etapas (ingestão, ETL, treinamento, MLOps/deploy).
- `config.json` → controla o pipeline: nome do aluno, se os dados nulos são limpos, % dos dados usados no treino e um "fator de qualidade do modelo".

## ⚙️ Algumas coisas técnicas explicadas

- **ETL (Extract, Transform, Load):** aqui é a etapa que remove os registros sujos (valores `None`) antes do treino. Se `limpar_dados_nulos` for `false`, os dados corrompidos vão direto para o modelo.
- **Simulação de acurácia:** não é um modelo de verdade, é uma fórmula simplificada usando o % de treino e o fator de qualidade do `config.json`, só pra mostrar que mais/melhores dados geralmente resultam em melhor acurácia.
- **Portão de deploy:** o script só "aprova" o modelo para produção se a acurácia for `>= 75%`, simulando um portão de qualidade real antes do deploy.

## ▶️ Como rodar

```
python simulador_mlops.py
```

**Tenta mudar `limpar_dados_nulos` para `false` no `config.json` e rodar de novo pra ver a diferença!**

## 🛠️​ Uma correção que eu fiz

O código antigo não tinha um tratamento adequado para registros sujos (valores `None`), então eu fiz uma função chamada [`limparDados()`](simulador_mlops.py#L17-L19) que retorna uma lista só com os registros limpos. Depois, na etapa de ETL, eu adicionei um portão de parada antecipada: se [a porcentagem de dados sujos for muito alta](simulador_mlops.py#L47-L54), o pipeline para ali mesmo em vez de treinar com dados ruins.
