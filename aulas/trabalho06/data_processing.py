'''
Esse arquivo não foi feito por mim, e sim pelo meu colega de classe Guilherme Zamboni

link original do nosso repositorio : https://github.com/GuiZamb32/ATV_06_Projeto_Modular_Trio

'''

import pandas as pd

def process_data(file_path: str) -> pd.DataFrame:
    """
    Lê os dados brutos de transações, aplica pivot_table por categoria,
    calcula a frequência total de compras e define a flag de churn.
    """
    # 1. Leitura do arquivo CSV[cite: 6]
    df = pd.read_csv(file_path)
    
    # 2. Construção da Tabela Dinâmica (valores gastos e contagem por categoria)[cite: 6]
    pivot = pd.pivot_table(
        df,
        index='id_cliente',
        columns='categoria',
        values='valor',
        aggfunc=['sum', 'count'],
        fill_value=0
    )
    
    # Aplanar os nomes das colunas após o pivot
    pivot.columns = [f"{agg}_{cat}".lower() for agg, cat in pivot.columns]
    
    # 3. Cálculo da frequência total de compras do cliente
    colunas_count = [col for col in pivot.columns if col.startswith('count_')]
    pivot['frequencia_total'] = pivot[colunas_count].sum(axis=1)
    
    # 4. Geração da regra de Churn (1 para frequência < 8, senão 0)[cite: 6]
    pivot['churn'] = (pivot['frequencia_total'] < 8).astype(int)
    
    return pivot.reset_index()

if __name__ == "__main__":
    # Teste isolado do módulo
    df_processed = process_data("data/raw_transactions.csv")
    print("Dados processados com sucesso!")
    print(df_processed.head())