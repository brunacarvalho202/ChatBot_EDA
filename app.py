# app.py
import streamlit as st
from agents.llm_agent import process_user_input
import pandas as pd
from PIL import Image
import os
from dotenv import load_dotenv

# --- Chama load_dotenv() no início do script para carregar as variáveis do .env ---
load_dotenv()  

st.set_page_config(page_title="Chatbot de Análise de Dados", page_icon="💬")
st.title("💬 Chatbot de Análise de Dados")

# Inicializa histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Caixa de entrada
user_input = st.chat_input("Digite sua pergunta ou solicitação de análise:")

if user_input:
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Processa entrada do usuário via LangChain
        df, insight_or_plot = process_user_input(user_input)

        # Cria conteúdo do assistente
        assistant_content = []

        # Texto introdutório ou DataFrame
        if isinstance(df, pd.DataFrame):
            assistant_content.append(("text", "Aqui estão os dados:"))
            assistant_content.append(("dataframe", df))

        # Gráfico (imagem)
        if isinstance(insight_or_plot, str) and (insight_or_plot.endswith(".png") or insight_or_plot.endswith(".jpg")):
            assistant_content.append(("text", "Segue o gráfico gerado:"))
            assistant_content.append(("image", insight_or_plot))

        # Insight textual
        elif isinstance(insight_or_plot, str) and not (insight_or_plot.endswith(".png") or insight_or_plot.endswith(".jpg")):
            assistant_content.append(("text", insight_or_plot))

        # Adiciona ao histórico
        st.session_state.messages.append({"role": "assistant", "content": assistant_content})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": [("text", f"Erro ao processar a solicitação: {e}")]})


# Renderiza histórico de mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        content = msg["content"]
        if isinstance(content, list):  # assistente com múltiplos elementos
            for item_type, item in content:
                if item_type == "text":
                    st.markdown(item)
                elif item_type == "dataframe":
                    st.dataframe(item)
                elif item_type == "image":
                    img = Image.open(item)
                    st.image(img)
        else:  # usuário simples
            st.markdown(content)
