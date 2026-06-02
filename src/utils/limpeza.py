import pandas as pd
import numpy as np
import re

def transformar_strings(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    """
    Remove espaços extras, converte para minúsculo e remove caracteres 
    especiais de colunas de texto.
    """
    for col in colunas:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .str.normalize('NFKD')
                .encode('ascii', errors='ignore')
                .decode('utf-8')
            )
    return df

def converter_para_numerico(df: pd.DataFrame, colunas: list, tipo='float') -> pd.DataFrame:
    """
    Trata strings com padrão brasileiro  e converte para float ou int.
    """
    for col in colunas:
        if col in df.columns:
            # Remove pontos de milhar e troca vírgula por ponto
            df[col] = (
                df[col]
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
                .str.extract(r'(\d+\.?\d*)')[0] # Extrai apenas números e ponto
            )
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            if tipo == 'int':
                df[col] = df[col].fillna(0).astype(int)
                
    return df

def transformar_datetime(df: pd.DataFrame, colunas: list, formato: str = None) -> pd.DataFrame:
    """
    Converte colunas para o tipo datetime, tratando erros como NaT.
    """
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format=formato, errors='coerce')
    return df


def limpar_base_varejo(df):
    # 1. Ajuste de Tipos (Sprint 2)
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
    
    # 2. Tratamento de Nulos (Sprint 3 - Critério 4)
    # Lógica if/else para categorias vazias
    df['PR_CAT'] = df['PR_CAT'].apply(lambda x: "Sem Categoria" if pd.isna(x) or x == "" else x)
    
    # 3. Tratamento de Filhos (Garantir que seja numérico)
    df['CL_FHL'] = pd.to_numeric(df['CL_FHL'], errors='coerce').fillna(0).astype(int)
    
    # 4. Remover Duplicatas
    total_antes = len(df)
    df = df.drop_duplicates()
    print(f"Registros duplicados removidos: {total_antes - len(df)}")
    
    return df

def gerar_relatorio_estatistico(df):
    col = 'CL_FHL'
    stats = df[col].describe()
    
    print(f"--- Estatísticas Descritivas: Número de Filhos ---")
    print(f"Média: {stats['mean']:.2f}")
    print(f"Mediana: {df[col].median()}")
    print(f"Desvio Padrão: {stats['std']:.2f}")
    print(f"Moda: {df[col].mode()[0]}")
    print(f"Mínimo: {stats['min']}")
    print(f"Máximo: {stats['max']}")
    print(f"Contagem: {int(stats['count'])}")
    print(f"Quartis: Q1={stats['25%']}, Q2={stats['50%']}, Q3={stats['75%']}")

 