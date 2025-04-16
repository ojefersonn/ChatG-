import streamlit as st
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Chat RAG", layout="centered")
st.title("Chat RAG")

# Define um prompt fixo
prompt = PromptTemplate.from_template(
    "Responda com base no contexto:\n\n{context}\n\nPergunta: {question}"
)

# Inicializa sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe histórico
for troca in st.session_state.mensagens:
    st.markdown(f"**Você:** {troca['pergunta']}")
    st.markdown(f"**Prompt:** {troca['resposta']}")
    st.markdown("---")

# Input com Enter e botão
pergunta = st.text_input("Digite sua pergunta:", placeholder="Escreva aqui e pressione Enter ou clique em Enviar")

if st.button("Enviar") or (pergunta and pergunta != st.session_state.get("ultima_pergunta")):
    try:
        resposta = prompt.format(context="exemplo de contexto", question=pergunta)
        st.session_state.mensagens.append({"pergunta": pergunta, "resposta": resposta})
        st.session_state.ultima_pergunta = pergunta
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Erro ao formatar o prompt: {e}")