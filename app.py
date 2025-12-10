import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Briefing Arquitetônico", page_icon="🏠", layout="centered")

# --- CONTROLE DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'capa'

def ir_para_questionario():
    st.session_state['pagina'] = 'questionario'

# --- FUNÇÃO PARA GERAR EXCEL NA MEMÓRIA (ESSENCIAL PARA ONLINE) ---
def gerar_excel_bytes(df):
    output = io.BytesIO()
    # Usa o motor 'xlsxwriter' que é compatível com o Streamlit Cloud
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Briefing')
        # Ajuste automático da largura das colunas (opcional, para ficar bonito)
        worksheet = writer.sheets['Briefing']
        for i, col in enumerate(df.columns):
            worksheet.set_column(i, i, 20)
    return output.getvalue()

# --- CSS: ESTILO ROSE GOLD + CAIXAS BRANCAS ---
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
    h1, h2, h3, h4, p, label, .stMarkdown, .stRadio label {
        color: #4E342E !important;
    }

    /* 3. CAIXAS DE RESPOSTA BRANCAS COM BORDA PRETA */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 8px;
    }
    
    /* Caixas de Seleção e Multiselect */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
    }
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

# --- INÍCIO DO APP ---

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
        # O botão aqui serve apenas para confirmar o preenchimento
        enviar = st.form_submit_button("GERAR ARQUIVO EXCEL ✨")

    if enviar:
        if not nome:
            st.warning("Por favor, preencha pelo menos o seu Nome.")
        else:
            # 1. Cria o DataFrame com os dados
            dados = {
                "Data Preenchimento": [datetime.now().strftime("%d/%m/%Y %H:%M")],
                "Nome Cliente": [nome],
                "Idade": [idade],
                "Profissão": [profissao],
                "Usuários": [usuarios],
                "Estilos Preferidos": [", ".join(estilos)],
                "Rotina": [rotina],
                "Investimento R$": [investimento],
                "Prazo Limite": [prazo],
                "Observações": [obs]
            }
            df = pd.DataFrame(dados)
            
            # 2. Converte para Excel na memória (Bytes)
            excel_data = gerar_excel_bytes(df)
            
            st.success("Briefing gerado com sucesso!")
            st.markdown("### 👇 Clique abaixo para baixar e enviar para a Arquiteta:")
            
            # 3. Botão de Download (Onde a mágica acontece)
            st.download_button(
                label="📥 BAIXAR PLANILHA EXCEL",
                data=excel_data,
                file_name=f"Briefing_{nome.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.balloons()
