from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

def treinamento_modelo(df):
    colunas_count = [col for col in df.columns if col.startswith('count_')] # Contagem de colunas que começam com count_ que foi feita pelo zamboni
    colunas_drop = ['churn', 'frequencia_total', 'id_cliente'] + colunas_count # Criando uma variavel das colunas que precisam ser retiradas



    X = df.drop(columns=colunas_drop) # Definindo o x, tirando as colunas não necessarias como features
    y = df['churn'] # Definindo o y, como o churn, que é basicamente é o resultado de uma condição de if frequencia < 8 = 1

    X_train, X_test, y_train, y_test = train_test_split( # Separando os dados para treinamento e teste
        X, y, test_size=0.3, random_state=42, stratify=y # Importante explicar o stratify, ele é o que vai separar os dados para que o y não seja todos churn = 1
    ) 

    modelo = LogisticRegression() # Modelo de Regressão Logistica

    modelo.fit(X_train, y_train) # Treinamento

    y_pred = modelo.predict(X_test) # Predição

    acuracia = accuracy_score(y_test, y_pred) # Fazendo o score de acuracia
    matriz_confusao = confusion_matrix(y_test, y_pred) # Agora a matriz confusão

    '''
    Importante falar sobre a matriz confusao porque eu tive uma dificuldade inicial de entender

    basicamente a matriz confusão é separada assim
    [[4, 0]
    [0, 2]]

    o que significa?
    linha 1, coluna 1 = 4 = Verdadeiro Negativo
    linha 1, coluna 2 = 0 Falso Positivo
    linha 2, coluna 1 = 0 Falso Negativo
    linha 2, coluna 2 = 2 Verdadeiro Positivo
    '''

    return modelo, acuracia, matriz_confusao