#tool de sql, pandas e insights
import pandas as pd
from services.duckdb_service import DuckDBExecutor
from langchain.chat_models import ChatOpenAI

#SQL Tool
def execute_sql(sql_query: str) -> pd.DataFrame:
    """
    Recebe uma query SQL, executa no DuckDB e retorna DataFrame.
    """
    executor = DuckDBExecutor()
    df = executor.run_query(sql_query)
    return df


#pandas Tool
def execute_pandas(df: pd.DataFrame, pandas_code: str) -> pd.DataFrame:
    """
    Recebe um DataFrame e um código Pandas em string, executa e retorna resultado.
    """
    local_vars = {"df": df, "pd": pd}
    try:
        exec(pandas_code, {}, local_vars)
        #resultado final está em 'result'
        return local_vars.get("result", df)
    except Exception as e:
        raise ValueError(f"Erro executando código Pandas: {e}")


#insight Tool
def generate_insight(df: pd.DataFrame, llm: ChatOpenAI, context: str) -> str:
    """
    Recebe DataFrame e LLM, retorna insight textual sobre os dados.
    """
    #transformar DataFrame em string resumida
    summary = df.describe(include='all').to_string()
    prompt = f"""
        Você é um cientista de dados senior.
        Com base nos dados abaixo e no contexto:
        {context}

        Resumo dos dados:
        {summary}

        Gere um insight conciso e relevante para o usuário.
        """
    response = llm(prompt)
    return response
