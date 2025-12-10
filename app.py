import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Briefing Arquitetônico", page_icon="🏠", layout="centered")

# --- CONTROLE DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'capa'

def ir_para_questionario():
    st.session_state['pagina'] = 'questionario'

# --- CSS: ESTILO ROSE GOLD + CAIXAS BRANCAS (SOLICITADO) ---
st.markdown("""
<style>
    /* 1. Fundo Aquarela Rose */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/free-photo/pink-watercolor-texture-background_1083-169.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* 2. Textos em Marrom/Preto */
    h1, h2, h3, p, label, .stMarkdown {
        color: #4E342E !important;
    }

    /* 3. CAIXAS DE RESPOSTA BRANCAS COM BORDA PRETA */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 8px;
    }
    
    /* Caixas de Seleção (Dropdowns) */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
    }
    
    /* Tags dentro do multiselect */
    .stMultiSelect span {
        color: #000000 !important;
    }

    /* 4. Estilo da Capa */
    .titulo-capa {
        font-family: 'Helvetica', sans-serif;
        color: #880E4F;
        font-size: 4em;
        font-weight: 800;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.6);
    }
    .assinatura {
        font-family: 'Brush Script MT', cursive;
        font-size: 3em;
        color: #AD1457;
        text-align: center;
        margin-top: 10px;
    }

    /* 5. Container Branco */
    .block-container {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(136, 14, 79, 0.15);
    }

    /* 6. Botões */
    div.stButton > button {
        background-color: #D81B60;
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 30px;
        font-size: 18px;
        font-weight: bold;
        display: block;
        margin: 0 auto;
    }
    div.stButton > button:hover {
        background-color: #880E4F;
        transform: scale(1.05);
    }
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

    with st.form("briefing_completo"):
        
        st.markdown("### 1. Informações Gerais")
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo")
            idade = st.number_input("Idade", min_value=18, step=1)
        with col2:
            profissao = st.text_input("Profissão")
        
        usuarios = st.text_area("Quem utilizará o espaço? (Idades, pets, etc)")

        st.markdown("### 2. Estilo e Preferências")
        estilos = st.multiselect("Estilo que mais se identifica:", ["Moderno", "Contemporâneo", "Rústico", "Industrial", "Clássico", "Minimalista"])
        rotina = st.text_area("Como descreveria sua rotina em casa?")
        
        st.markdown("### 3. Orçamento e Prazos")
        investimento = st.number_input("Investimento Estimado (R$)", min_value=0.0)
        prazo = st.date_input("Prazo Limite")
        
        st.markdown("### Observações Finais")
        obs = st.text_area("Algo mais que precisamos saber?")

        st.markdown("<br>", unsafe_allow_html=True)
        enviar = st.form_submit_button("FINALIZAR E SALVAR ✨")

    if enviar:
        # Criação dos Dados
        dados = {
            "Data": [datetime.now().strftime("%d/%m/%Y")],
            "Nome": [nome],
            "Idade": [idade],
            "Profissão": [profissao],
            "Usuários": [usuarios],
            "Estilos": [", ".join(estilos)],
            "Rotina": [rotina],
            "Investimento": [investimento],
            "Prazo": [prazo],
            "Observações": [obs]
        }
        
        df = pd.DataFrame(dados)
        arquivo_excel = "Briefing_Respostas.xlsx"
        
        # Salvar (Append se já existir, Criar novo se não)
        if os.path.exists(arquivo_excel):
            # Carrega existente e adiciona novo
            with pd.ExcelWriter(arquivo_excel, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                # Tenta ler para saber onde parar, ou apenas concatena
                try:
                    df_existente = pd.read_excel(arquivo_excel)
                    df_final = pd.concat([df_existente, df], ignore_index=True)
                    df_final.to_excel(arquivo_excel, index=False)
                except:
                    df.to_excel(arquivo_excel, index=False)
        else:
            df.to_excel(arquivo_excel, index=False)
            
        st.success(f"Obrigado, {nome}! Suas respostas foram salvas.")
        st.balloons()
        
        # --- O PULO DO GATO ---
        # Botão para o cliente baixar o arquivo e te mandar
        with open(arquivo_excel, "rb") as file:
            btn = st.download_button(
                label="📥 CLIQUE AQUI PARA BAIXAR O ARQUIVO (Envie este arquivo para o Arquiteto)",
                data=file,
                file_name=f"Briefing_{nome}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )