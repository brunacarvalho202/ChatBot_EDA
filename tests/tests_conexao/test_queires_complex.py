import os
import unittest
import pandas as pd

from services.duckdb_service import DuckDBExecutor
from config import S3_PARQUET_PATH, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

"""queries de agregação e tendência para validar 
contagens, médias, top‑N e taxa mensal de inadimplência no dataset."""

class TestDuckDBComplexQueries(unittest.TestCase):
    def setUp(self):
        # garante credenciais disponíveis para httpfs / boto config usados pelo DuckDBExecutor
        os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID or ""
        os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY or ""
        os.environ["AWS_REGION"] = AWS_REGION or ""
        self.executor = DuckDBExecutor()

    def _assert_non_empty(self, df: pd.DataFrame, msg: str):
        self.assertFalse(df.empty, msg)


    """Objetivo: contar quantos registros existem por sexo (VAR2) e por TARGET (inadimplência), ou seja, 
        distribuir a quantidade de bons/maus pagadores por sexo.
        Saída esperada: tabela com colunas (sex, target, cnt) — cnt = número de registros por combinação."""

    def test_count_per_target_by_sex(self):
        """Contagem por inadimplência e sexo (sexo)."""
        q = f"""
        SELECT sexo AS sex, inadimplencia AS target, COUNT(*) AS cnt
        FROM read_parquet('{S3_PARQUET_PATH}')
        WHERE sexo IS NOT NULL
        GROUP BY sexo, inadimplencia
        ORDER BY sexo, inadimplencia
        LIMIT 100
        """
        df = self.executor.run_query(q)
        self._assert_non_empty(df, "Query retornou DataFrame vazio: count_per_target_by_sex")

        # O pipeline normaliza para lowercase e renomeia 'target' -> 'inadimplencia'
        self.assertIn("sex", df.columns)
        self.assertIn("inadimplencia", df.columns)
        self.assertIn("cnt", df.columns)

        # garante que 'cnt' é numérico e existe ao menos uma contagem > 0
        df["cnt"] = pd.to_numeric(df["cnt"], errors="coerce")
        self.assertTrue((df["cnt"] > 0).any())

        # mostra saída da query para inspeção rápida durante o teste
        print("\n--- test_count_per_target_by_sex: query result columns ---")
        print(df.columns.tolist())
        print("\n--- test_count_per_target_by_sex: head ---")
        # to_string evita truncamento no output do unittest
        print(df.head(10).to_string(index=False))

    def test_mean_age_bad_payers_by_uf(self):
        """Média de IDADE para maus pagadores (TARGET=1) por UF (VAR5)."""
        q = f"""
        SELECT uf, AVG(idade) AS mean_age
        FROM read_parquet('{S3_PARQUET_PATH}')
        WHERE inadimplencia = 1 AND uf IS NOT NULL
        GROUP BY uf
        ORDER BY mean_age DESC
        LIMIT 20
        """
        df = self.executor.run_query(q)
        self._assert_non_empty(df, "Query retornou DataFrame vazio: mean_age_bad_payers_by_uf")

        # No pipeline as colunas ficam em lowercase e 'target' pode ser renomeado por clean_dataset
        self.assertIn("uf", df.columns)
        self.assertIn("mean_age", df.columns)

        # imprime saída para inspeção rápida durante o teste
        print("\n--- test_mean_age_bad_payers_by_uf: query result columns ---")
        print(df.columns.tolist())
        print("\n--- test_mean_age_bad_payers_by_uf: head ---")
        print(df.head(10).to_string(index=False))

        # garante que 'mean_age' é numérico e não nulo
        df["mean_age"] = pd.to_numeric(df["mean_age"], errors="coerce")
        self.assertTrue((df["mean_age"].notna()).all())

    def test_top5_max_age_by_social_class(self):
        """Top 5 classes sociais com maior idade máxima."""
        q = f"""
        SELECT classe_social AS class_social, MAX(idade) AS max_age
        FROM read_parquet('{S3_PARQUET_PATH}')
        WHERE classe_social IS NOT NULL
        GROUP BY classe_social
        ORDER BY max_age DESC
        LIMIT 5
        """
        df = self.executor.run_query(q)
        self._assert_non_empty(df, "Query retornou DataFrame vazio: top5_max_age_by_social_class")
        self.assertIn("class_social", df.columns)
        self.assertIn("max_age", df.columns)
        self.assertLessEqual(len(df), 5)
        self.assertTrue((df["max_age"] > 0).any())

        #imprime saída para inspeção rápida durante o teste
        print("\n--- test_top5_max_age_by_social_class: query result columns ---")
        print(df.columns.tolist())
        print("\n--- test_top5_max_age_by_social_class: head ---")
        print(df.head(5).to_string(index=False))

    def test_monthly_bad_rate_trend(self):
        """Taxa de inadimplência média por mês (trend) — verifica intervalo [0,1]."""
        q = f"""
        SELECT STRFTIME(ref_date, '%Y-%m') AS ym,
            AVG(CAST(inadimplencia AS DOUBLE)) AS bad_rate
        FROM read_parquet('{S3_PARQUET_PATH}')
        WHERE ref_date IS NOT NULL
        GROUP BY ym
        ORDER BY ym
        LIMIT 12
        """
        df = self.executor.run_query(q)
        self._assert_non_empty(df, "Query retornou DataFrame vazio: monthly_bad_rate_trend")
        self.assertIn("ym", df.columns)
        self.assertIn("bad_rate", df.columns)

        # verifica que as taxas estejam no intervalo esperado
        self.assertTrue(((df["bad_rate"] >= 0) & (df["bad_rate"] <= 1)).all())


if __name__ == "__main__":
    unittest.main()