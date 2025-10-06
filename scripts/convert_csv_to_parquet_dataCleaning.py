# scripts/preprocess_csv_to_parquet_duckdb.py
import os
import sys
import duckdb
import pandas as pd

# 🔹 Adiciona a raiz do projeto e a pasta services ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))

# 🔹 Imports
from config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET, S3_DATASET_PATH
from data_cleaning import clean_dataset

# 🔹 Configura variáveis de ambiente AWS
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["AWS_REGION"] = AWS_REGION

# 🔹 Caminho final do Parquet no S3
parquet_path = f"s3://{S3_BUCKET}/train_dataset_cleaned_versao3.parquet"

# 🔹 Conecta DuckDB e habilita S3
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")
con.execute(f"SET s3_region='{AWS_REGION}';")
con.execute(f"SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';")
con.execute(f"SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY}';")

# 🔹 Ler CSV do S3 apenas com colunas necessárias
print("📥 Lendo CSV do S3 via DuckDB...")
df = con.execute(f"""
    SELECT REF_DATE, TARGET, VAR2, IDADE, VAR4, VAR5, VAR8
    FROM read_csv_auto('{S3_DATASET_PATH}')
""").df()

# 🔹 Aplicar limpeza
print("🧹 Aplicando clean_dataset...")
df_clean = clean_dataset(df)

# 🔹 Salvar como Parquet no S3
print("💾 Salvando Parquet limpo no S3...")
con.register("df_clean", df_clean)
con.execute(f"COPY df_clean TO '{parquet_path}' (FORMAT PARQUET)")

print(f"✅ Pré-processamento concluído! Parquet salvo em: {parquet_path}")
