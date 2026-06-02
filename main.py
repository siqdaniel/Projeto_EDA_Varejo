import sys
import os
import pandas as pd
sys.path.append(os.getcwd())
from src.utils.limpeza import * 

def executar_pipeline():
    print("---  INICIANDO PIPELINE DE DADOS: VAREJO ---")
    
    # 1. CARGA
    df = pd.read_csv(r'data\raw\Base Varejo.csv', sep=';', encoding='latin1')
    
    # RELATÓRIO DE QUALIDADE INICIAL (Critério 1 e 2)
    print(f"\nREGISTROS INICIAIS: {len(df):,}")
    print(f" VALORES NULOS POR COLUNA:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f" DUPLICATAS IDENTIFICADAS: {df.duplicated().sum()}")

    # 2. LIMPEZA E TRANSFORMAÇÃO 
    # Ajuste de tipos
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')
    
    # Lógica de negócio: Categoria e Nulos
    df['PR_CAT'] = df['PR_CAT'].apply(lambda x: "Sem Categoria" if pd.isna(x) or str(x).strip() == "" else x)
    
    # Tratamento de nulos na coluna de filhos (Garantir integridade para a estatística)
    df['CL_FHL'] = pd.to_numeric(df['CL_FHL'], errors='coerce').fillna(0).astype(int)
    
    # Remoção de duplicatas
    df = df.drop_duplicates()
    
    # 3. ESTATÍSTICA DESCRITIVA
    print("\n" + "="*40)
    print(" ESTATÍSTICAS: NÚMERO DE FILHOS (CL_FHL)")
    print("="*40)
    stats_filhos = df['CL_FHL'].describe()
    print(f"Média: {stats_filhos['mean']:.2f}")
    print(f"Mediana: {df['CL_FHL'].median()}")
    print(f"Desvio Padrão: {stats_filhos['std']:.2f}")
    print(f"Moda: {df['CL_FHL'].mode()[0]}")
    print(f"Mínimo: {stats_filhos['min']}")
    print(f"Máximo: {stats_filhos['max']}")
    print(f"Quartis: Q1={stats_filhos['25%']}, Q3={stats_filhos['75%']}")

    # 4. AGRUPAMENTOS 
    print("\n" + "="*40)
    print("INSIGHTS DE AGRUPAMENTO")
    print("="*40)
    
    # Gênero com mais compras (Frequência de IDs de Compra únicos)
    genero_stats = df.groupby('CL_GENERO')['CO_ID'].nunique().sort_values(ascending=False)
    print(f"\nVolume de Compras por Gênero:\n{genero_stats}")
    
    # Top 5 Categorias
    top_categorias = df['PR_CAT'].value_counts().head(5)
    print(f"\nTop 5 Categorias mais Vendidas:\n{top_categorias}")

    print("\n PIPELINE FINALIZADO COM SUCESSO!")
    return df

# Executar
df_limpo = executar_pipeline()

