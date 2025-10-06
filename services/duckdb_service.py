import duckdb
import pandas as pd
#from .data_cleaning import clean_dataset
import sys, os
sys.path.append(os.path.dirname(__file__))
from data_cleaning import clean_dataset

from config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_DATASET_PATH

class DuckDBExecutor:
    """Conexão básica com DuckDB para ler arquivos no S3 e executar queries SQL."""

    def __init__(self):
        #self.con.close() #Se já existir uma conexão antiga, fecha
        self.con = duckdb.connect()
        self.con.execute("INSTALL httpfs; LOAD httpfs;")
        #self.con.execute(f"SET s3_region='{AWS_REGION}';")
        #self.con.execute(f"SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';")
        #self.con.execute(f"SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY}';")
        self.con.execute(f"SET s3_region='{AWS_REGION}';")
        self.con.execute(f"SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';")
        self.con.execute(f"SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY}';")

        


    def _cast_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica cast genérico de tipos (datas, inteiros, floats, strings)."""
        for col in df.columns:
            series = df[col]

            if pd.api.types.is_datetime64_any_dtype(series) or "DATE" in str(series.dtype).upper():
                df[col] = pd.to_datetime(series, errors="coerce", utc=True)
            elif pd.api.types.is_bool_dtype(series):
                df[col] = series.astype("boolean")
            elif pd.api.types.is_integer_dtype(series):
                df[col] = series.astype("Int64")
            elif pd.api.types.is_float_dtype(series):
                df[col] = pd.to_numeric(series, errors="coerce")
                if df[col].dropna().apply(lambda x: float(x).is_integer()).all():
                    df[col] = df[col].astype("Int64")
            elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
                df[col] = df[col].astype(str).str.strip()
        return df

    def run_query(self, query: str) -> pd.DataFrame:
        """
        Executa query SQL no S3, aplica cast de tipos genéricos e passa pelo clean_dataset.
        Retorna um DataFrame limpo, padronizado e pronto para análise.
        """
        # query no DuckDB
        df = self.con.execute(query).fetchdf()

        #Normaliza nomes para lowercase e remove espaços antes do cast
        df.columns = [c.strip().lower() for c in df.columns]

        #Cast genérico de tipos
        df = self._cast_types(df)

        #Limpeza final e renomeação de colunas
        df = clean_dataset(df)

        return df
