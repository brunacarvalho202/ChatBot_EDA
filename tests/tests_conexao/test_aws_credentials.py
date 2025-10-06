import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION  # se usa config.py

try:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    s3.list_buckets()
    print("✅ Credenciais válidas — acesso autorizado à AWS.")
except NoCredentialsError:
    print("❌ Nenhuma credencial encontrada.")
except PartialCredentialsError:
    print("❌ Credenciais incompletas.")
except ClientError as e:
    code = e.response["Error"]["Code"]
    if code in ["InvalidAccessKeyId", "SignatureDoesNotMatch"]:
        print("❌ Credenciais inválidas ou expiradas.")
    elif code == "AccessDenied":
        print("❌ Credenciais válidas, mas sem permissão de acesso ao recurso.")
    else:
        print(f"⚠️ Outro erro de cliente: {code}")
