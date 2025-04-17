import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do .env
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# Define os parâmetros do endpoint base
BASE_URL = "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens"
CNPJ_ORGAO = "04384829000196"
ANO_COMPRA = 2024
SEQUENCIAL_INICIAL = 1
SEQUENCIAL_FINAL = 20

# Lista para armazenar os resultados
itens_contratacoes = []

print("📥 Iniciando coleta de dados do PNCP...")

# Coleta de dados via API
def coletar_dados():
    for sequencial in range(SEQUENCIAL_INICIAL, SEQUENCIAL_FINAL + 1):
        url = BASE_URL.format(cnpj=CNPJ_ORGAO, ano=ANO_COMPRA, sequencial=sequencial)
        print(f"🔎 Consultando: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()
            itens_contratacoes.extend(dados)
        except requests.RequestException as e:
            print(f"⚠️ Erro ao consultar {url}: {e}")

# Armazena os dados no PostgreSQL
def salvar_no_postgres():
    if not itens_contratacoes:
        print("⚠️ Nenhum dado para salvar.")
        return

    df = pd.DataFrame(itens_contratacoes)

    # Cria engine de conexão usando variáveis de ambiente
    conn_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(conn_string)

    # Salva os dados na tabela (cria se não existir)
    df.to_sql("pncp_contratacoes", con=engine, if_exists="append", index=False)
    print(f"✅ Dados salvos com sucesso no banco PostgreSQL!")

if __name__ == "__main__":
    coletar_dados()
    print(f"✅ Total de itens obtidos: {len(itens_contratacoes)}")
    salvar_no_postgres()
