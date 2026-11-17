# MLOps Classes / Aulas de MLOps

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) ![Python](https://img.shields.io/badge/Language-Python-blue.svg)

Practical coursework in MLOps, data engineering and machine learning with Python.<br>
Trabalhos práticos de MLOps, engenharia de dados e aprendizado de máquina com Python.

[English](#english) · [Português](#português)

## English

### What it does

This public repository collects code from my **MLOps classes**, with examples of data ingestion, ETL, analytical modeling, model training and evaluation. Each class folder includes a README explaining the exercise and its technical decisions.

**MLOps** combines DevOps practices, automation and collaboration to build, deploy and monitor machine learning models safely and reliably in real-world applications. **DevOps** is a culture and practice that unites software development and IT operations to build, test and release code faster and more reliably through automation.

These are educational exercises using simulated or sample data, rather than a production platform. The deploy gate in class 01 is simulated; class 05's ETL pipeline (`etl_pipeline.py`) is still empty. There is no single command or shared dependency file for all classes, and class 04's `requirements.txt` is currently empty.

### Repository structure

- `aulas/` — six class folders listed below, each with its own README and Python scripts.
- `aulas/trabalho04/src/` — modules for data generation, preprocessing, metrics, plots and reporting.
- `aulas/trabalho06/data/` and `aulas/trabalho06/docs/` — transaction dataset and assignment PDF.
- `README.md`, `.gitignore` and `LICENSE` — repository overview, ignore rules and MIT license.

### Classes board

| Class | Description |
|---|---|
| [Trabalho 01](aulas/trabalho01) | 🎬 MLOps pipeline simulator: data ingestion, ETL/cleaning, training and a deploy gate. |
| [Trabalho 02](aulas/trabalho02) | 🗃️ Data Warehouse with DuckDB: OLTP to OLAP, Star Schema, export to Excel. |
| [Trabalho 03](aulas/trabalho3) | 🔧 Predictive maintenance for an air compressor: two Random Forests + a live Streamlit dashboard. |
| [Trabalho 04](aulas/trabalho04) | 📊 Classification metrics on imbalanced data: why accuracy lies and how to tune the threshold by cost. |
| [Trabalho 05](aulas/trabalho05) | 🧹 Dirty data generator (JSON CRM + CSV shipments) to feed an ETL pipeline. *(in progress)* |
| [Trabalho 06](aulas/trabalho06) | 👥 Modular churn classification pipeline (pivot table + Logistic Regression), built as a trio project. |

### How to run

Clone the repository and run class 01, which only uses the Python standard library:

```bash
git clone https://github.com/gilas-byte/aulas-mlops
cd aulas-mlops/aulas/trabalho01
python simulador_mlops.py
```

Run it from `aulas/trabalho01/` so it can find `config.json`. With the checked-in configuration, it removes two of five records and stops before training because only 60% remain, below its 85% gate. Training and deployment are simulations.

For the other exercises, follow the README linked in the classes board, running commands from the corresponding class folder. Dependencies vary by exercise; class 02 has a populated `requirements.txt`, while class 04's dependency list still needs to be filled in. Some scripts overwrite generated data or model files when rerun.

To update an existing clone, run from inside the repository:

```bash
git pull
```

### Status

Study — coursework repository; class 05's ETL pipeline is unfinished.

### License

[MIT](LICENSE).

## Português

### O que faz

Este repositório público reúne códigos das minhas **aulas de MLOps**, com exemplos de ingestão de dados, ETL, modelagem analítica, treinamento e avaliação de modelos. Cada pasta de aula inclui um README com a explicação do exercício e das decisões técnicas.

**MLOps** combina práticas de DevOps, automação e colaboração para construir, implantar e monitorar modelos de machine learning de forma segura e confiável no mundo real. **DevOps** é uma cultura e prática que une o desenvolvimento de software e as operações de TI para criar, testar e liberar código de forma mais rápida e confiável por meio da automação.

São exercícios didáticos com dados simulados ou de exemplo, sem uma plataforma de produção. O portão de deploy da aula 01 é simulado; o pipeline de ETL da aula 05 (`etl_pipeline.py`) ainda está vazio. Não há comando único nem arquivo de dependências compartilhado entre todas as aulas, e o `requirements.txt` da aula 04 está vazio.

### Estrutura do repositório

- `aulas/` — seis pastas de aulas listadas abaixo, cada uma com README próprio e scripts Python.
- `aulas/trabalho04/src/` — módulos de geração de dados, pré-processamento, métricas, gráficos e relatórios.
- `aulas/trabalho06/data/` e `aulas/trabalho06/docs/` — dataset de transações e PDF do enunciado.
- `README.md`, `.gitignore` e `LICENSE` — visão geral, regras de arquivos ignorados e licença MIT.

### Quadro de aulas

| Aula | Descrição |
|---|---|
| [Trabalho 01](aulas/trabalho01) | 🎬 Simulador de pipeline de MLOps: ingestão de dados, ETL/limpeza, treinamento e um portão de deploy. |
| [Trabalho 02](aulas/trabalho02) | 🗃️ Data Warehouse com DuckDB: de OLTP para OLAP, Star Schema, exportação para Excel. |
| [Trabalho 03](aulas/trabalho3) | 🔧 Manutenção preditiva de um compressor de ar: dois Random Forests + um dashboard ao vivo em Streamlit. |
| [Trabalho 04](aulas/trabalho04) | 📊 Métricas de classificação em dados desbalanceados: por que a acurácia mente e como ajustar o threshold por custo. |
| [Trabalho 05](aulas/trabalho05) | 🧹 Gerador de dados sujos (CRM em JSON + envios em CSV) para alimentar um pipeline de ETL. *(em desenvolvimento)* |
| [Trabalho 06](aulas/trabalho06) | 👥 Pipeline modularizado de classificação de churn (tabela dinâmica + Regressão Logística), feito como trabalho em trio. |

### Como rodar

Clone o repositório e execute a aula 01, que usa apenas a biblioteca padrão do Python:

```bash
git clone https://github.com/gilas-byte/aulas-mlops
cd aulas-mlops/aulas/trabalho01
python simulador_mlops.py
```

Execute dentro de `aulas/trabalho01/` para que o script encontre `config.json`. Com a configuração versionada, ele remove dois dos cinco registros e para antes do treinamento porque restam apenas 60%, abaixo do limite de 85%. O treinamento e o deploy são simulados.

Para os outros exercícios, siga o README vinculado no quadro de aulas, executando os comandos dentro da pasta correspondente. As dependências variam por exercício; a aula 02 tem um `requirements.txt` preenchido, enquanto a lista de dependências da aula 04 ainda precisa ser preenchida. Alguns scripts sobrescrevem dados ou modelos gerados ao serem executados novamente.

Para atualizar um clone existente, execute dentro do repositório:

```bash
git pull
```

### Status

Estudo — repositório de trabalhos de aula; o pipeline de ETL da aula 05 está incompleto.

### Licença

[MIT](LICENSE).
