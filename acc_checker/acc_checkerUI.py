import streamlit as st
from functions import load_json, create_sub_crit_layout
from vector_prep.text_prep import return_clean_pdf_text, get_text_chunks, get_nr_of_tokens_and_price
from vector_prep.embedder import get_vectorstore
from dotenv import load_dotenv

def acc_check():

    load_dotenv()       # needed for accessing OpenAI APIs

    st.set_page_config(layout="wide")
    st.title("Welcome to AccChecker")

    if "text_length" not in st.session_state:
        st.session_state.text_length = None
    if "nr_tokens" not in st.session_state:
        st.session_state.nr_tokens = None
    if "price" not in st.session_state:
        st.session_state.price = None

    # markdown test
    # st.markdown('<p class="crit-font">Hello World !!</p>', unsafe_allow_html=True)

    TextInspectTab, AccCheckTab, CritMgmtTab = st.tabs(["Text Inspection", "AccCheck", "Criteria Manager"])

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

        # create container to hold text analysis info
        fact_container = insp_col2.container()
        fact_container.write("Text length / number of characters:")
        text_len_cont = fact_container.container()                          # this will hold the text length
        fact_container.write("Number of tokens:")
        token_nr_container = fact_container.container()                     # this will hold the number of tokens
        fact_container.write("Est. embedding cost (USD):")
        price_container = fact_container.container()                        # this will hold the calculated embedding price
        embed_button = fact_container.button("**Embed text as vectors**")   # this button will launch embedding


    st.sidebar.header('PDF Import')
    with st.sidebar:
        # st.subheader("Your documents")
        pdf_doc = st.file_uploader(
            "Upload a PDF here and click on 'Process'", accept_multiple_files=False)
        if st.button("Process"):
            with st.spinner("Processing"):

                # take uploaded PDF, extract and clean text
                cleaned_text = return_clean_pdf_text(pdf_doc)

                # obtain text length
                st.session_state.text_length = len(cleaned_text)

                # break into text chunks for embedding
                text_chunks = get_text_chunks(cleaned_text)

                # get number of tokens and price. Note that due to text overlap we use text_chunks variable (not cleaned_text)
                st.session_state.nr_tokens, st.session_state.price = get_nr_of_tokens_and_price(text_chunks, 0.0001)

                # communicate this to user
                text_len_cont.write(st.session_state.text_length)
                token_nr_container.write(st.session_state.nr_tokens)
                price_container.write(st.session_state.price)
                clean_text_exp.text_area("", cleaned_text, height=500)
                if embed_button:

                    # get vector store
                    with fact_container.spinner("Processing"):
                        vectorstore = get_vectorstore(text_chunks)
                        fact_container.write("Embedding completed!")






    with AccCheckTab:
        for c in criteria:
            crit_cont = st.expander(f"**{c['name']}**")
            for s in c["subcriteria"]:
                create_sub_crit_layout(crit_cont, s)



if __name__ == '__main__':
    acc_check()