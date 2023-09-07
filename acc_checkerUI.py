import streamlit as st
from acc_checker.text_prep.text_prep import FileProcessor
from acc_checker.text_prep.embedder import Embedder
from dotenv import load_dotenv
# from llm.analysis_executor import AnalysisExecutor
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from acc_checker.docbot.htmlTemplates import css, bot_template, user_template
from user_interface.functionsUI import load_json, generate_crit_layout, generate_crit_mgmt_layout

# from docbot.docbot import handle_userinput, get_conversation_chain
# from text_prep.text_prep_old import return_clean_pdf_text, get_text_chunks, get_nr_of_tokens_and_price



# this function is activated by the "Process" button in the sidebar
def display_results(pdf_doc):
    with st.spinner("Processing"):
        if pdf_doc is not None:
            fp = FileProcessor(pdf_doc)
            st.session_state.text_length = fp.text_length
            st.session_state.cleaned_text = fp.preview_text
            st.session_state.text_chunks = fp.text_chunks
            st.session_state.nr_tokens = fp.nr_tokens
            st.session_state.price = fp.price
        else:
            pass


# get conversation chain
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(temperature= 0.0)  # initialize LLM model

    # initialize memory class
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # create conversation chain using LLM and Memory instances - takes into account chat history as well as docs
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain
    


# this function is activated by the "Embed as vectors" button on the TextInspectTab
def execute_embedding(fact_container):
    with st.spinner("Processing"):
        st.session_state.vector_store = Embedder(st.session_state.text_chunks).vector_store
        fact_container.write("Embedding completed!")



# communicate with user
def handle_userinput(user_question, bot_container):

    st.session_state.conversation = get_conversation_chain(st.session_state.vector_store)
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            bot_container.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            bot_container.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            


def main():

    load_dotenv()       # needed for accessing OpenAI APIs

    st.set_page_config(layout="wide")
    st.title("Welcome to DocCheck - Your Document Analysis Assistant")

    
    st.sidebar.header('PDF Import')
    with st.sidebar:
        # st.subheader("Your documents")
        pdf_doc = st.file_uploader(
            "Upload a PDF here and click on 'Process'", accept_multiple_files=False)
        process_txt_button = st.button("Process", on_click=display_results, args=(pdf_doc,))

    TextInspectTab, AccBotTab, SessionStateTab = st.tabs(["Text Inspection", "DocBot", "Session State"])
    
    # for TextInspect Tab 
    if "crit_content" not in st.session_state:
        st.session_state.crit_content = None
    if "text_length" not in st.session_state:
        st.session_state.text_length = 0
    if "nr_tokens" not in st.session_state:
        st.session_state.nr_tokens = 0
    if "price" not in st.session_state:
        st.session_state.price = 0
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "cleaned_text" not in st.session_state:
        st.session_state.cleaned_text = 'na'
    if "text_chunks" not in st.session_state:
        st.session_state.text_chunks = None
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    # for AccBot tab
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # for AccCheck Tab 
    # if "criteria_set" not in st.session_state:
    #     st.session_state.criteria_set = None
    # if "analyzer" not in st.session_state:
    #     st.session_state.analyzer = None
    # if "answer_list" not in st.session_state:
    #     st.session_state.answer_list = None
    # if "analysis_cost" not in st.session_state:
    #     st.session_state.analysis_cost = 0


    with TextInspectTab:
        st.header('Text Inspection')

        '''
        This assistant can help you analyze your documents.
        
        __INSTRUCTIONS:__
        
        1) please use the __sidebar on the left__ to upload a PDF file. The imported and formatted text will appear below. 
        Take a look to make sure that the formatted text looks alright. The number of characters and the estimated cost of 
        embedding them will appear on the right hand side of the imported text.

        2) If you are satisfied and the estimated embedding cost is below __0.003__ (may be higher in future app versions), you can 
        click on the button "Embed text as vectors". Once you see the message below the button that the embedding has been completed 
        successfully, proceed to the next tab and ask the bot some questions about your document.
        '''

        # create multiple columns
        insp_col1, insp_col2 = st.columns([4, 2])
        clean_text_exp = insp_col1.expander('Cleaned Text', expanded=True)
        # clean_text_exp.write("Cleaned text will appear below. Please note that the cleaning process removes blank lines")

        clean_text_exp.text_area("", st.session_state.cleaned_text, height=500, key="clean_text_area")

        # create container in second column to hold text analysis info
        fact_container = insp_col2.container()

        with fact_container:
            # this holds the text length
            st.write(f"Text length / number of characters:")
            text_len_cont = fact_container.container()
            text_len_cont.write(st.session_state.text_length)

            # this holds the number of tokens
            st.write("Number of tokens:")
            token_nr_container = fact_container.container()
            token_nr_container.write(st.session_state.nr_tokens)

            # this holds the calculated embedding price
            st.write("Est. embedding cost (USD):")
            price_container = fact_container.container()
            price_container.write(st.session_state.price)

            # create button to launch embedding - do NOT pass session_state arguments to function --> automatically triggers button whenever session state changes
            if 0 < st.session_state.price < 0.003:
                embed_button = fact_container.button("**Embed text as vectors**", on_click=execute_embedding, args=(fact_container,))


    with AccBotTab:
        st.write(css, unsafe_allow_html=True)  # implements imported CSS

        st.header("Document ChatBot")
        '''This tab allows you to ask questions about the uploaded document and converse with the Document ChatBot.  
        In the first step, we search the document for relevant text snippets, then we submit those snippets to ChatGPT along with your question.'''
        
        bot_container = st.container()
        with bot_container:
            user_question = st.text_input("Ask your documents a question:")
            if user_question:
                handle_userinput(user_question, bot_container)


    # with SessionStateTab:
    #     st.write(st.session_state)





if __name__ == '__main__':
    main()