# tests/tests_tools/test_data_tools.py

import sys
import os

# Adiciona a raiz do projeto ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Agora os imports funcionam
import pytest
import pandas as pd
from unittest.mock import MagicMock
from tools.data_tools import execute_sql, execute_pandas, generate_insight



# 🔹 Mock DataFrame
df_mock = pd.DataFrame({
    "idade": [25, 30, 35, 40, 45],
    "uf": ["SP", "RJ", "MG", "RS", "BA"],
    "sexo": ["Masculino", "Feminino", "Masculino", "Feminino", "Masculino"]
})

# -----------------------------
# Teste SQL Tool
# -----------------------------
def test_execute_sql(monkeypatch):
    # Criar mock do DuckDBExecutor
    mock_df = pd.DataFrame({"col": [1, 2, 3]})

    class MockExecutor:
        def run_query(self, query):
            return mock_df

    # Patch DuckDBExecutor para retornar o mock
    monkeypatch.setattr("tools.data_tools.DuckDBExecutor", lambda: MockExecutor())

    sql_query = "SELECT * FROM tabela"
    df = execute_sql(sql_query)
    assert isinstance(df, pd.DataFrame)
    assert df.equals(mock_df)
     # 🔹 Mostra o resultado no terminal
    print("\n===== RESULTADO DA CONSULTA =====")
    print(df)
    print("=================================")

# -----------------------------
# Teste SQL Tool com mock realista
# -----------------------------
def test_execute_sql_realistic_mock(monkeypatch):
    # Criar mock do DuckDBExecutor
    class MockExecutor:
        def run_query(self, query):
            return df_mock

    # Patch DuckDBExecutor para retornar o mock
    monkeypatch.setattr("tools.data_tools.DuckDBExecutor", lambda: MockExecutor())

    sql_query = "SELECT * FROM tabela"
    df = execute_sql(sql_query)

    # Testes básicos
    assert isinstance(df, pd.DataFrame)
    assert df.equals(df_mock)

    # Opcional: imprimir para visualizar durante o teste
    print("\n===== RESULTADO DA CONSULTA COM MOCK REALISTA =====")
    print(df)

    """===== RESULTADO DA CONSULTA COM MOCK REALISTA =====
    idade  uf       sexo
   0  25  SP  Masculino
   1  30  RJ   Feminino
   2  35  MG  Masculino
   3  40  RS   Feminino
   4  45  BA  Masculino"""

# -----------------------------
# Teste Pandas Tool
# -----------------------------
def test_execute_pandas():
    pandas_code = """
result = df[df['idade'] > 30]
"""
    result_df = execute_pandas(df_mock, pandas_code)
    assert isinstance(result_df, pd.DataFrame)
    assert (result_df['idade'] > 30).all()

    # Teste erro em código inválido
    invalid_code = "result = df['col_inexistente']"
    with pytest.raises(ValueError):
        execute_pandas(df_mock, invalid_code)

# -----------------------------
# Teste Insight Tool realista
# -----------------------------
def test_generate_insight_realistic():
    # Contexto coerente com o df_mock
    context_mock = """
idade: idade do indivíduo
uf: unidade federativa do indivíduo
sexo: sexo do indivíduo
"""

    # Mock do LLM que gera insight baseado nos dados
    class MockLLM:
        def __call__(self, prompt: str) -> str:
            if "idade" in prompt:
                media = df_mock['idade'].mean()
                return f"A média de idade no dataset é {media:.1f} anos."
            if "sexo" in prompt:
                qtd_m = (df_mock['sexo'] == "Masculino").sum()
                qtd_f = (df_mock['sexo'] == "Feminino").sum()
                return f"Há {qtd_m} homens e {qtd_f} mulheres no dataset."
            return "Nenhum insight gerado."

    llm = MockLLM()

    insight = generate_insight(df_mock, llm=llm, context=context_mock)

    # 🔹 Print do insight
    print("\n" + "="*30)
    print("=== RESULTADO DO INSIGHT REALISTA ===")
    print(insight)
    print("="*30 + "\n")

    # 🔹 Asserções básicas
    assert isinstance(insight, str)
    assert len(insight) > 0


