import streamlit as st
import pandas as pd
from datetime import datetime
import requests # Biblioteca para falar com a internet
import json

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Briefing Arquitetônico", page_icon="🏠", layout="centered")

# --- ⚠️ COLOQUE SEU LINK DO SHEETDB AQUI ⚠️ ---
# Exemplo: "https://sheetdb.io/api/v1/a1b2c3d4e5f6"
URL_PLANILHA = "https://sheetdb.io/api/v1/v5tluj00urary" 

# --- CONTROLE DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'capa'

def ir_para_questionario():
    st.session_state['pagina'] = 'questionario'

# --- FUNÇÃO: ENVIAR PARA O GOOGLE SHEETS ---
def salvar_no_google_sheets(dados):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL_PLANILHA, data=json.dumps(dados), headers=headers)
    return response.status_code == 201

# --- CSS (ROSE GOLD + CAIXAS BRANCAS) ---
st.markdown("""
<style>
    /* Fundo */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/free-photo/pink-watercolor-texture-background_1083-169.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Textos */
    h1, h2, h3, h4, p, label, .stMarkdown { color: #4E342E !important; }
    
    /* Inputs Brancos */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 8px;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
    }
    .stMultiSelect span { color: #000000 !important; }

    /* Capa e Botões */
    .titulo-capa {
        font-family: 'Helvetica', sans-serif;
        color: #880E4F; font-size: 4em; font-weight: 800; text-align: center;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.6);
    }
    .assinatura {
        font-family: 'Brush Script MT', cursive;
        font-size: 3em; color: #AD1457; text-align: center; margin-top: 10px;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 3rem; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(136, 14, 79, 0.15);
    }
    div.stButton > button {
        background-color: #D81B60; color: white; border: none;
        padding: 15px 40px; border-radius: 30px; font-size: 18px; font-weight: bold;
        display: block; margin: 0 auto;
    }
    div.stButton > button:hover { background-color: #880E4F; transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# --- APP ---

if st.session_state['pagina'] == 'capa':
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#AD1457; letter-spacing:2px;'>PROGRAMA DE NECESSIDADES</div>", unsafe_allow_html=True)
    st.markdown("<div class='titulo-capa'>Briefing<br>Arquitetônico</div>", unsafe_allow_html=True)
    st.markdown("<div class='assinatura'>Desirée Braga</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.button("INICIAR PROJETO  💖", on_click=ir_para_questionario)

else:
    st.markdown("<h1 style='text-align: center; color: #880E4F;'>Questionário de Perfil</h1>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form("briefing_online"):
        st.markdown("### 1. Dados Básicos")
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo")
            idade = st.number_input("Idade", min_value=18, step=1)
        with col2:
            profissao = st.text_input("Profissão")
        
        usuarios = st.text_area("Quem utilizará o espaço?")
        
        st.markdown("### 2. Preferências")
        estilos = st.multiselect("Estilos preferidos:", ["Moderno", "Clássico", "Industrial", "Rústico", "Minimalista"])
        
        st.markdown("### 3. Orçamento e Prazos")
        investimento = st.number_input("Investimento (R$)", min_value=0.0)
        prazo = st.date_input("Prazo Limite").strftime("%d/%m/%Y")
        obs = st.text_area("Observações Finais")

        st.markdown("<br>", unsafe_allow_html=True)
        enviar = st.form_submit_button("FINALIZAR E ATUALIZAR PLANILHA ✨")

    if enviar:
        if URL_PLANILHA == "COLE_SEU_LINK_AQUI":
            st.error("⚠️ ERRO: Você esqueceu de colocar o link do SheetDB no código!")
        else:
            # Prepara os dados (Os nomes aqui devem ser IGUAIS aos da Linha 1 do Excel)
            novo_dado = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Nome": nome,
                "Idade": str(idade),
                "Profissao": profissao,
                "Usuarios": usuarios,
                "Estilos": ", ".join(estilos),
                "Investimento": str(investimento),
                "Prazo": prazo,
                "Obs": obs
            }
            
            with st.spinner("Atualizando a planilha no Google..."):
                sucesso = salvar_no_google_sheets(novo_dado)
            
            if sucesso:
                st.success(f"Sucesso! Os dados de {nome} foram salvos na nuvem.")
                st.balloons()
            else:
                st.error("Houve um erro ao conectar com a planilha. Verifique o link.")
