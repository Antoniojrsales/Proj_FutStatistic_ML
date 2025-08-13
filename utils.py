import streamlit as st
import pandas as pd
import gspread

# --- A função de conexão com o Google Sheets ---
@st.cache_resource
def connect_to_gsheets():
    try:
        # Carrega as credenciais de forma segura (usando st.secrets)
        GSPREAD_CREDENTIALS = st.secrets["gspread"]
        SHEET_ID = st.secrets["sheet"]["sheet_id"]
        gc = gspread.service_account_from_dict(GSPREAD_CREDENTIALS)
        return gc.open_by_key(SHEET_ID)
    except Exception as e:
        st.error(f"❌ Erro ao conectar com o Google Sheets: {e}")
        return None

# --- A função de carga de dados brutos (retorna uma lista) ---
@st.cache_data(ttl=3600)
def load_raw_data(sheet_name: str):
    sheet = connect_to_gsheets()
    if sheet is None:
        return []
    try:
        worksheet = sheet.worksheet(sheet_name)
        data = worksheet.get_all_values()
        if not data: return []
        return data
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados da aba '{sheet_name}': {e}")
        return []

# --- A função principal de preparação de DataFrame ---
def prepare_dataframe(raw_data: list, header_row_index: int):
    """
    Cria um DataFrame a partir dos dados brutos e define o cabeçalho.

    Args:
        raw_data (list): Dados brutos da planilha (lista de listas).
        header_row_index (int): O índice da linha que contém o cabeçalho.

    Returns:
        pd.DataFrame: O DataFrame limpo e com o cabeçalho correto.
    """
    # Verifica se os dados são válidos
    if not raw_data or len(raw_data) <= header_row_index:
        return pd.DataFrame()

    # Pega a linha do cabeçalho
    columns = raw_data[header_row_index]
    
    # Pega os dados a partir da linha seguinte ao cabeçalho
    data_rows = raw_data[header_row_index + 1:]
    
    # Converte para DataFrame
    df = pd.DataFrame(data_rows, columns=columns)
    
    # Remove colunas duplicadas que podem ter sido criadas por células vazias
    df = df.loc[:,~df.columns.duplicated()]

    # Remove linhas totalmente vazias que podem ter sido lidas
    df = df.dropna(how='all')
    
    return df    

def add_avg(df):
    df['GF'] = pd.to_numeric(df['GF'])
    df['MP'] = pd.to_numeric(df['MP'])
    df['AVG'] = df['GF'] / df['MP']
    df['AVG'] = df['AVG'].round(2)
    return df

# Dentro da função preparar_tabela_geral(df)
def prepare_overall(df):
    df = add_avg(df)
    
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

# --- Função de Preparação para a Tabela Goalkeeping ---
def prepare_keep(df_input):
    """
    Processa o DataFrame de Goalkeeping, renomeando colunas e ajustando tipos.
    """
    if df_input.empty:
        return df_input
    
    # Mapeamento de nomes de colunas
    mapa_nomes = {
        'Squad': 'Time_keep', '# Pl': 'PI_keep', 'MP': 'Partidas_keep',
        'Starts': 'Starts_keep', 'Min': 'Min_keep', '90s': '90s_keep',
        'GA': 'Gols_Sofridos_keep', 'GA90': 'GA90_keep', 'SoTA': 'SoTA_keep',
        'Saves': 'Saves_keep', 'Save%': 'Save%_keep_Perform', 'W': 'W_keep',
        'D': 'D_keep', 'L': 'L_keep', 'CS': 'CS_keep', 'CS%': 'CS%_keep',
        'PKatt': 'PKatt_keep', 'PKA': 'PKA_keep', 'PKsv': 'PKsv_keep',
        'PKm': 'PKm_keep', 'Save%': 'Save_keep_Penalty'
    }

    # Renomear as colunas
    df_renamed = df_input.rename(columns=mapa_nomes)
    
    # Converter as colunas numéricas (exemplo, adicione mais se necessário)
    colunas_numericas = ['Partidas_keep', 'Starts_keep', 'Min_keep', '90s_keep',
                         'Gols_Sofridos_keep', 'GA90_keep', 'SoTA_keep',
                         'Saves_keep', 'Save%_keep_Perform', 'W_keep',
                         'D_keep', 'L_keep', 'CS_keep', 'CS%_keep',
                         'PKatt_keep', 'PKA_keep', 'PKsv_keep', 'PKm_keep',
                         'Save_keep_Penalty']
    
    for col in colunas_numericas:
        if col in df_renamed.columns:
            df_renamed[col] = pd.to_numeric(df_renamed[col], errors='coerce')
    
    return df_renamed