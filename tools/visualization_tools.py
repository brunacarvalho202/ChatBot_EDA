#tool de viualização de dados

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

def plot_matplotlib_generic(df, x_col, y_col=None, plot_type="bar", title="", save_path="plot_matplotlib.png"):
    """
    Tool genérica para criar gráficos Matplotlib.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados.
        x_col (str): Coluna para o eixo X.
        y_col (str, optional): Coluna para o eixo Y. Necessária para alguns tipos de gráfico.
        plot_type (str): Tipo de gráfico: "bar", "line", "scatter", "hist", "box".
        title (str): Título do gráfico.
        save_path (str): Caminho para salvar o gráfico.
    
    Returns:
        str: Caminho do gráfico salvo.
    """
    plt.figure(figsize=(8,6))
    
    if plot_type == "bar":
        plt.bar(df[x_col], df[y_col]) if y_col else plt.bar(df[x_col], df[x_col])
    elif plot_type == "line":
        plt.plot(df[x_col], df[y_col])
    elif plot_type == "scatter":
        plt.scatter(df[x_col], df[y_col])
    elif plot_type == "hist":
        plt.hist(df[x_col])
    elif plot_type == "box":
        plt.boxplot(df[x_col])
    else:
        raise ValueError(f"plot_type '{plot_type}' não suportado para Matplotlib")
    
    plt.title(title)
    plt.xlabel(x_col)
    if y_col:
        plt.ylabel(y_col)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    
    return save_path


def plot_seaborn_generic(df, x_col=None, y_col=None, plot_type="bar", title="", save_path="plot_seaborn.png"):
    """
    Tool genérica para criar gráficos Seaborn.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados.
        x_col (str, optional): Coluna para o eixo X.
        y_col (str, optional): Coluna para o eixo Y.
        plot_type (str): Tipo de gráfico: "bar", "line", "scatter", "hist", "box", "heatmap".
        title (str): Título do gráfico.
        save_path (str): Caminho para salvar o gráfico.
    
    Returns:
        str: Caminho do gráfico salvo.
    """
    plt.figure(figsize=(8,6))
    
    if plot_type == "bar":
        sns.barplot(data=df, x=x_col, y=y_col)
    elif plot_type == "line":
        sns.lineplot(data=df, x=x_col, y=y_col)
    elif plot_type == "scatter":
        sns.scatterplot(data=df, x=x_col, y=y_col)
    elif plot_type == "hist":
        sns.histplot(data=df, x=x_col)
    elif plot_type == "box":
        sns.boxplot(data=df, x=x_col, y=y_col)
    elif plot_type == "heatmap":
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    else:
        raise ValueError(f"plot_type '{plot_type}' não suportado para Seaborn")
    
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    
    return save_path


def plot_plotly_generic(df, x_col=None, y_col=None, plot_type="bar", title=""):
    """
    Tool genérica para criar gráficos interativos Plotly.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados.
        x_col (str, optional): Coluna para o eixo X.
        y_col (str, optional): Coluna para o eixo Y.
        plot_type (str): Tipo de gráfico: "bar", "line", "scatter", "hist", "box", "heatmap".
        title (str): Título do gráfico.
    
    Returns:
        plotly.graph_objs._figure.Figure: Objeto Plotly pronto para exibir.
    """
    fig = None
    
    if plot_type == "bar":
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    elif plot_type == "line":
        fig = px.line(df, x=x_col, y=y_col, title=title)
    elif plot_type == "scatter":
        fig = px.scatter(df, x=x_col, y=y_col, title=title)
    elif plot_type == "hist":
        fig = px.histogram(df, x=x_col, title=title)
    elif plot_type == "box":
        fig = px.box(df, x=x_col, y=y_col, title=title)
    elif plot_type == "heatmap":
        fig = px.imshow(df.corr(), text_auto=True, title=title, color_continuous_scale="RdBu_r")
    else:
        raise ValueError(f"plot_type '{plot_type}' não suportado para Plotly")
    
    return fig
