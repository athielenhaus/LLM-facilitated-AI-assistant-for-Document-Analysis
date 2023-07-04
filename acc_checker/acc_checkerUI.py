import streamlit as st
from functions import load_json, create_sub_crit_layout
from vector_prep.text_prep import return_clean_pdf_text, get_text_chunks, get_nr_of_tokens_and_price
from vector_prep.embedder import get_vectorstore
from dotenv import load_dotenv



def display_results(pdf_doc):
    with st.spinner("Processing"):
        if pdf_doc != None:
            st.session_state.cleaned_text = return_clean_pdf_text(pdf_doc)                      # take uploaded PDF, extract and clean text
            st.session_state.text_length = len(st.session_state.cleaned_text)                   # obtain text length
            st.session_state.text_chunks = get_text_chunks(st.session_state.cleaned_text)       # break into text chunks for embedding
            # get number of tokens and price. Note that due to text overlap we use text_chunks variable (not cleaned_text)
            st.session_state.nr_tokens, st.session_state.price = get_nr_of_tokens_and_price(st.session_state.text_chunks,
                                                                                            0.0001)
        else:
            pass

def execute_embedding(fact_container):
    with st.spinner("Processing"):
        st.session_state.vector_store = get_vectorstore(st.session_state.text_chunks)
        fact_container.write("Embedding completed!")



def acc_check():

    load_dotenv()       # needed for accessing OpenAI APIs

    st.set_page_config(layout="wide")
    st.title("Welcome to AccChecker")

    if "text_length" not in st.session_state:
        st.session_state.text_length = 0
    if "nr_tokens" not in st.session_state:
        st.session_state.nr_tokens = 0
    if "price" not in st.session_state:
        st.session_state.price = 0
    if "vector_store" not in st.session_state:
        st.vector_store = None
    if "cleaned_text" not in st.session_state:
        st.session_state.cleaned_text = ""
    if "text_chunks" not in st.session_state:
        st.session_state.text_chunks = None
    if "counter" not in st.session_state:
        st.session_state.counter = 0


    # markdown test
    # st.markdown('<p class="crit-font">Hello World !!</p>', unsafe_allow_html=True)

    TextInspectTab, AccCheckTab, CritMgmtTab, SessionStateTab = st.tabs(["Text Inspection", "AccCheck", "Criteria Manager", "Session State"])

    # file_path = os.path.join("..", 'criteria_sets.json')
    file_path = 'criteria_sets.json'
    criteria_sets = load_json(file_path)
    criteria = criteria_sets['criteria_sets'][0]['criteria']


    with TextInspectTab:
        st.header('Text Inspection')

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

            # this holds the price
            st.write("Est. embedding cost (USD):")
            price_container = fact_container.container()                        # this will hold the calculated embedding price
            price_container.write(st.session_state.price)

            # create button to launch embedding - do NOT pass session_state arguments to function --> automatically triggers button whenever session state changes
            embed_button = fact_container.button("**Embed text as vectors**", on_click=execute_embedding, args=(fact_container,))


    st.sidebar.header('PDF Import')
    with st.sidebar:
        # st.subheader("Your documents")
        pdf_doc = st.file_uploader(
            "Upload a PDF here and click on 'Process'", accept_multiple_files=False)
        process_txt_button = st.button("Process", on_click=display_results, args=(pdf_doc,))




    with AccCheckTab:

        st.header("Automated document analysis")
        '''This section allows you to view:  \n- **Accreditation Criteria**  \n- **relevant text snippets** retrieved from the documents 
        \n- **suggested conclusions**.'''
        'For each criterion there is an expander. After clicking the "Begin Analysis" button you can click on the expanders to see the results.'
        acc_check_button = st.button("**Begin document analysis**", on_click=run_analysis)
        for c in criteria:
            crit_cont = st.expander(f"**{c['name']}**")
            for s in c["subcriteria"]:
                create_sub_crit_layout(crit_cont, s)

    with CritMgmtTab:
        counter_cont = st.container()
        counter_cont.write(st.session_state.counter)
        add_button = st.button("Add one")

        if add_button:
            with st.spinner("Processing"):
                st.session_state.counter += 1
                # counter_cont.write("point added!")
                # st.balloons()
                # st.info("Useful info")
                # st.warning('This is a warning', icon="⚠️")
                # st.success('This is a success message!', icon="✅")
                # e = RuntimeError('This is an exception of type RuntimeError')
                # st.exception(e)
                # st.snow()
                # st.write("hello")

    with SessionStateTab:
        st.write(st.session_state)



if __name__ == '__main__':
    acc_check()