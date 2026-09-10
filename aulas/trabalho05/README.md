# 📚 Trabalho 05 - Gerador de Dados Sujos + Pipeline de ETL 🤖

> 🇬🇧 **English** below · 🇧🇷 **Português** [mais abaixo](#-trabalho-05---gerador-de-dados-sujos--pipeline-de-etl-pt-br-)
>
> ⚠️ **Work in progress:** the data generator is done, the ETL pipeline (`etl_pipeline.py`) is still empty.

## 🤖 What is this about?

This project is the **"before" side of an ETL**: instead of receiving a clean dataset, here I *build* the mess on purpose. The script generates two data sources that simulate a real company — a **CRM in JSON** (customers) and a **shipping system in CSV** (transactions) — both full of the classic problems you find in production data.

`The idea is simple: you can't really learn ETL with perfect data. So first I generate realistic dirty data, and then the pipeline has to clean it and join the two sources by the customer ID.`

## 📂 Files

- `gerador_dados.py` → generates the two dirty data sources with `Faker` (pt_BR locale).
- `clientes_crm.json` → the generated CRM file: 80 customers, **inconsistent key names on every record**.
- `data/envios_brutos.csv` → the generated shipping file: 300 transactions + 15 duplicates.
- `etl_pipeline.py` → *(empty for now)* the cleaning/joining pipeline.
- `teste.py` → a small scratch script I used to figure out how to read a value from a dict whose key name is random.

## ⚙️ The dirt I generate on purpose, explained

Every "defect" below is a real-world data problem, injected with a controlled probability:

- **Random key names (schema drift):** each customer record picks its own key names from [`opcoes_chaves`](gerador_dados.py#L9-L15) — so the same field can show up as `cliente_id`, `id_cliente` or `ID_Cliente`, `nome_completo` / `nome` / `Nome_Completo`, and so on ([lines 39-51](gerador_dados.py#L39-L51)). This simulates a CRM that changed its export schema over the years, and it's the reason a naive `json.load()` + `df['cliente_id']` simply breaks.
- **Broken encoding (mojibake):** 10% of the names are re-encoded with [`encode('utf-8').decode('latin-1')`](gerador_dados.py#L22-L24), producing the classic `JoÃ£o` instead of `João`.
- **Inconsistent document format:** the CPF comes out either masked (`123.456.789-00`) or unmasked (`12345678900`), 50/50 ([lines 28-31](gerador_dados.py#L28-L31)) — so the same person can look like two different people.
- **Two date formats in the same column:** `Data_Envio` is written as `%d/%m/%Y` or `%Y-%m-%d` at random ([lines 69-73](gerador_dados.py#L69-L73)), which is the fastest way to break a `pd.to_datetime()` that assumes one format.
- **Null values:** 10% of `Valor_Frete_USD` come out as `None` ([lines 76-78](gerador_dados.py#L76-L78)), leaving empty cells in the CSV.
- **Inconsistent capitalization:** `Status_Entrega` is randomly `ENTREGUE`, `entregue` or `Entregue` ([lines 81-86](gerador_dados.py#L81-L86)), so a `groupby` would count the same status three times.
- **Duplicate records:** [15 rows are copied](gerador_dados.py#L97-L101) from the existing shipments and re-appended with a new `ID_Transacao` — a duplicate that a simple `drop_duplicates()` on the ID **won't** catch, because only the primary key changed.
- **The join key that survives:** the customer's numeric ID is the *first value* of each record, which is why the shipping generator uses [`list(cliente_sorteado.values())[0]`](gerador_dados.py#L62-L63) — it can't rely on the key name, only on the position. That's exactly the workaround I prototyped in `teste.py`.

## ▶️ How to run

```
pip install faker

python gerador_dados.py
```

The script writes `clientes_crm.json` and `envios_brutos.csv` **in the current directory** — in this repo the CSV is kept in `data/`, so move it there (or run the script from inside `data/`) if you regenerate the files.

**Every run produces a different dataset (there's no fixed seed), so the ETL can't be tuned to one specific file — it has to actually handle the general case.**

---

# 📚 Trabalho 05 - Gerador de Dados Sujos + Pipeline de ETL (PT-BR) 🤖

> ⚠️ **Em desenvolvimento:** o gerador de dados está pronto, o pipeline de ETL (`etl_pipeline.py`) ainda está vazio.

## 🤖 Sobre o que é esse trabalho?

Esse projeto é o **lado "antes" de um ETL**: em vez de receber um dataset limpo, aqui eu *construo* a bagunça de propósito. O script gera duas fontes de dados que simulam uma empresa real — um **CRM em JSON** (clientes) e um **sistema de envios em CSV** (transações) — as duas cheias dos problemas clássicos que aparecem em dado de produção.

`A ideia é simples: não dá pra aprender ETL de verdade com dado perfeito. Então primeiro eu gero dado sujo realista, e depois o pipeline tem que limpar e juntar as duas fontes pelo ID do cliente.`

## 📂 Arquivos

- `gerador_dados.py` → gera as duas fontes de dados sujos com `Faker` (locale pt_BR).
- `clientes_crm.json` → o arquivo de CRM gerado: 80 clientes, **com nomes de chave inconsistentes em cada registro**.
- `data/envios_brutos.csv` → o arquivo de envios gerado: 300 transações + 15 duplicatas.
- `etl_pipeline.py` → *(vazio por enquanto)* o pipeline de limpeza/junção.
- `teste.py` → um script de rascunho que eu usei pra descobrir como ler um valor de um dicionário cuja chave tem nome aleatório.

## ⚙️ A sujeira que eu gero de propósito, explicada

Cada "defeito" abaixo é um problema real de dados, injetado com uma probabilidade controlada:

- **Nomes de chave aleatórios (schema drift):** cada registro de cliente escolhe os próprios nomes de chave a partir do [`opcoes_chaves`](gerador_dados.py#L9-L15) — então o mesmo campo pode aparecer como `cliente_id`, `id_cliente` ou `ID_Cliente`, `nome_completo` / `nome` / `Nome_Completo`, e por aí vai ([linhas 39-51](gerador_dados.py#L39-L51)). Isso simula um CRM que mudou o schema de exportação ao longo dos anos, e é justamente por isso que um `json.load()` + `df['cliente_id']` ingênuo simplesmente quebra.
- **Encoding quebrado (mojibake):** 10% dos nomes são recodificados com [`encode('utf-8').decode('latin-1')`](gerador_dados.py#L22-L24), gerando o clássico `JoÃ£o` no lugar de `João`.
- **Formato de documento inconsistente:** o CPF sai ou com máscara (`123.456.789-00`) ou sem (`12345678900`), 50/50 ([linhas 28-31](gerador_dados.py#L28-L31)) — então a mesma pessoa pode parecer duas pessoas diferentes.
- **Dois formatos de data na mesma coluna:** o `Data_Envio` é escrito como `%d/%m/%Y` ou `%Y-%m-%d` aleatoriamente ([linhas 69-73](gerador_dados.py#L69-L73)), que é o jeito mais rápido de quebrar um `pd.to_datetime()` que assume um formato só.
- **Valores nulos:** 10% dos `Valor_Frete_USD` saem como `None` ([linhas 76-78](gerador_dados.py#L76-L78)), deixando células vazias no CSV.
- **Capitalização inconsistente:** o `Status_Entrega` vem aleatoriamente como `ENTREGUE`, `entregue` ou `Entregue` ([linhas 81-86](gerador_dados.py#L81-L86)), então um `groupby` contaria o mesmo status três vezes.
- **Registros duplicados:** [15 linhas são copiadas](gerador_dados.py#L97-L101) dos envios já existentes e adicionadas de novo com um `ID_Transacao` novo — uma duplicata que um `drop_duplicates()` simples no ID **não** pega, porque só a chave primária mudou.
- **A chave de junção que sobrevive:** o ID numérico do cliente é o *primeiro valor* de cada registro, e é por isso que o gerador de envios usa [`list(cliente_sorteado.values())[0]`](gerador_dados.py#L62-L63) — ele não pode confiar no nome da chave, só na posição. Foi exatamente essa gambiarra que eu prototipei no `teste.py`.

## ▶️ Como rodar

```
pip install faker

python gerador_dados.py
```

O script escreve o `clientes_crm.json` e o `envios_brutos.csv` **no diretório atual** — nesse repositório o CSV fica em `data/`, então move ele pra lá (ou roda o script de dentro de `data/`) se você gerar os arquivos de novo.

**Cada execução gera um dataset diferente (não tem seed fixa), então o ETL não pode ser ajustado pra um arquivo específico — ele tem que lidar com o caso geral de verdade.**
