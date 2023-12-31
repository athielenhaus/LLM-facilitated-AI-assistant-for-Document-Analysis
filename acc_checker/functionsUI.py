import json
import streamlit as st

def load_json(file_path):
    file = open(file_path, encoding="utf-8")   # specifying encoding necessary to display German characters
    criteria_sets = json.load(file)
    return criteria_sets


# this function generates the layout in the AccCheckTab
def create_crit_layout(crit_container, crit_dict, key):
    crit_container.write(crit_dict["text"])
    crit_col1, crit_col2 = crit_container.columns([3, 2])

    ##### MUST ADD SHORT NAME

    # set default values for text areas to blank if no source texts or responses are available yet
    retrieved_txt_def = "" if "source" not in crit_dict else crit_dict["source"]
    sug_resp_def = "" if "response" not in crit_dict else crit_dict["response"]

    # note: for streamlit, each text area must have unique key
    crit_col1.text_area(f'{key} Retrieved Text', retrieved_txt_def, height=200)
    crit_col2.text_area(f'{key} Suggested Response', sug_resp_def, height=200)


def generate_crit_layout(criterion):
    crit_expander = st.expander(f"**{criterion['name']}**")
    if "subcriteria" in criterion:
        for s in criterion["subcriteria"]:
            key = f'{criterion["name_short"]} {s["name"]}'
            create_crit_layout(crit_expander, s, key)
    else:
        key = f'{criterion["name_short"]}'
        create_crit_layout(crit_expander, criterion, key)


# saves criteria to dict, differentiating between criteria and subcriteria
def save_crit_to_dict(count, subcount, txt_key, prpt_key):
    if subcount is None:
        criterion= st.session_state.criteria_set[count]
        criterion['text'] = st.session_state[txt_key]
        criterion['prompt'] = st.session_state[prpt_key]
    else:
        subcriterion = st.session_state.criteria_set[count]["subcriteria"][subcount]
        subcriterion['text'] = st.session_state[txt_key]
        subcriterion['prompt'] = st.session_state[prpt_key]


# helper function for creating layout for CritMgmtTab
def create_crit_mgmt_layout(expander, criterion, key, count, subcount=None):
    txt_key = f'{key}_txt'
    prpt_key = f'{key}_prpt'
    crit_form = expander.form(f'{key} form')
    with crit_form:
        st.text_area(f'{criterion["name"]} Text', criterion["text"], key=txt_key)
        st.text_area(f'{criterion["name"]} Prompt', criterion["prompt"], key=prpt_key)
        crit_submit_button = st.form_submit_button("Save",
                                                   on_click=save_crit_to_dict,
                                                   kwargs={"count": count,
                                                           "subcount": subcount,
                                                           "txt_key": txt_key,
                                                           "prpt_key": prpt_key
                                                           }
                                                   )

# creates layout for CritMgmtTab
def generate_crit_mgmt_layout(criterion, count):
    crit_expander = st.expander(f"**{criterion['name']}**")
    if "subcriteria" in criterion:
        for subcount, subcriterion in enumerate(criterion["subcriteria"]):
            key = f'{criterion["name_short"]} {subcriterion["name"]}'
            create_crit_mgmt_layout(crit_expander, subcriterion, key, count, subcount)
    else:
        key = criterion["name_short"]
        create_crit_mgmt_layout(crit_expander, criterion, key, count)





# def display_results(pdf_doc):
#     # take uploaded PDF, extract and clean text stuff
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