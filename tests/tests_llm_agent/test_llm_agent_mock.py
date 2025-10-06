# tests/tests_llm_agent/test_llm_agent_mock.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pandas as pd
import pytest
from unittest.mock import MagicMock
import agents.llm_agent as llm_agent


# 🔹 FakeLLM simples que substitui LLMChain.llm
class FakeLLM:
    def __init__(self, response):
        self.response = response

    def __call__(self, **kwargs):
        # LLMChain moderno chama __call__ com dicionário de inputs
        return {"text": self.response}


def test_process_user_input_with_mocks(monkeypatch):
    """
    Teste do pipeline completo do agente usando mocks:
    SQL -> DuckDB (mock) -> Pandas -> Insight
    sem chamar a OpenAI.
    """

    # 🔹 Mock do DuckDBExecutor: devolve DataFrame fixo
    df_mock = pd.DataFrame({
        "idade": [25, 30, 40],
        "uf": ["SP", "RJ", "MG"],
        "inadimplencia": [0, 1, 0]
    })
    monkeypatch.setattr("tools.data_tools.execute_sql", lambda query: df_mock)

    # 🔹 Mock de execute_pandas (simula código aplicado)
    def fake_execute_pandas(df, code):
        return df[df["idade"] > 30]
    monkeypatch.setattr("tools.data_tools.execute_pandas", fake_execute_pandas)

    # 🔹 Substitui os LLMs internos por FakeLLM
    llm_agent.llm_sql_chain.llm = FakeLLM("SELECT * FROM read_parquet('mock')")
    llm_agent.llm_pandas_chain.llm = FakeLLM("result = df[df['idade'] > 30]")
    llm_agent.llm_insight_chain.llm = FakeLLM("Pessoas mais velhas têm menor inadimplência.")

    # 🔹 Executa pipeline
    df_result, insight = llm_agent.process_user_input("Quais estados têm menor inadimplência?")

    # 🔹 Asserções
    assert isinstance(df_result, pd.DataFrame)
    assert not df_result.empty
    assert insight == "Pessoas mais velhas têm menor inadimplência."

    # 🔹 Prints para conferência
    print("\n=== RESULTADO FINAL DO TESTE ===")
    print(df_result)
    print("Insight:", insight)
    print("================================\n")
