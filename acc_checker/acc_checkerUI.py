import streamlit as st
from functions import load_json, generate_crit_layout, generate_crit_mgmt_layout
from text_prep.text_prep_old import return_clean_pdf_text, get_text_chunks, get_nr_of_tokens_and_price
from text_prep.text_prep import FileProcessor
from text_prep.embedder import get_vectorstore
from dotenv import load_dotenv
from llm.retrieval_chain import AnalysisExecutor
import json



# this function is activated by the "Process" button in the sidebar
def display_results(pdf_doc):
    with st.spinner("Processing"):
        if pdf_doc is not None:
            fp = FileProcessor(pdf_doc)
            st.session_state.cleaned_text = fp.preview_text
            st.session_state.text_length = fp.text_length
            st.session_state.text_chunks = fp.text_chunks
            st.session_state.nr_tokens = fp.nr_tokens
            st.session_state.price = fp.price

            # st.session_state.cleaned_text = return_clean_pdf_text(pdf_doc)                      # take uploaded PDF, extract and clean text
            # st.session_state.text_length = len(st.session_state.cleaned_text)                   # obtain text length
            # st.session_state.text_chunks = get_text_chunks(st.session_state.cleaned_text)       # break into text chunks for embedding
            # # get number of tokens and price. Note that due to text overlap we use text_chunks variable (not cleaned_text)
            # st.session_state.nr_tokens, st.session_state.price = get_nr_of_tokens_and_price(st.session_state.text_chunks,
            #                                                                                 0.0001)
        else:
            pass


# this function is activated by the "Embed as vectors" button on the TextInspectTab
def execute_embedding(fact_container):
    with st.spinner("Processing"):
        st.session_state.vector_store = get_vectorstore(st.session_state.text_chunks)
        fact_container.write("Embedding completed!")


# this function is activated by the "Import criteria" button on the AccCheckTab
def import_criteria_set():
    # file_path = os.path.join("..", 'criteria_sets.json')
    file_path = 'criteria_sets_two_levels.json'
    criteria_sets = load_json(file_path)
    st.session_state.criteria_set = criteria_sets['criteria_sets'][0]['criteria']
    return st.session_state.criteria_set



# this function is activated by the "Add subcriterion" button on the CritMgmtTab
def add_subcrit_to_dict(count):
    # st.session_state.crit_content = [count, subcount, st.session_state[txt_key], st.session_state[prpt_key]]
    subcrit_list = st.session_state.criteria_set[count]["subcriteria"]
    empty_subcrit_dict = {"subcriterion_nr": len(subcrit_list)+1, "name":"", "text":"", "prompt":""}
    subcrit_list.append(empty_subcrit_dict)


def run_analysis():
    with st.spinner("Processing"):
        st.session_state.analyzer = AnalysisExecutor(st.session_state.criteria_set, st.session_state.vector_store)
        st.session_state.answer_list = st.session_state.analyzer.answer_list




def acc_check():

    load_dotenv()       # needed for accessing OpenAI APIs

    st.set_page_config(layout="wide")
    st.title("Welcome to AccCheck")

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
        st.session_state.cleaned_text = ""
    if "text_chunks" not in st.session_state:
        st.session_state.text_chunks = None
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if "criteria_set" not in st.session_state:
        st.session_state.criteria_set = None
    if "analyzer" not in st.session_state:
        st.session_state.analyzer = None
    if "answer_list" not in st.session_state:
        st.session_state.answer_list = None


    # markdown test
    # st.markdown('<p class="crit-font">Hello World !!</p>', unsafe_allow_html=True)

    TextInspectTab, AccCheckTab, CritMgmtTab, SessionStateTab, TestTab = st.tabs(["Text Inspection", "AccCheck", "Criteria Manager", "Session State", "Testing"])


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

            # this holds the calculated embedding price
            st.write("Est. embedding cost (USD):")
            price_container = fact_container.container()
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
        '''This section allows you to view:  \n- **Accreditation Criteria**  \n- **related text snippets** retrieved from the documents 
        \n- **suggested conclusions**.'''
        'For each criterion there is an expander. After clicking the "Begin Analysis" button you can click on the expanders to see the results.'
        acc_check_button = st.button("**Begin document analysis**", on_click=run_analysis)
        import_crit_button = st.button("Import criteria", on_click=import_criteria_set)

        if st.session_state.answer_list is None:
            for c in st.session_state.criteria_set:
                    generate_crit_layout(c)
        else:
            for c in st.session_state.answer_list:
                generate_crit_layout(c)


    with CritMgmtTab:
        # create expander for each criterion
        for count, criterion in enumerate(st.session_state.criteria_set):
            generate_crit_mgmt_layout(criterion, count)


                # BUTTON FOR ADDING ADDITIONAL CRITERIA --> NICE-TO-HAVE
                #     # with button_col2:
                # crit_add_button = crit_expander.button("Add subcriterion",
                #                                        on_click=add_subcrit_to_dict,
                #                                        kwargs={"count":count}
                #                                        )


    with TestTab:
        counter_cont = st.container()
        counter_cont.write(st.session_state.counter)
        json_object = json.dumps(st.session_state.criteria_set, indent=4, ensure_ascii=False)
        st.download_button("Download criteria as JSON", json_object, file_name="test.json")
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
                # st.snow()             #awesome!!
                # st.write("hello")


    with SessionStateTab:
        st.write(st.session_state)



if __name__ == '__main__':
    acc_check()