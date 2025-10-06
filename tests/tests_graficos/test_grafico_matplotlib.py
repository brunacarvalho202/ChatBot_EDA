import os
import unittest
import matplotlib.pyplot as plt
import pandas as pd
from services.duckdb_service import DuckDBExecutor  # ajuste conforme o seu projeto
from config import S3_PARQUET_PATH


class TestGraficoMatplotlib(unittest.TestCase):
    """
    Teste unitário: gera gráfico de taxa média de inadimplência por mês e salva em arquivo.
    """

    def setUp(self):
        # Instancia o executor DuckDB e garante o diretório de saída
        self.executor = DuckDBExecutor()
        self.output_dir = os.path.join(os.path.dirname(__file__), "test_graficos")
        os.makedirs(self.output_dir, exist_ok=True)

    def test_plot_monthly_bad_rate(self):
        """Gera e valida o gráfico da taxa média de inadimplência mensal."""

        # 1️⃣ Query SQL sobre o parquet limpo
        sql = f"""
        SELECT STRFTIME(ref_date, '%Y-%m') AS ym,
               AVG(CAST(inadimplencia AS DOUBLE)) AS bad_rate
        FROM read_parquet('{S3_PARQUET_PATH}')
        WHERE ref_date IS NOT NULL
        GROUP BY ym
        ORDER BY ym
        LIMIT 12
        """
        df = self.executor.run_query(sql)

        # 2️⃣ Valida retorno do DuckDB
        self.assertFalse(df.empty, "Query retornou DataFrame vazio.")
        self.assertIn("ym", df.columns)
        self.assertIn("bad_rate", df.columns)

        df["bad_rate"] = pd.to_numeric(df["bad_rate"], errors="coerce")
        df = df.dropna(subset=["bad_rate"])
        self.assertTrue(((df["bad_rate"] >= 0) & (df["bad_rate"] <= 1)).all())

        # 3️⃣ Gera gráfico com matplotlib
        plt.figure(figsize=(10, 5))
        plt.plot(df["ym"], df["bad_rate"], marker='o', linestyle='-', color='blue')
        plt.title("Taxa média de inadimplência por mês")
        plt.xlabel("Mês (YYYY-MM)")
        plt.ylabel("Taxa de inadimplência (0-1)")
        plt.grid(True)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # 4️⃣ Salva na subpasta local (tests/tests_graficos/test_graficos)
        output_path = os.path.join(self.output_dir, "grafico_inadimplencia_mensal.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        # 5️⃣ Testa se o arquivo foi gerado
        self.assertTrue(os.path.exists(output_path), f"Arquivo não encontrado: {output_path}")
        self.assertGreater(os.path.getsize(output_path), 0, "Arquivo gerado está vazio.")

        print(f"\n✅ Gráfico gerado com sucesso: {output_path}")
        print(df.head())


if __name__ == "__main__":
    unittest.main()
