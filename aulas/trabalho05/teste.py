import random

opcoes_chaves = {
    'cliente_id': ['cliente_id', 'id_cliente', 'ID_Cliente'],
    'nome_completo': ['nome_completo', 'nome', 'Nome_Completo'],
    'documento_cpf_cnpj': ['documento_cpf_cnpj', 'cpf_cnpj', 'documento'],
    'regiao_estado': ['regiao_estado', 'estado', 'regiao'],
    'categoria_conta': ['categoria_conta', 'categoria', 'tipo_conta']
}

lista = []

for i in range(5):

    chave_id = random.choice(opcoes_chaves['cliente_id'])
    nome_id = random.choice(opcoes_chaves['nome_completo'])

    dic_teste = {
        'id' : f'{i}',
        f'{chave_id}': "bola",
        f'{nome_id}': "roblox"
    }

    lista.append(dic_teste)

print(list((random.choice(lista)).values())[0])

# print(random.choice(lista)[0])