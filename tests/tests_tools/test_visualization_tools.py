import pytest
import pandas as pd
import matplotlib.figure
import plotly.graph_objects as go
import sys
import os
import tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tools')))
from visualization_tools import (
    plot_matplotlib_generic,
    plot_seaborn_generic,
    plot_plotly_generic
)

# 🔹 Mock DataFrame para testes
df_mock = pd.DataFrame({
    "idade": [25, 30, 35, 40, 45],
    "uf": ["SP", "RJ", "MG", "RS", "BA"],
    "sexo": ["Masculino", "Feminino", "Masculino", "Feminino", "Masculino"]
})

# -----------------------------
# Teste Matplotlib
# -----------------------------
def test_plot_matplotlib():
    fig_path  = plot_matplotlib_generic(df_mock, x_col="uf", y_col="idade", plot_type="bar")
    assert isinstance(fig_path, str)
    assert fig_path.endswith(".png")


# -----------------------------
# Teste Seaborn
# -----------------------------
def test_plot_seaborn():
    fig_path = plot_seaborn_generic(df_mock, x_col="uf", y_col="idade", plot_type="bar")
    assert isinstance(fig_path, str)
    assert fig_path.endswith(".png")
    assert os.path.exists(fig_path)

# -----------------------------
# Teste Plotly
# -----------------------------
def test_plot_plotly():
    # Gera o gráfico (objeto Figure)
    fig = plot_plotly_generic(df_mock, x_col="uf", y_col="idade", plot_type="bar")
    
    # Verifica se é realmente um objeto Figure
    assert isinstance(fig, go.Figure)

    # Salva temporariamente como HTML para visualizar durante o teste
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, "test_plotly_bar.html")
    fig.write_html(file_path)

    # Checa se o arquivo foi criado
    assert os.path.exists(file_path)

    print(f"Abra este arquivo no navegador para ver o gráfico: {file_path}")

# -----------------------------
# Teste Plotly para tipos diferentes
# -----------------------------
@pytest.mark.parametrize("plot_type", ["bar", "line", "scatter", "box", "hist"])
def test_plotly_various_types(plot_type):
    fig = plot_plotly_generic(df_mock, x_col="uf", y_col="idade", plot_type=plot_type)
    
    # Verifica tipo do objeto
    assert isinstance(fig, go.Figure)
    
    # Salva em HTML temporário para inspeção
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        fig.write_html(tmpfile.name)
        print(f"Gráfico {plot_type} salvo em HTML temporário: {tmpfile.name}")
        assert os.path.exists(tmpfile.name)