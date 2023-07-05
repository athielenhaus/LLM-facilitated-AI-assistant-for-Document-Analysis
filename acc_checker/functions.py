import json
import streamlit as st

def load_json(file_path):
    file = open(file_path, encoding="utf-8")   # specifying encoding necessary to display German characters
    criteria_sets = json.load(file)
    return criteria_sets

def create_sub_crit_layout(crit_container, subcriterion):
    crit_container.write(subcriterion["text"])
    crit_col1, crit_col2 = crit_container.columns(2)

    # note: for streamlit, each text area must have unique key
    crit_col1.text_area(f'{subcriterion["name"]} Retrieved Text')
    crit_col2.text_area(f'{subcriterion["name"]} Suggested Response')


def create_crit_mgmt_layout(crit_expander, subcriterion):
    form = crit_expander.form(f'{subcriterion["name"]} form')
    # with crit_container.form("my_form"):
    with form:
        st.text_area(f'{subcriterion["name"]} Text', subcriterion["text"])
        st.text_area(f'{subcriterion["name"]} Prompt', subcriterion["prompt"])
    # crit_expander.text_area(f'{subcriterion["name"]} Text', subcriterion["text"])
    # crit_expander.text_area(f'{subcriterion["name"]} Prompt', subcriterion["prompt"])
        crit_submit_button = st.form_submit_button("Save")

# def display_results(pdf_doc):
#     # take uploaded PDF, extract and clean text
#     st.session_state.cleaned_text = return_clean_pdf_text(pdf_doc)
#
#     # obtain text length
#     st.session_state.text_length = len(cleaned_text)
#
#     # break into text chunks for embedding
#     text_chunks = get_text_chunks(cleaned_text)
#
#     # get number of tokens and price. Note that due to text overlap we use text_chunks variable (not cleaned_text)
#     st.session_state.nr_tokens, st.session_state.price = get_nr_of_tokens_and_price(text_chunks, 0.0001)
#
#     # communicate this to user
#     text_len_cont.write(st.session_state.text_length)
#     token_nr_container.write(st.session_state.nr_tokens)
#     price_container.write(st.session_state.price)
#     clean_text_exp.text_area("", cleaned_text, height=500)
#     if embed_button:
#         # get vector store
#         with fact_container.spinner("Processing"):
#             st.session_state.vector_store = get_vectorstore(text_chunks)
#             fact_container.write("Embedding completed!")