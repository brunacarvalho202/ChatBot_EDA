# test_env_vars.py

import os
from dotenv import load_dotenv

# Carrega o .env da pasta atual
load_dotenv()

# Função auxiliar para limpar espaços e quebras de linha
def safe_get(key, default=None):
    value = os.getenv(key, default)
    return value.strip() if value else default

# Lê as variáveis
AWS_REGION = safe_get("AWS_REGION")
AWS_ACCESS_KEY_ID = safe_get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = safe_get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = safe_get("S3_BUCKET")
S3_DATASET_PATH = safe_get("S3_DATASET_PATH")

# Mostra resultados
print("🔍 Verificando variáveis carregadas:\n")
print("AWS_REGION:", AWS_REGION)
print("AWS_ACCESS_KEY_ID:", repr(AWS_ACCESS_KEY_ID))
print("AWS_SECRET_ACCESS_KEY:", repr(AWS_SECRET_ACCESS_KEY))
print("S3_BUCKET:", S3_BUCKET)
print("S3_DATASET_PATH:", S3_DATASET_PATH)

# Teste adicional — detectar possíveis quebras de linha
for key, value in {
    "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
    "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
}.items():
    if value and ("\n" in value or " " in value):
        print(f"⚠️  {key} contém espaço ou quebra de linha!")
