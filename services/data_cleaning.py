import pandas as pd
import numpy as np

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e padroniza o dataset para uso pelo chatbot.
    - Cria colunas originais para auditoria.
    - Padroniza colunas conhecidas.
    - Faz a conversão de tipo, mas não remove linhas ou colunas.
    """

    #Normaliza nomes de colunas: lowercase e remove espaços
    df.columns = [c.strip().lower() for c in df.columns]
    
    #Renomeia colunas conhecidas
    rename_map = {
        "ref_date": "ref_date",
        "target": "inadimplencia",
        "var2": "sexo",
        "idade": "idade",
        "var4": "flag_obito",
        "var5": "uf",
        "var8": "classe_social"
    }
    existing_rename = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=existing_rename)
    
    #Aviso sobre colunas esperadas não encontradas
    missing_cols = [v for k,v in rename_map.items() if k not in df.columns]
    if missing_cols:
        print(f"⚠️ Colunas esperadas não encontradas no CSV: {missing_cols}")
    
    if "ref_date" in df.columns:
        df["ref_date_orig"] = df["ref_date"]
        df["ref_date"] = pd.to_datetime(df["ref_date"], errors="coerce", utc=True)

    if "inadimplencia" in df.columns:
        df["inadimplencia_orig"] = df["inadimplencia"]
        df["inadimplencia"] = pd.to_numeric(df["inadimplencia"], errors="coerce")
        # Substitui valores fora do intervalo [0, 1] por NaN, sem remover linhas
        df["inadimplencia"] = df["inadimplencia"].mask(
            (df["inadimplencia"] < 0) | (df["inadimplencia"] > 1)
        )
        df["inadimplencia"] = df["inadimplencia"].astype("Int64", errors="ignore")

    if "sexo" in df.columns:
        df["sexo_orig"] = df["sexo"]
        df["sexo"] = df["sexo"].astype(str).str.strip().str.upper()
        df["sexo"] = df["sexo"].replace({"M": "Masculino", "F": "Feminino"})
        # Marca valores inválidos como NaN, sem remover
        df.loc[~df["sexo"].isin(["Masculino", "Feminino"]), "sexo"] = np.nan

    if "idade" in df.columns:
        df["idade_orig"] = df["idade"]
        df["idade"] = pd.to_numeric(df["idade"], errors="coerce")
        # Marca valores fora do intervalo como NaN, sem remover
        df.loc[(df["idade"] < 18) | (df["idade"] > 120), "idade"] = np.nan
        df["idade"] = df["idade"].round(0).astype("Int64", errors="ignore")
    
    if "flag_obito" in df.columns:
        df["flag_obito_orig"] = df["flag_obito"]
        df["flag_obito"] = df["flag_obito"].astype(str).str.strip().str.upper()
        df["flag_obito"] = df["flag_obito"].replace({"S": "Sim", "N": "Não"})
        # Marca valores inválidos como NaN, sem remover
        df.loc[~df["flag_obito"].isin(["Sim","Não"]), "flag_obito"] = np.nan

    if "uf" in df.columns:
        df["uf_orig"] = df["uf"]
        df["uf"] = df["uf"].astype(str).str.strip().str.upper()
        valid_ufs = [
            "AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG",
            "MS","MT","PA","PB","PE","PI","PR","RJ","RN","RO","RR",
            "RS","SC","SE","SP","TO"
        ]
        # Marca UFs inválidas como NaN, sem remover
        df.loc[~df["uf"].isin(valid_ufs), "uf"] = np.nan

    if "classe_social" in df.columns:
        df["classe_social_orig"] = df["classe_social"]
        df["classe_social"] = df["classe_social"].astype(str).str.strip().str.upper()
        df["classe_social"] = df["classe_social"].replace({
            "A": "Classe A", "B": "Classe B", "C": "Classe C", "D": "Classe D", "E": "Classe E"
        })
        # Marca classes sociais inválidas como NaN, sem remover
        df.loc[~df["classe_social"].isin(
            ["Classe A", "Classe B", "Classe C", "Classe D", "Classe E"]
        ), "classe_social"] = np.nan

    #Colunas desconhecidas (agregadas/calculadas)
    known_cols = set(rename_map.values())
    for col in df.columns:
        if col not in known_cols and not col.endswith("_orig"):
            series = df[col]
            if pd.api.types.is_datetime64_any_dtype(series) or "date" in col:
                df[col] = pd.to_datetime(series, errors="coerce", utc=True)
            elif pd.api.types.is_integer_dtype(series):
                df[col] = series.astype("Int64", errors="ignore")
            elif pd.api.types.is_float_dtype(series):
                df[col] = pd.to_numeric(series, errors="coerce")
                if df[col].dropna().apply(lambda x: float(x).is_integer()).all():
                    df[col] = df[col].astype("Int64", errors="ignore")
            elif pd.api.types.is_object_dtype(series):
                df[col] = series.astype(str).str.strip()
    
    #Reordena colunas conhecidas
    ordered_cols = ["ref_date","inadimplencia","sexo","idade","flag_obito","uf","classe_social"]
    df = df[[c for c in ordered_cols if c in df.columns] + [c for c in df.columns if c not in ordered_cols and not c.endswith('_orig')]]

    return df
