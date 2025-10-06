# Use Python 3.10 slim como base
FROM python:3.10-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements.txt primeiro (para melhor cache)
COPY requirements.txt .

# Instala dependências do sistema necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Atualiza pip e instala dependências Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . .

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Define variáveis de ambiente para rodar Streamlit no container
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Comando padrão para iniciar a aplicação
CMD ["streamlit", "run", "app.py"]
