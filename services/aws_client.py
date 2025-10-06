import boto3
from config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET

#sessão do boto3 com as credenciais da AWS
session = boto3.session.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


#cliente S3
s3_client = session.client('s3')

def list_files(prefix=""):
    """Lista arquivos no bucket S3 com um prefixo opcional."""
    
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)

    
    return [obj["Key"] for obj in response.get("Contents", [])]
