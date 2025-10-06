import unittest
import pandas as pd
from services.duckdb_service import DuckDBExecutor
from services.aws_client import list_files, S3_BUCKET
from config import S3_PARQUET_PATH

class TestPipelineIntegration(unittest.TestCase):

    def setUp(self):
        """Configura o executor DuckDB"""
        import os
        from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
        os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
        os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
        os.environ["AWS_REGION"] = AWS_REGION

        self.executor = DuckDBExecutor()

    def test_pipeline_s3_duckdb(self):
        """Testa o fluxo completo: S3 -> DuckDB -> análise"""
        #Verifica se o Parquet existe no bucket
        files = list_files()
        self.assertIn("train_dataset_neuro.parquet", files, "O Parquet esperado não está no bucket.")

        #Lê o Parquet com DuckDB
        query = f"SELECT * FROM read_parquet('{S3_PARQUET_PATH}') LIMIT 10"
        df = self.executor.run_query(query)
        self.assertFalse(df.empty, "O Parquet está vazio ou não foi possível ler.")

        #Verifica se as colunas esperadas existem
        expected_columns = ['ref_date', 'inadimplencia', 'sexo', 'idade', 'flag_obito', 'uf', 'classe_social']
        for col in expected_columns:
            self.assertIn(col, df.columns, f"A coluna esperada '{col}' não está presente no dataset.")

        #Executa uma consulta simples de análise
        # Ex: conta quantos registros existem por inadimplencia
        count_df = self.executor.run_query(f"SELECT inadimplencia, COUNT(*) AS total FROM read_parquet('{S3_PARQUET_PATH}') GROUP BY inadimplencia")
        self.assertFalse(count_df.empty, "A consulta de agregação retornou DataFrame vazio.")
        print("Resultado da contagem por inadimplencia:")
        print(count_df)

if __name__ == "__main__":
    unittest.main()
