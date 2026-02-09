import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

FALLBACK = "Não tenho informações necessárias para responder sua pergunta."

load_dotenv()

def search_prompt(question: str) -> str:
  question = (question or "").strip()
  if not question:
    return FALLBACK
  
  results = search_pgVector(question)

  if not results:
        return FALLBACK

  contexto = "\n\n".join([doc.page_content for doc, _score in results]).strip()

  if not contexto:
        return FALLBACK

  prompt = PromptTemplate(
      input_variables=["contexto", "pergunta"],
      template=PROMPT_TEMPLATE,
  )

  llm = ChatOpenAI(
      model=os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano"),
      temperature=0,
  )

  chain = prompt | llm

  resposta = chain.invoke({"contexto": contexto, "pergunta": question})
  
  if hasattr(resposta, "content"):
    return resposta.content.strip()

  return str(resposta).strip()

    

def search_pgVector(question=None):
  for key in ("PGVECTOR_URL","PGVECTOR_COLLECTION", "GEMINI_EMBEDDINGS_MODEL"):
    if not os.getenv(key):
        raise RuntimeError(f"Environment variable {key} is not set.")
    
  embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")
    )
  store = PGVector(
      embeddings=embeddings,
      collection_name=os.getenv("PGVECTOR_COLLECTION"),
      connection=os.getenv("PGVECTOR_URL"),
      use_jsonb=True,
  )

  results = store.similarity_search_with_score(question, k=10)
  return results



