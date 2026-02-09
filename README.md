# Desafio MBA Engenharia de Software com IA - Full Cycle

Este repositório contém a solução do desafio de **Ingestão e Busca Semântica em documentos PDF**, utilizando **LangChain**, **PostgreSQL com extensão pgVector** e execução via **Docker**.

A aplicação permite que o conteúdo de um PDF seja ingerido, transformado em embeddings vetoriais e armazenado em banco de dados. Em seguida, o usuário pode realizar perguntas via **linha de comando (CLI)** e receber respostas baseadas **exclusivamente no conteúdo do documento**, seguindo regras estritas para evitar respostas fora de contexto.

---

## 🎯 Objetivo

Entregar um software capaz de:

- Ler um arquivo PDF
- Dividir o texto em **chunks de 1000 caracteres com overlap de 150**
- Gerar embeddings para cada chunk
- Armazenar os vetores no **PostgreSQL + pgVector**
- Permitir consultas semânticas via **CLI**
- Responder **somente com base no conteúdo do PDF**
- Retornar uma mensagem padrão para perguntas fora do contexto


---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **LangChain**
- **PostgreSQL**
- **pgVector**
- **Docker & Docker Compose**
- **OpenAI API**
  - Embeddings: `text-embedding-3-small`
  - LLM: `gpt-5-nano`

---

## 🚀 Como Executar o Projeto

### 1️⃣ Pré-requisitos

- Docker instalado
- Docker Compose instalado
- Python 3.10 ou superior
- API Key válida da OpenAI (com créditos ativos)

---

### 2️⃣ Subir o Banco de Dados

Na raiz do projeto, execute:

```bash
docker compose up -d

Esse comando irá subir o PostgreSQL e habilitar automaticamente a extensão pgVector.

---

### 3️⃣ Criar e Ativar Ambiente Virtual
python -m venv venv


```Windows

venv\Scripts\activate


```Linux / macOS

source venv/bin/activate

---

### 4️⃣ Instalar Dependências
pip install -r requirements.txt

---

### 5️⃣ Configurar Variáveis de Ambiente

Crie o arquivo .env a partir do exemplo:

cp .env.example .env


Edite o arquivo .env e informe sua chave da OpenAI:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

OPENAI_EMBEDDINGS_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-5-nano

PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=pdf_collection

---

### 6️⃣ Ingestão do PDF

Coloque o arquivo document.pdf na raiz do projeto.

Execute:

python src/ingest.py


Ou, para informar outro PDF:

python src/ingest.py caminho/para/arquivo.pdf


Ao final da execução, será exibida uma mensagem informando quantos chunks foram ingeridos.

---

### 7️⃣ Executar o Chat (CLI)
python src/chat.py


Exemplo de uso:

Faça sua pergunta (digite 'sair' para encerrar):

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.


Exemplo de pergunta fora do contexto:

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
