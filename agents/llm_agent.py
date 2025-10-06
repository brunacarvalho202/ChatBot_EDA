from typing import Tuple
from chains.llm_chains import create_sql_chain, create_pandas_chain, create_insight_chain
from tools.data_tools import execute_sql, execute_pandas
from tools.visualization_tools import plot_matplotlib_generic, plot_seaborn_generic, plot_plotly_generic
from config import S3_PARQUET_PATH

COLUMNS_INFO = """
ref_date: data de referência do registro
inadimplencia: alvo binário de inadimplência (1: Mau Pagador, 0: Bom Pagador)
sexo: sexo do indivíduo
idade: idade do indivíduo
flag_obito: flag indicando óbito
uf: unidade federativa (estado)
classe_social: classe social estimada
"""

PARQUET_PATH = S3_PARQUET_PATH

#Criação das chains
llm_sql_chain = create_sql_chain()
llm_pandas_chain = create_pandas_chain()
llm_insight_chain = create_insight_chain()


def process_user_input(user_input: str) -> Tuple[object, str]:
    #SQL
    sql_query = llm_sql_chain.invoke({
        "user_input": user_input,
        "columns_info": COLUMNS_INFO,
        "parquet_path": PARQUET_PATH
    }).content.strip()

    #remoção dos delimitadores de bloco de código
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    if not sql_query:
        raise ValueError("Nenhuma query SQL gerada pelo LLM.")

    #executa SQL
    df = execute_sql(sql_query)

    #pandas
    pandas_code = llm_pandas_chain.invoke({
        "user_input": user_input,
        "columns_info": COLUMNS_INFO
    }).content.strip()

    if pandas_code:
        #remover delimitadores de código Python, se o LLM gerar
        pandas_code = pandas_code.replace("```python", "").replace("```", "").strip()
        df = execute_pandas(df, pandas_code)

    #insight
    try:
        df_summary = df.describe(include='all').to_string()
    except Exception:
        df_summary = df.head().to_string()

    insight = llm_insight_chain.invoke({
        "user_input": user_input,
        "columns_info": COLUMNS_INFO,
        "df_summary": df_summary
    }).content

    return df, insight
