import streamlit as st
import hashlib
from supabase import create_client, Client

# ⚙️ Configuração da página e CSS (mantido como está)
st.set_page_config(
    page_title="Login | FutStatistic", 
    page_icon="🔏", 
    layout="centered")
st.sidebar.markdown('Desenvolvido por [AntonioJrSales](https://antoniojrsales.github.io/meu_portfolio/)')
# ... seu CSS aqui ...

# --- Conexão com o Supabase ---
try:
    url: str = st.secrets["supabase"]["url"]
    key: str = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Erro ao conectar com o Supabase. Verifique suas configurações em secrets.toml.")
    st.stop()

# --- Funções de Banco de Dados ---

def get_user(username: str):
    """Busca os dados de um usuário (hash da senha e papel/role)."""
    response = supabase.table('users').select('hash_password, role').eq('username', username).execute()
    if response.data:
        return response.data[0]
    return None

def add_user(username: str, hash_password: str):
    """Adiciona um novo usuário ao banco de dados. O papel será 'user' por padrão (definido no Supabase)."""
    response = supabase.table('users').insert({"username": username, "hash_password": hash_password}).execute()
    return response

# --- Inicialização do Session State ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['role'] = None

# --- Lógica Principal ---

# Se o usuário NÃO estiver logado, mostra a tela de login
if not st.session_state['logged_in']:
    st.header("🔐 Login - FutStatistic")
    with st.form("login_form"):
        username = st.text_input("👤 Usuário").strip()
        password = st.text_input("🔒 Senha", type="password").strip()
        submit = st.form_submit_button("Entrar")

        if submit:
            user_data = get_user(username)
            if user_data and hashlib.sha256(password.encode()).hexdigest() == user_data['hash_password']:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['role'] = user_data['role'] # Armazena o papel na sessão
                st.rerun()
            else:
                st.error("❌ Usuário ou senha inválidos.")
else:
    # --- ÁREA LOGADA ---
    st.sidebar.success(f"Logado como: {st.session_state['username']}")
    st.sidebar.info(f"Permissão: {st.session_state['role'].upper()}")

    st.title("⚽ Painel FutStatistic")
    st.markdown("### Bem-vindo(a) à área principal de estatísticas!")
    #
    # AQUI VOCÊ COLOCARÁ SEUS GRÁFICOS E TABELAS
    #
    st.markdown("---")


    # --- ÁREA EXCLUSIVA DO ADMINISTRADOR ---
    if st.session_state['role'] == 'admin':
        st.subheader("🔑 Painel do Administrador")
        with st.expander("Cadastrar Novo Usuário"):
            with st.form("signup_form", clear_on_submit=True):
                st.markdown("Preencha os dados do novo usuário:")
                new_username = st.text_input("👤 Novo Usuário").strip()
                new_password = st.text_input("🔒 Senha para o novo usuário", type="password").strip()
                signup_submit = st.form_submit_button("Cadastrar Usuário")

                if signup_submit:
                    if not new_username or not new_password:
                        st.warning("⚠️ Por favor, preencha todos os campos.")
                    elif get_user_data(new_username):
                        st.error(f"❌ O usuário '{new_username}' já existe.")
                    else:
                        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                        add_user(new_username, hashed_password)
                        st.success(f"🎉 Usuário '{new_username}' cadastrado com sucesso!")

    # Botão de Sair
    if st.sidebar.button("Sair"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['role'] = None
        st.rerun()