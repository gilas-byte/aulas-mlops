'''
Esse arquivo não foi feito por mim, e sim pelo meu colega de classe Vinicius Joacir

link original do nosso repositorio : https://github.com/GuiZamb32/ATV_06_Projeto_Modular_Trio

'''

import pandas as pd

from data_processing import process_data
from model_training import treinamento_modelo

CAMINHO_DADOS = "data/raw_transactions.csv"

# Perfil do cliente novo: total gasto por categoria.
# Chaves ausentes sao preenchidas com 0.0 automaticamente.
CLIENTE_NOVO = {
    "sum_alimentos": 250.00,
    "sum_casa": 480.00,
    "sum_eletronicos": 900.00,
    "sum_livros": 110.00,
    "sum_roupas": 320.00,
}

# Perfil alternativo (cliente de baixo gasto) para demonstrar a deteccao de churn.
# Para usar, substitua CLIENTE_NOVO pelos valores abaixo:
#   sum_alimentos=120.00, sum_casa=80.50, sum_eletronicos=0.00,
#   sum_livros=45.90, sum_roupas=60.00


def montar_registro(perfil: dict, features: list) -> pd.DataFrame:
    """
    Monta o DataFrame de inferencia respeitando a ORDEM EXATA das colunas
    que o modelo viu durante o treino.

    Divergencia de ordem entre treino e inferencia (training-serving skew)
    nao levanta excecao no scikit-learn: o modelo simplesmente preve errado
    em silencio. Por isso a ordem vem do proprio modelo treinado, nunca de
    uma lista escrita a mao.
    """
    linha = [float(perfil.get(coluna, 0.0)) for coluna in features]
    return pd.DataFrame([linha], columns=features)


def exibir_metricas(acuracia, matriz_confusao) -> None:
    """Imprime as metricas de avaliacao do modelo de forma legivel."""
    vn, fp = matriz_confusao[0]
    fn, vp = matriz_confusao[1]

    print(f"Acuracia no conjunto de teste: {acuracia:.2%}\n")
    print("Matriz de confusao:")
    print(f"  Verdadeiro Negativo (previu ativo, era ativo)  : {vn}")
    print(f"  Falso Positivo      (previu churn, era ativo)  : {fp}")
    print(f"  Falso Negativo      (previu ativo, era churn)  : {fn}")
    print(f"  Verdadeiro Positivo (previu churn, era churn)  : {vp}")


def main() -> None:
    print("=" * 60)
    print("PIPELINE DE CLASSIFICACAO DE CHURN")
    print("=" * 60)

    # ETAPA 1 - Engenharia de Dados (Pessoa A)
    print("\n[1/3] Processando dados brutos...")
    dados = process_data(CAMINHO_DADOS)
    print(f"      {len(dados)} clientes agregados, {dados.shape[1]} colunas geradas.")

    # ETAPA 2 - Treinamento do modelo (Pessoa B)
    print("\n[2/3] Treinando modelo de classificacao...")
    modelo, acuracia, matriz_confusao = treinamento_modelo(dados)
    features = list(modelo.feature_names_in_)
    print(f"      Modelo: {type(modelo).__name__}")
    print(f"      Features utilizadas ({len(features)}): {', '.join(features)}\n")
    exibir_metricas(acuracia, matriz_confusao)

    # ETAPA 3 - Inferencia para um novo cliente (Pessoa C)
    print("\n[3/3] Inferencia para um novo cliente...")
    registro = montar_registro(CLIENTE_NOVO, features)
    print("      Perfil de entrada:")
    for coluna in features:
        print(f"        {coluna:<20} R$ {registro.iloc[0][coluna]:>8.2f}")

    predicao = modelo.predict(registro)[0]
    probabilidade = modelo.predict_proba(registro)[0][1]

    rotulo = "CHURN (risco de nao voltar a comprar)" if predicao == 1 else "ATIVO (sem risco identificado)"
    print(f"\n      RESULTADO: {rotulo}")
    print(f"      Probabilidade de churn: {probabilidade:.2%}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()