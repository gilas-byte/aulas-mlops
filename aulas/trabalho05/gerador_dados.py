import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('pt_BR')

def gerar_clientes(qtd=80):
    clientes = []
    for i in range(1, qtd + 1):
        cliente_id = i  # ID_Cliente que vai bater com o CSV depois

        nome = fake.name()

        cpf = fake.cpf()

        if random.randint(0,1) == 0:
            documento = cpf
        else:
            documento = cpf.replace(".", "").replace("-","")

        regiao = fake.estado_sigla()  # ex: 'SC', 'SP'

        categoria = random.choice(['Bronze', 'Prata', 'Ouro'])

        clientes.append({
            'cliente_id': cliente_id,
            'nome_completo': nome,
            'documento_cpf_cnpj': documento,
            'regiao_estado': regiao,
            'categoria_conta': categoria
        })
    return clientes

def gerar_envios(clientes, qtd=300):
    envios = []
    status_possiveis = ['Entregue', 'Em Transito', 'Cancelado']

    for i in range(1, qtd + 1):
        transacao_id = i

        # TODO: escolher um cliente_id aleatório dentre os clientes gerados
        cliente_escolhido = random.choice(clientes)['cliente_id']

        # TODO: gerar uma data aleatória, ex: nos últimos 12 meses
        data_envio = datetime.now() - timedelta(random.randint(1, 365))
        if random.randint(0, 1) == 0:
            data_envio = data_envio.strftime("%d/%m/%Y")
        else:
            data_envio = data_envio.strftime("%Y-%m-%d")

        # TODO: gerar um valor de frete em USD, ex: entre 5.0 e 200.0
        valor_frete = random.uniform(5.0, 200.0)

        status = random.choice(status_possiveis)
        chanceStatus = random.randint(0,2)
        if chanceStatus == 0:
            status.upper()
        else:
            if chanceStatus == 1:
                status.lower()

        envios.append({
            'ID_Transacao': transacao_id,
            'Data_Envio': data_envio,
            'ID_Cliente': cliente_escolhido,
            'Valor_Frete_USD': valor_frete,
            'Status_Entrega': status
        })
    return envios