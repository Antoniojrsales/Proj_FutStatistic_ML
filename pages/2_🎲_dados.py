import streamlit as st
import pandas as pd
from utils import load_raw_data, prepare_dataframe, prepare_overall, prepare_keep

# --- Configuração da Página e Verificação de Login ---
st.set_page_config(
    page_title="Visualização dos Dados | FutStatistic⚽",
    page_icon="🎲",
    layout='wide'
)

if not st.session_state.get('logged_in'):
    st.error("🔒 Acesso negado. Por favor, faça o login primeiro.")
    st.page_link("1__loginFut.py", label="**Ir para a página de Login**", icon="🏠")
    st.stop()
# ---------------------------------------------------------

st.title("📊 Painel de Análises")
st.markdown("Navegue pelas abas para visualizar diferentes recortes de dados.")

# --- Criação das Abas ---
aba1, aba2, aba3, aba4, aba5 = st.tabs(['Jogos do Dia', 'Partidas Realizadas', 'Tabela Overall', 'Tabela Goalkeeping', 'Tabela Shooting'])

# --- Lógica da Aba 1: Jogos do Dia ---
with aba1:
    st.subheader(" Partidas do Dia")
    
    # Suponha que sua aba se chame 'Jogos_dia'
    name_aba = "Jogos_dia" 
    
    # 1. Carrega os dados brutos (lista de listas)
    raw_data = load_raw_data(name_aba)
    
    # 2. Prepara o DataFrame a partir dos dados brutos
    #    'header_row_index=0' porque o cabeçalho está na primeira linha
    df_jogos = prepare_dataframe(raw_data, header_row_index=0)
    
    # 3. Verifica se o DataFrame não está vazio
    if not df_jogos.empty:
        st.dataframe(df_jogos, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para 'Jogos do Dia'.")

# --- Lógica da Aba 2: Tabela Partidas Realizadas ---
with aba2:
    st.subheader("🏆 Tabela Partidas Realizadas - Campeonato")
    name_aba = st.secrets["sheet"]["aba_scoresfixtures"]

    raw_data = load_raw_data(name_aba)
    df_scoresfixtures = prepare_dataframe(raw_data, header_row_index=0)
    
    if not df_scoresfixtures.empty:
        st.dataframe(df_scoresfixtures, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para a 'Tabela ScoresFixtures'.")

# --- Lógica da Aba 3: Tabela Geral ---
with aba3:
    st.subheader("🏆 Tabela Geral - Campeonato")
    name_aba = st.secrets["sheet"]["aba_tabelaGeral"]
    raw_data = load_raw_data(name_aba)
    df_bruto = prepare_dataframe(raw_data, header_row_index=0)
    df_overall = prepare_overall(df_bruto)
    
    if not df_overall.empty:
        st.dataframe(df_overall, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para a 'Tabela Geral'.")

# --- Lógica da Aba 4: Tabela GoalKeeping ---
with aba4:
    st.subheader(" Tabela GoalKeeping - Campeonato")
    name_aba = st.secrets["sheet"]["aba_goalkeeping"]
    raw_data = load_raw_data(name_aba)
    df_bruto = prepare_dataframe(raw_data, header_row_index=1)
    df_goalkeeping = prepare_keep(df_bruto)
    
    if not df_goalkeeping.empty:
        st.dataframe(df_goalkeeping, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para a 'Tabela GoalKeeping'.")

# --- Lógica da Aba 5: Tabela Shooting ---
with aba5:
    st.subheader(" Tabela Shooting - Campeonato")
    name_aba = st.secrets["sheet"]["aba_shooting"]
    raw_data = load_raw_data(name_aba)
    df_shooting = prepare_dataframe(raw_data, header_row_index=1)
    
    if not df_shooting.empty:
        st.dataframe(df_shooting, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para a 'Tabela Shooting'.")