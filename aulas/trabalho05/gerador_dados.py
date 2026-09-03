import random
from faker import Faker
from datetime import datetime, timedelta
import json
import csv

fake = Faker('pt_BR')

opcoes_chaves = {
    'cliente_id': ['cliente_id', 'id_cliente', 'ID_Cliente'],
    'nome_completo': ['nome_completo', 'nome', 'Nome_Completo'],
    'documento_cpf_cnpj': ['documento_cpf_cnpj', 'cpf_cnpj', 'documento'],
    'regiao_estado': ['regiao_estado', 'estado', 'regiao'],
    'categoria_conta': ['categoria_conta', 'categoria', 'tipo_conta']
}

def gerar_clientes(qtd=80):
    clientes = []
    for i in range(1, qtd + 1):
        cliente_id = i  # ID_Cliente que vai bater com o CSV depois

        nome = fake.name()
        if random.random() < 0.1:
            nome = nome.encode('utf-8').decode('latin-1')

        cpf = fake.cpf()

        if random.randint(0,1) == 0:
            documento = cpf
        else:
            documento = cpf.replace(".", "").replace("-","")

        regiao = fake.estado_sigla()  # ex: 'SC', 'SP'

        categoria = random.choice(['Bronze', 'Prata', 'Ouro'])

        # chaves diferentes pra simular mais dados sujos

        cliente_chave = random.choice(opcoes_chaves['cliente_id'])
        nome_chave = random.choice(opcoes_chaves['nome_completo'])
        documento_chave = random.choice(opcoes_chaves['documento_cpf_cnpj'])
        regiao_chave = random.choice(opcoes_chaves['regiao_estado'])
        categoria_chave = random.choice(opcoes_chaves['categoria_conta'])

        clientes.append({
            cliente_chave: cliente_id,
            nome_chave: nome,
            documento_chave: documento,
            regiao_chave: regiao,
            categoria_chave: categoria
        })
    return clientes

def gerar_envios(clientes, qtd=300):
    envios = []
    status_possiveis = ['Entregue', 'Em Transito', 'Cancelado']

    for i in range(1, qtd + 1):
        transacao_id = i

        # escolhemos um cliente para esse tal envio
        cliente_sorteado = random.choice(clientes)
        cliente_escolhido = list(cliente_sorteado.values())[0]

        # transformamos em lista porque o dicionario vem com cliente_id todo estranho, e dicionarios
        # não tem como fazer [0], então transformando em uma lista conseguimos pegar o valor do dicionario e usar corretamente

        # criamos uma data ficticia, utilizando um timedelta com random int entre 1 a 365 dias
        data_envio = datetime.now() - timedelta(random.randint(1, 365))
        if random.randint(0, 1) == 0:
            data_envio = data_envio.strftime("%d/%m/%Y")
        else:
            data_envio = data_envio.strftime("%Y-%m-%d")

        # aqui temos outra parte aonde fazemos um valor ficticio
        valor_frete = round((random.uniform(5.0, 200.0)), 2)
        if random.random() < 0.1: # aonde também temos a probabilidade de 10% de um dado ser sujo e o valor estar nulo
            valor_frete = None

        # escolhemos um status para o envio
        status = random.choice(status_possiveis)
        chanceStatus = random.randint(0,2) # mais uma vez com uma probabilidade de 33% de chance de vir ASSIM, Assim ou assim
        if chanceStatus == 0:
            status = status.upper()
        elif chanceStatus == 1:
            status = status.lower()

        # adicionamos ao dicionario de envios
        envios.append({
            'ID_Transacao': transacao_id,
            'Data_Envio': data_envio,
            'ID_Cliente': cliente_escolhido,
            'Valor_Frete_USD': valor_frete,
            'Status_Entrega': status
        })

    # adicionar duplicatas
    for i in range(15):
        duplicata = (random.choice(envios)).copy()
        duplicata['ID_Transacao'] = (len(envios) + 1)
        envios.append(duplicata)
    
    return envios

clientes = gerar_clientes(80)
envios = gerar_envios(clientes, 300)

with open('clientes_crm.json', 'w', encoding='utf-8') as f:
    json.dump(clientes, f, ensure_ascii=False, indent=2)

with open('envios_brutos.csv', 'w', encoding='utf-8', newline='') as f:
    campos = ['ID_Transacao', 'Data_Envio', 'ID_Cliente', 'Valor_Frete_USD', 'Status_Entrega']
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()      # escreve a primeira linha (nomes das colunas)
    writer.writerows(envios)  # escreve todas as linhas de uma vez