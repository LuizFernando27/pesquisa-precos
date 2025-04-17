# src/api_coleta/pncp_contratacoes_diretas.py

import requests
import pandas as pd
import os
from datetime import datetime

def coletar_contratacoes_diretas(cnpj="04384829000196", ano="2024", sequencias=20):
    base_url = f"https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{{}}/itens"
    all_items = []

    for sequencial in range(1, sequencias + 1):
        url = base_url.format(sequencial)
        print(f"🔍 Consultando: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            items = response.json()
            all_items.extend(items)
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao consultar {url}: {e}")
            continue

    if all_items:
        df = pd.DataFrame(all_items)
        os.makedirs("data/raw", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"data/raw/contratacoes_diretas_{ts}.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n✅ Arquivo CSV salvo em: {csv_path}")
    else:
        print("⚠️ Nenhum item retornado.")

if __name__ == "__main__":
    coletar_contratacoes_diretas()
