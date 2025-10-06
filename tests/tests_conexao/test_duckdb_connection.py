import unittest
import pandas as pd
import os
from services.duckdb_service import DuckDBExecutor
from config import S3_PARQUET_PATH, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

class TestDuckDBConnection(unittest.TestCase):

    def setUp(self):
        """Configura credenciais e inicializa o executor para todos os testes."""
        os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
        os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
        os.environ["AWS_REGION"] = AWS_REGION

        self.executor = DuckDBExecutor()

    def test_ref_date_equal_to_timestamp(self):
        """Consulta apenas a coluna ref_date e verifica valores específicos."""
        ts = "2017-06-01 00:00:00+00:00"
        query = f"SELECT ref_date FROM read_parquet('{S3_PARQUET_PATH}') WHERE ref_date = '{ts}' LIMIT 50"
        df = self.executor.run_query(query)

        # Garante que recebemos algum resultado
        self.assertFalse(df.empty, "A query retornou um DataFrame vazio; verifique os dados de teste.")

        # A coluna agora é renomeada pelo clean_dataset
        df['ref_date'] = pd.to_datetime(df['ref_date'], utc=True, errors='coerce')
        self.assertFalse(df['ref_date'].isna().any(), "Existem valores de ref_date inválidos ou nulos.")

        cutoff = pd.to_datetime(ts, utc=True)
        self.assertTrue((df['ref_date'] == cutoff).all(), "Existem valores de ref_date que não são iguais ao timestamp esperado.")

    def test_list_columns(self):
        """Retorna e verifica as colunas presentes no dataset Parquet."""
        query = f"SELECT * FROM read_parquet('{S3_PARQUET_PATH}') LIMIT 1"
        df = self.executor.run_query(query)

        # Verifica se o DataFrame não está vazio
        self.assertFalse(df.empty, "O Parquet está vazio; não há colunas para verificar.")

        # Obtém o nome das colunas
        columns = list(df.columns)
        print(f"Colunas presentes no dataset: {columns}")

        # Verificação simples: garante que algumas colunas esperadas existem (após renomeação)
        expected_columns = ["ref_date", "inadimplencia", "sexo", "idade", "flag_obito", "uf", "classe_social"]
        for col in expected_columns:
            self.assertIn(col, columns, f"A coluna esperada '{col}' não está presente no dataset.")


if __name__ == "__main__":
    unittest.main()
