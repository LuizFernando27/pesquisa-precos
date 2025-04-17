import requests
import json
import os
from datetime import datetime

def coletar_pncp_exemplo():
    cnpj = "10783898000175"  # Caixa Econômica Federal
    ano = "2025"
    sequencial = "1"
    categoria = "1"

    url = f"https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/pca/{ano}/{sequencial}/itens"
    params = {
        "categoria": categoria,
        "pagina": 1,
        "tamanhoPagina": 5
    }

    headers = {"Accept": "application/json"}

    resposta = requests.get(url, headers=headers, params=params)

    if resposta.status_code == 200:
        dados = resposta.json()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("data/raw", exist_ok=True)
        caminho = f"data/raw/itens_pncp_{ts}.json"
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"\n⭐ Dados salvos em: {caminho}")
    else:
        print(f"\n❌ Erro {resposta.status_code} ao consultar a API")

if __name__ == "__main__":
    coletar_pncp_exemplo()
