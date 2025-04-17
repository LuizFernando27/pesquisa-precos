# Projeto: Pesquisa de Preços com Dados do PNCP via API

Este projeto tem como objetivo realizar a coleta de dados públicos do Portal Nacional de Contratações Públicas (PNCP), salvando os resultados em um banco de dados PostgreSQL para posterior análise e uso em estimativas de preços para licitações.

---

## 📦 Estrutura do Projeto

```
├── data/                    # Diretório para dados temporários (ignorado pelo Git)
├── modelo_salvo_local/     # Modelos treinados (ignorado pelo Git)
├── src/
│   └── api_coleta/
│       └── pncp_contratacoes.py  # Script principal para coleta de dados homologados
├── .env                    # Variáveis de ambiente (não versionado)
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Requisitos

- Python 3.10 ou superior
- PostgreSQL instalado localmente

---

## 🐍 Configuração do Ambiente Python

1. Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate.bat  # Windows
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

> O `requirements.txt` deve conter:
> ```txt
> pandas
> requests
> python-dotenv
> SQLAlchemy
> psycopg2-binary
> ```

---

## 🛠️ Configuração do Banco de Dados PostgreSQL

1. Acesse o terminal como usuário `postgres`:

```bash
sudo -u postgres psql
```

2. Crie o banco de dados e usuário:

```sql
CREATE DATABASE pesquisa_precos;
CREATE USER coletaapis WITH PASSWORD 'Prefeitura321';
GRANT ALL PRIVILEGES ON DATABASE pesquisa_precos TO coletaapis;
\c pesquisa_precos
GRANT ALL PRIVILEGES ON SCHEMA public TO coletaapis;
GRANT USAGE ON SCHEMA public TO coletaapis;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO coletaapis;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO coletaapis;
\q
```

---

## 🔐 Variáveis de Ambiente (.env)

Crie um arquivo `.env` com as credenciais do banco:

```ini
DATABASE_URL=postgresql+psycopg2://coletaapis:Prefeitura321@localhost:5432/pesquisa_precos

POSTGRES_USER=coletaapis
POSTGRES_PASSWORD=Prefeitura321
POSTGRES_DB=pesquisa_precos
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

> **Importante:** esse arquivo **não deve ser versionado**.

---

## 🚀 Executar a Coleta de Dados

```bash
python src/api_coleta/pncp_contratacoes.py
```

O script irá:

- Consultar as APIs públicas de contratações homologadas do PNCP
- Coletar os dados de 20 processos sequenciais
- Salvar o resultado no banco PostgreSQL na tabela `pncp_contratacoes`

---

## 📌 Próximos Passos

- Integração com outras APIs públicas (ex: TCE-SP, SIASG, ComprasNet)
- Interface para seleção automática por item CATMAT
- Sistema de busca inteligente por similaridade
- Interface web para não técnicos (futura integração com Streamlit ou Flask)

---

## ✅ Status Atual

✔ Ambiente configurado com VS Code + GitHub + PostgreSQL + Python 
✔ Coleta de dados via API funcionando com armazenamento no banco
✔ Usuário exclusivo `coletaapis` configurado com segurança 

---

## 📬 Contato

Este projeto é de uso público e pode ser adaptado por qualquer prefeitura ou órgão que deseje automatizar sua coleta de preços públicos. Sinta-se à vontade para contribuir ou adaptar conforme suas necessidades!

---

> Criado com 💻 por Luiz com suporte do ChatGPT/OpenAI.
