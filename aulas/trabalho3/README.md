# 📚 Trabalho 3 - Predição de Falhas em Compressor (Manutenção Preditiva) 🤖

> 🇬🇧 **English** below · 🇧🇷 **Português** [mais abaixo](#-trabalho-3---predição-de-falhas-em-compressor-manutenção-preditiva-pt-br-)

## 🤖 What is this about?

This project simulates a **predictive maintenance system** for an industrial air compressor. It trains two `RandomForestClassifier` models with `scikit-learn` and serves live predictions through a `Streamlit` dashboard that mimics a real-time IoT data stream, deciding whether the compressor is likely to fail **within the next 7 days**.

`The core idea: a compressor behaves very differently when it's running vs. when it's stopped, so instead of one generic model, the solution trains and serves two specialized models and switches between them automatically based on the machine's current status.`

## 📂 Files

- `treinarmodelo.py` → trains the two models on synthetic sensor data and saves them as `.joblib` files.
- `Teste_Compressor.py` → the Streamlit app that loads the models, simulates incoming IoT readings and shows live predictions.
- `modelo_motor_rodando.joblib` → trained model used when the compressor is **running**.
- `modelo_motor_parado.joblib` → trained model used when the compressor is **stopped**.

## ⚙️ My solution, explained

- **Why two models instead of one:** a running motor exposes 7-day rolling stats (mean, std, deviation) for every sensor, while a stopped motor doesn't generate that kind of trend data. Instead of forcing one model to handle both cases (and fake the missing features), I trained [two separate `RandomForestClassifier`s](treinarmodelo.py#L90-L94): one on the full feature set with rolling stats (`modelo_rodando`), and one on just the raw sensor/horimeter readings (`modelo_parado`).
- **Feature set:** sensor variables (pressure, temperature, flow, power, current) and equipment horimeters. For the "running" model, each variable is expanded into 4 columns — raw value, `_media_7dias`, `_std_7dias` and `_desvio_7dias` — built in [`treinarmodelo.py`](treinarmodelo.py#L30-L33).
- **Automatic model switching:** the dashboard reads `status_operacao` and checks it against [`status_motor_rodando`](Teste_Compressor.py#L28), a list of the status codes that mean "the motor is on". Based on that, [`prever_ponto_dinamicamente()`](Teste_Compressor.py#L47-L100) routes the data point to the correct model, using `modelo.feature_names_in_` to know exactly which columns to build — so the app never sends the wrong feature set to the wrong model.
- **Feature engineering at inference time:** since the live simulator only generates raw sensor values (not real 7-day history), I approximate the rolling stats on the fly: `_media_7dias` ≈ 95% of the raw value, `_std_7dias` ≈ 10% of the raw value, and `_desvio_7dias` is the difference between the raw value and that estimated mean (see [lines 62-71](Teste_Compressor.py#L62-L71)). This keeps the model's expected input shape satisfied without needing a real historical database.
- **Realistic IoT simulation:** the dashboard doesn't just loop instantly — it waits `10s + random(0, 5s)` between readings (`intervalo_base_segundos` / `atraso_iot_max_segundos`, [lines 114-116](Teste_Compressor.py#L114-L116)) to simulate the natural delay/jitter of real IoT devices sending telemetry.
- **Imbalanced synthetic data on purpose:** the training labels are generated with `p=[0.85, 0.15]` for the running model and `p=[0.95, 0.05]` for the stopped model ([treinarmodelo.py#L74](treinarmodelo.py#L74), [#L87](treinarmodelo.py#L87)), since real failures are rare events — this keeps the synthetic dataset closer to a real predictive-maintenance scenario.

## ▶️ How to run

```
pip install streamlit pandas numpy scikit-learn joblib

# 1. Generate the .joblib models
python treinarmodelo.py

# 2. Launch the live dashboard
streamlit run Teste_Compressor.py
```

Click **"Iniciar Simulação"** to start streaming simulated sensor readings and watch the model switch between "Motor Rodando" and "Motor Parado" predictions in real time.

---

# 📚 Trabalho 3 - Predição de Falhas em Compressor (Manutenção Preditiva) (PT-BR) 🤖

## 🤖 Sobre o que é esse trabalho?

Esse projeto simula um **sistema de manutenção preditiva** para um compressor de ar industrial. Ele treina dois modelos `RandomForestClassifier` com `scikit-learn` e serve previsões em tempo real através de um dashboard em `Streamlit` que simula um fluxo de dados de IoT, decidindo se o compressor tem chance de falhar **nos próximos 7 dias**.

`A ideia central: um compressor se comporta de forma bem diferente ligado e desligado, então em vez de um modelo genérico, a solução treina e serve dois modelos especializados e alterna entre eles automaticamente com base no status atual da máquina.`

## 📂 Arquivos

- `treinarmodelo.py` → treina os dois modelos com dados sintéticos de sensores e salva como arquivos `.joblib`.
- `Teste_Compressor.py` → o app Streamlit que carrega os modelos, simula leituras de IoT chegando e mostra as previsões em tempo real.
- `modelo_motor_rodando.joblib` → modelo treinado usado quando o compressor está **ligado**.
- `modelo_motor_parado.joblib` → modelo treinado usado quando o compressor está **parado**.

## ⚙️ Minha solução, explicada

- **Por que dois modelos em vez de um:** um motor rodando expõe estatísticas móveis de 7 dias (média, desvio padrão, desvio) para cada sensor, enquanto um motor parado não gera esse tipo de dado de tendência. Em vez de forçar um único modelo a lidar com os dois casos (e inventar as features que faltam), eu treinei [dois `RandomForestClassifier` separados](treinarmodelo.py#L90-L94): um com o conjunto completo de features com estatísticas móveis (`modelo_rodando`), e outro só com as leituras brutas de sensores/horímetros (`modelo_parado`).
- **Conjunto de features:** variáveis de sensores (pressão, temperatura, vazão, potência, corrente) e horímetros do equipamento. Para o modelo "rodando", cada variável vira 4 colunas — valor bruto, `_media_7dias`, `_std_7dias` e `_desvio_7dias` — montadas em [`treinarmodelo.py`](treinarmodelo.py#L30-L33).
- **Chaveamento automático de modelo:** o dashboard lê o `status_operacao` e compara com [`status_motor_rodando`](Teste_Compressor.py#L28), uma lista dos códigos de status que significam "o motor está ligado". Com base nisso, [`prever_ponto_dinamicamente()`](Teste_Compressor.py#L47-L100) direciona o ponto de dado pro modelo correto, usando `modelo.feature_names_in_` pra saber exatamente quais colunas montar — assim o app nunca manda o conjunto de features errado pro modelo errado.
- **Engenharia de features em tempo de inferência:** como o simulador ao vivo só gera valores brutos de sensor (sem um histórico real de 7 dias), eu aproximo as estatísticas móveis na hora: `_media_7dias` ≈ 95% do valor bruto, `_std_7dias` ≈ 10% do valor bruto, e `_desvio_7dias` é a diferença entre o valor bruto e essa média estimada (ver [linhas 62-71](Teste_Compressor.py#L62-L71)). Isso mantém o formato de entrada esperado pelo modelo sem precisar de um banco histórico real.
- **Dados sintéticos desbalanceados de propósito:** os rótulos de treino são gerados com `p=[0.85, 0.15]` pro modelo rodando e `p=[0.95, 0.05]` pro modelo parado ([treinarmodelo.py#L74](treinarmodelo.py#L74), [#L87](treinarmodelo.py#L87)), já que falhas reais são eventos raros — isso deixa o dataset sintético mais próximo de um cenário real de manutenção preditiva.

## ▶️ Como rodar

```
pip install streamlit pandas numpy scikit-learn joblib

# 1. Gera os modelos .joblib
python treinarmodelo.py

# 2. Sobe o dashboard ao vivo
streamlit run Teste_Compressor.py
```

Clica em **"Iniciar Simulação"** pra começar a receber leituras simuladas de sensores e ver o modelo alternando entre previsões de "Motor Rodando" e "Motor Parado" em tempo real.
