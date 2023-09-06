from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv 
from docbot.htmlTemplates import css, bot_template, user_template


# get conversation chain
def get_conversation_chain(vectorstore):
    load_dotenv()
    llm = ChatOpenAI()  # initialize LLM model

    # initialize memory class
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # create conversation chain using LLM and Memory instances - takes into account chat history as well as docs
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


# communicate with user
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)