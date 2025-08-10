# Arquivo: utils.py
import streamlit as st
import pandas as pd
import gspread

# A função de conexão pode ser chamada uma vez e o resultado cacheado
@st.cache_resource
def connect_to_gsheets():
    GSPREAD_CREDENTIALS = st.secrets["gspread"]
    SHEET_ID = st.secrets["sheet"]["sheet_id"]
    gc = gspread.service_account_from_dict(GSPREAD_CREDENTIALS)
    return gc.open_by_key(SHEET_ID)

# A função de carga de dados
@st.cache_data(ttl=3600)
def load_data(sheet_name: str):
    sheet = connect_to_gsheets()
    try:
        worksheet = sheet.worksheet(sheet_name)
        data = worksheet.get_all_values()
        if not data: return pd.DataFrame()
        columns = data.pop(0)
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados da aba '{sheet_name}': {e}")
        return pd.DataFrame()
    
def adicionar_media_gols(df):
    df['GF'] = pd.to_numeric(df['GF'])
    df['MP'] = pd.to_numeric(df['MP'])
    df['AVG'] = df['GF'] / df['MP']
    df['AVG'] = df['AVG'].round(2)
    return df

# Dentro da função preparar_tabela_geral(df)
def preparar_tabela_geral(df):
    df = adicionar_media_gols(df)
    
    mapa_nomes = {'Squad':'Time', 'MP':'Partidas', 'W':'Vitórias', 'D':'Derrotas', 'L':'Empates', 'GF':'Gols_Marcados', 'GA':'Gols_Sofridos', 'GD':'Saldo_Gols'}
    df = df.rename(columns=mapa_nomes)
    
    # --- SUGESTÃO DE MELHORIA ---
    # A sua lista com a ordem ideal
    ordem_ideal = [
        'Rk', 'Time', 'Partidas', 'Vitórias', 'Derrotas', 'Empates', 'Gols_Marcados', 'Gols_Sofridos', 'Saldo_Gols', 'AVG', 'Pts', 'Pts/MP', 'xG', 'xGA', 'xGD', 'xGD/90', 'Last 5'
    ]
    
    # Filtra a lista para conter apenas as colunas que realmente existem no DataFrame
    colunas_existentes_na_ordem = [col for col in ordem_ideal if col in df.columns]
    
    # Aplica a ordem segura, usando apenas as colunas que foram encontradas
    df = df[colunas_existentes_na_ordem]
    
    return df