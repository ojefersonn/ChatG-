import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# =====================
# 🔐 Carrega variáveis de ambiente
# =====================
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# =====================
# 💬 Interface Streamlit
# =====================
st.title("💬 Chatbot com RAG - Decreto 11.246/2022")
st.write("Chatbot com busca contextual usando PDF do Decreto 11.246/2022")

if not OPENAI_API_KEY:
    st.info("Adicione sua chave da OpenAI no arquivo `.env` como OPENAI_API_KEY=...", icon="🗝️")
    st.stop()

# =====================
# 📄 Carregamento e segmentação do PDF
# =====================
dados = PyPDFLoader("Dados/D11246.pdf").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
textos = text_splitter.split_documents(dados)

# =====================
# 🧠 Embeddings + ChromaDB com persistência
# =====================
embedding_engine = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_db_path = "chroma_db"

if not os.path.exists(vector_db_path):
    vector_db = Chroma.from_documents(textos, embedding_engine, persist_directory=vector_db_path)
    vector_db.persist()
else:
    vector_db = Chroma(persist_directory=vector_db_path, embedding_function=embedding_engine)

# =====================
# 🤖 LLM + Prompt personalizado
# =====================
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4")

prompt_template = PromptTemplate(
    input_variables=["context", "question", "history"],
    template="""
Você é um assistente especializado no Decreto 11.246/2022.
Baseie sua resposta apenas nos trechos abaixo. Se não souber, diga que não sabe.

{context}

Histórico da conversa:
{history}

Pergunta: {question}
Resposta:
"""
)

# =====================
# 💬 Sessão e Histórico
# =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================
# 📚 Funções auxiliares
# =====================
def format_docs(documentos):
    return "\n\n---\n\n".join(
        f"Trecho {i+1} (página {doc.metadata['page']+1}):\n{doc.page_content}" 
        for i, doc in enumerate(documentos)
    )

def gerar_resposta(pergunta):
    documentos = vector_db.as_retriever(k=3).invoke(pergunta)
    contexto = format_docs(documentos)
    historico = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages if m['role'] in ['user', 'assistant']])
    prompt_formatado = prompt_template.format(context=contexto, question=pergunta, history=historico)
    return llm.invoke(prompt_formatado).content

# =====================
# 🎤 Entrada do usuário + resposta do assistente
# =====================
if pergunta := st.chat_input("Qual sua dúvida sobre o decreto?"):
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    try:
        with st.chat_message("assistant"):
            resposta = gerar_resposta(pergunta)
            st.markdown(str(resposta))
        st.session_state.messages.append({"role": "assistant", "content": resposta})
    except Exception as e:
        st.error(f"Erro ao gerar resposta: {e}")
