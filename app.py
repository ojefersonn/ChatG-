from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

dados = PyPDFLoader("Dados/D11246.pdf").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
textos = text_splitter.split_documents(dados)
embedding_engine = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_db = Chroma.from_documents(textos, embedding_engine)

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
n_documentos = 1

def format_docs(documentos):
    return "\n\n".join(documento.page_content for documento in documentos)

llm = ChatOpenAI(openai_api_key = OPENAI_API_KEY, model = "gpt-4o-mini")
prompt = hub.pull("rlm/rag-prompt")

rag = (
    {
        "question": RunnablePassthrough(),
        "context": vector_db.as_retriever(k = n_documentos) 
                    | format_docs
    }
    | prompt
    | llm
    | StrOutputParser()
)

prompt = "Quantos artigos tem o decreto 11246?"
rag.invoke(prompt)

#Streamlit

import streamlit as st
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Chat RAG", layout="centered")
st.title("Chat Gê")

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
        st._rerun()
    except Exception as e:
        st.error(f"Erro ao formatar o prompt: {e}")