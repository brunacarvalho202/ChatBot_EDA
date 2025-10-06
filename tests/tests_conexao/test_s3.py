import boto3
import pandas as pd
from io import BytesIO
from config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET, S3_PARQUET_PATH
from dotenv import load_dotenv

load_dotenv()

def test_s3_access():
    """Testa o acesso ao S3 e a leitura do arquivo parquet usando boto3."""
    # Extrair apenas o key do S3
    key = S3_PARQUET_PATH.replace(f"s3://{S3_BUCKET}/", "")
    
    try:
        s3 = boto3.client(
            's3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        print(AWS_ACCESS_KEY_ID)
        response = s3.get_object(Bucket=S3_BUCKET, Key=key)
        df_from_boto3 = pd.read_parquet(BytesIO(response['Body'].read()))
        print("✅ Sucesso! DataFrame carregado com boto3.")
        print(df_from_boto3.head())

    except Exception as e:
        print(f"❌ Erro ao carregar com boto3: {e}")

if __name__ == "__main__":
    test_s3_access()
