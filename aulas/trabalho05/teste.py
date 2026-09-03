import random
from datetime import datetime, timedelta

data_teste = datetime.now() - timedelta(random.randint(1, 365))
if random.randint(0, 1) == 0:
    data_teste = data_teste.strftime("%d/%m/%Y")
else:
    data_teste = data_teste.strftime("%Y-%m-%d")

print(data_teste)