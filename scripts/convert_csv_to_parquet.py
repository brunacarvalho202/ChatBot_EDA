# scripts/convert_csv_to_parquet.py
import duckdb
import os
from config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET, S3_DATASET_PATH

# Configura variáveis de ambiente para DuckDB/Boto3 acessar o S3
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["AWS_REGION"] = AWS_REGION

# Conecta DuckDB
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")  # habilita leitura do S3
con.execute(f"SET s3_region='{AWS_REGION}';")
con.execute(f"SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';")
con.execute(f"SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY}';")

# Define caminho do CSV e do Parquet no S3
csv_path = S3_DATASET_PATH
parquet_path = f"s3://{S3_BUCKET}/train_dataset_neuro.parquet"

# Converte CSV para Parquet apenas com as colunas que você vai usar
con.execute(f"""
COPY (
    SELECT 
        REF_DATE,
        TARGET,
        VAR2,
        IDADE,
        VAR4,
        VAR5,
        VAR8
    FROM read_csv_auto('{csv_path}')
) TO '{parquet_path}' (FORMAT PARQUET)
""")

print(f"✅ Conversão concluída! Parquet salvo em: {parquet_path}")
