import json
import random
import time

def carregar_configuracao():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def simular_pipeline():
    config = carregar_configuracao()
    print("\n" + "=" * 50)
    print(
        f" INICIANDO SIMULADOR DE MLOPS - Aluno: {config.get('nome_aluno')}"
    )
    print("=" * 50)
    time.sleep(1)

    # --- ETAPA 1: DADOS BRUTOS ---
    print("\n[1. INGESTÃO DE DADOS]")
    dados_brutos = [
        {"id": 1, "idade": 25, "renda": 3500},
        {"id": 2, "idade": None, "renda": 4200}, # Dado sujo
        {"id": 3, "idade": 45, "renda": 8900},
        {"id": 4, "idade": 19, "renda": None}, # Dado sujo
        {"id": 5, "idade": 31, "renda": 5100},
    ]
    print(f"\nRecebidos {len(dados_brutos)} registros da fonte.\n")
    print("\n[2. ENGENHARIA DE DADOS(ETL)]")
    time.sleep(1)
    if config["limpar_dados_nulos"]:
        dados_limpos = [
            d
            for d in dados_brutos
            if d["idade"] is not None and d["renda"] is not None
        ]
        removidos = len(dados_brutos) - len(dados_limpos)
        print(f"Filtro ativado! {removidos} registros com erro foram REMOVIDOS.")
    else:
        dados_limpos = dados_brutos
        print(
            "ALERTA! Limpeza desativada! Registros corrompidos passaram para o modelo."
            # eu sinceramente daria um return aqui pra n ir dados corrompidos para o modelo, até porque
            # pode fazer o modelo ser falho e inutilizavel
        )

    print(f"\nBase pronta para treino: {len(dados_limpos)} registros válidos.")

    # --- ETAPA 3: MACHINE LEARNING ---
    print("\n[3. TREINAMENTO DO MODELO (ML)]")
    time.sleep(1)
    pct_treino = config["tamanho_treino_porcentagem"]
    print(f"Usando {pct_treino}% dos dados para treinar o modelo...")

    # Causalidade simples para acuracia simulada
    if not config["limpar_dados_nulos"]:
        acuracia = random.randint(40,55) # acuracia ruim devido aos dados sujos
        status_dados = "Sujos"
    else:
        # acuracia melhora com mais dados de treino
        acuracia = min(
            98,
            int(
                (pct_treino * 0.8) + (config["fator_qualidade_modelo"] * 15)
            ),
        )
        status_dados = "Limpos"

    print(f" Modelo treinado! Acuracia obtida: {acuracia}%")

    # --- ETAPA 4: MLOPS & MONITORAÇÃO ---
    print("\n[4. MLOPS E DEPLOY]")
    time.sleep(1)
    print("Salvando registro do experimento (log)...")
    print(f"          ↪ Status dos Dados: {status_dados}")
    print(f"          ↪ Acuracia Final: {acuracia}")

    if acuracia >= 75:
        print("\n [SISTEMA]: Acuracia alta! Modelo APROVADO para ir pra produção.")
    else:
        print(
            "\n [SISTEMA]: Acuracia muito baixa! Modelo REPROVADO. Corrija o pipeline!"
        )

    print("=" * 50 + "\n")


if __name__ == "__main__":
    simular_pipeline()