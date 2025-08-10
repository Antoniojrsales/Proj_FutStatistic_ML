import streamlit as st
import pandas as pd
from utils import load_data, preparar_tabela_geral

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
    st.subheader("🏟️ Partidas do Dia")
    nome_da_aba = st.secrets["sheet"]["aba_jogos"]
    df_jogos = load_data(nome_da_aba)

    if not df_jogos.empty:
        st.dataframe(df_jogos, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para 'Jogos do Dia'.")

# --- Lógica da Aba 2: Tabela Partidas Realizadas ---
with aba2:
    st.subheader("🏆 Tabela Partidas Realizadas - Campeonato")
    nome_da_aba = st.secrets["sheet"]["aba_scoresfixtures"]
    df_scoresfixtures = load_data(nome_da_aba)
    
    if not df_scoresfixtures.empty:
        st.dataframe(df_scoresfixtures, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para a 'Tabela ScoresFixtures'.")

# --- Lógica da Aba 3: Tabela Geral ---
with aba3:
    st.subheader("🏆 Tabela Geral - Campeonato")
    nome_da_aba = st.secrets["sheet"]["aba_tabelaGeral"]
    df_brutos = load_data(nome_da_aba)
    df_geral = preparar_tabela_geral(df_brutos)
    
    if not df_geral.empty:
        st.dataframe(df_geral, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para a 'Tabela Geral'.")

# --- Lógica da Aba 4: Tabela GoalKeeping ---
with aba4:
    st.subheader(" Tabela GoalKeeping - Campeonato")
    nome_da_aba = st.secrets["sheet"]["aba_goalkeeping"]
    df_goalkeeping = load_data(nome_da_aba)
    
    if not df_goalkeeping.empty:
        st.dataframe(df_goalkeeping, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para a 'Tabela GoalKeeping'.")

# --- Lógica da Aba 5: Tabela Shooting ---
with aba5:
    st.subheader(" Tabela Shooting - Campeonato")
    nome_da_aba = st.secrets["sheet"]["aba_shooting"]
    df_shooting = load_data(nome_da_aba)
    
    if not df_shooting.empty:
        st.dataframe(df_shooting, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para a 'Tabela Shooting'.")