# tests/test_duckdb_connection_extra.py

import unittest
import pandas as pd
from services.duckdb_service import DuckDBExecutor
from config import S3_PARQUET_PATH


class TestDuckDBExtra(unittest.TestCase):
    """Testes adicionais para validar leitura e integridade do dataset no S3 via DuckDB."""

    def setUp(self):
        """Instancia o executor antes de cada teste"""
        self.executor = DuckDBExecutor()

    #nomes das colunas
    def test_columns_in_parquet(self):
        query = f"SELECT * FROM read_parquet('{S3_PARQUET_PATH}') LIMIT 1"
        df = self.executor.run_query(query)

        #Imprime os nomes das colunas retornadas
        print("Colunas retornadas pelo DataFrame:", df.columns.tolist())

        #Opcional: você pode checar se não está vazio
        self.assertGreater(len(df.columns), 0, "O DataFrame não retornou colunas.")


    #Teste de leitura mínima do Parquet
    def test_can_read_from_parquet(self):
        query = f"SELECT * FROM read_parquet('{S3_PARQUET_PATH}') LIMIT 1"
        df = self.executor.run_query(query)
        self.assertEqual(len(df), 1, "Não foi possível ler uma linha do Parquet no S3.")

    #Teste de tipos de dados das colunas
    def test_column_types(self):
        query = f"SELECT ref_date, idade FROM read_parquet('{S3_PARQUET_PATH}') LIMIT 50"
        df = self.executor.run_query(query)

        # Verifica se a coluna de data foi convertida corretamente
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(pd.to_datetime(df["ref_date"], errors="coerce")),
                        "REF_DATE não está no formato datetime.")
        # Verifica se a coluna de idade é inteira
        self.assertTrue(pd.api.types.is_integer_dtype(df["idade"]),
                        "IDADE não está no formato inteiro.")

    #Teste de intervalo de datas
    def test_date_range(self):
        query = f"SELECT MIN(ref_date) as min_date, MAX(ref_date) as max_date FROM read_parquet('{S3_PARQUET_PATH}')"
        df = self.executor.run_query(query)

        min_date = pd.to_datetime(df["min_date"][0])
        max_date = pd.to_datetime(df["max_date"][0])

        self.assertLess(min_date, max_date, "As datas do dataset não estão consistentes.")

    #Teste de valores nulos
    def test_no_nulls_in_key_columns(self):
        query = f"SELECT ref_date, inadimplencia FROM read_parquet('{S3_PARQUET_PATH}') LIMIT 1000"
        df = self.executor.run_query(query)

        #Atualizado para refletir a renomeação de colunas
        self.assertFalse(df["ref_date"].isnull().any(), "Existem valores nulos em REF_DATE.")
        self.assertFalse(df["inadimplencia"].isnull().any(), "Existem valores nulos em INADIMPLENCIA.")

    #Teste de agregação simples
    def test_groupby_target(self):
        query = f"SELECT inadimplencia, COUNT(*) as cnt FROM read_parquet('{S3_PARQUET_PATH}') GROUP BY inadimplencia"
        df = self.executor.run_query(query)

        #Atualizado para refletir a renomeação de colunas
        self.assertGreater(len(df), 0, "A consulta group by não retornou resultados.")
        print(f"\nResultados do group by inadimplencia:\n{df.head()}")

if __name__ == "__main__":
    unittest.main()
