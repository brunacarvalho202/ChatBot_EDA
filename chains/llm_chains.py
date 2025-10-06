from langchain.prompts import PromptTemplate
from langchain_google_vertexai import ChatVertexAI
from config import GOOGLE_APPLICATION_CREDENTIALS
from config import PROJECT_ID, CREDENTIALS

#SQL Chain
def create_sql_chain():
    sql_prompt = PromptTemplate(
        input_variables=["user_input", "columns_info", "parquet_path"],
        template="""
Você é um cientista de dados experiente.

**Instrução:** Gere uma query SQL válida usando a função 'read_parquet()' do DuckDB para ler os dados do caminho S3. Não use `FROM {parquet_path}`, mas sim `FROM read_parquet('{parquet_path}')`.

Caminho do arquivo Parquet: {parquet_path}

Colunas disponíveis:
{columns_info}

Gere uma query SQL válida para responder:
"{user_input}"

⚙️ Retorne apenas a query SQL final, sem formatação de código (ex: ```sql).
"""
    )
    llm = ChatVertexAI(
        model_name="gemini-2.0-flash-001",
        location="global",  # Acesso garantido a modelos Vertex AI
        project=PROJECT_ID,
        credentials=CREDENTIALS,
    )
    return sql_prompt | llm


#Pandas Chain
def create_pandas_chain():
    pandas_prompt = PromptTemplate(
        input_variables=["user_input", "columns_info"],
        template="""
Colunas disponíveis:
{columns_info}

Gere código Python usando Pandas que produza 'result'.
Sem explicações.
"""
    )
    llm = ChatVertexAI(
        model_name="gemini-2.0-flash-001",
        location="global",
        project=PROJECT_ID,
        credentials=CREDENTIALS,
    )
    return pandas_prompt | llm


#Insight Chain
def create_insight_chain():
    insight_prompt = PromptTemplate(
        input_variables=["user_input", "columns_info", "df_summary"],
        template="""
Solicitação:
"{user_input}"

Colunas:
{columns_info}

Resumo dos dados:
{df_summary}

Gere um insight textual conciso.
"""
    )
    llm = ChatVertexAI(
        model_name="gemini-2.0-flash-001",
        location="global",
        project=PROJECT_ID,
        credentials=CREDENTIALS,
    )
    return insight_prompt | llm
