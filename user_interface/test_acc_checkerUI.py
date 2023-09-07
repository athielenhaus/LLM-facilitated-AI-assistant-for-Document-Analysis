from acc_checkerUI import get_conversation_chain
from text_prep.embedder import Embedder
from langchain.document_loaders import PDFPlumberLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import streamlit as st


def create_sample_vectorstore():
    loader = PDFPlumberLoader('C:/Users/Arne/Downloads/Prüfungsordnungen/KIT_Ba_Informatik.pdf')
    data = loader.load()
    full_text = ''
    for doc in data:
        full_text += doc.page_content
    # print(full_text)
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "(?<=\. )", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    text_chunks = text_splitter.create_documents([full_text])
    # print(text_chunks[2])
    vs = Embedder(text_chunks=text_chunks).vector_store
    vs.save_local('sample_vectorstore')
    print('vector store created!')


def test_get_conversation_chain():
    load_dotenv()
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("sample_vectorstore", embeddings)
    conversation = get_conversation_chain(vectorstore)
    # print(conversation)
    assert conversation is not None

# test_get_conversation_chain()


def test_execute_embedding():
    load_dotenv()

    # initialize
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.conversation = None

    # with st.spinner("Processing"):
    embeddings = OpenAIEmbeddings()
    st.session_state.vector_store = FAISS.load_local("sample_vectorstore", embeddings)
    print(st.session_state.vector_store)

    # create conversation chain
    print(st.session_state.conversation)
    st.session_state.conversation = get_conversation_chain(st.session_state.vector_store)
    print(st.session_state.conversation)
    st.write("Embedding completed!")