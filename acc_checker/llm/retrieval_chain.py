from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from acc_checker.functions import load_json
from acc_checker.vector_prep.embedder import get_vectorstore
from acc_checker.vector_prep.text_prep import return_clean_pdf_text, get_text_chunks

def get_retrieval_chain(vector_store):
    llm = OpenAI(temperature=0.0)  # initialize LLM model

    # turbo_llm = ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo')

    '''Notes on from_llm method: takes llm, prompt (see prompt template) and any kwargs as arguments'''
    retrieval_chain = RetrievalQA.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 1}),
        # memory = memory,
        return_source_documents=True
    )
    return retrieval_chain


def get_response_with_sources(query_list, retrieval_chain):
    response_list = retrieval_chain.apply(query_list)

    file_path = 'criteria_sets.json'
    criteria_sets = load_json(file_path)
    criteria = criteria_sets['criteria_sets'][0]['criteria']
    for r in response_list:
        pass

# get queries / prompts from dict and combine them
def prep_queries():
    file_path = '../criteria_sets.json'
    criteria_sets = load_json(file_path)
    criteria = criteria_sets['criteria_sets'][0]['criteria']
    for c in criteria:
        pass

    # save response to dict
    # save doc to dict

file_path = '../criteria_sets.json'
criteria_sets = load_json(file_path)
criteria = criteria_sets['criteria_sets'][0]['criteria']
subcriteria = criteria[0]['subcriteria']
# print(subcriteria[0]['prompt'])

final_prompt = f'''Untersuche den Text um diese Frage zu beantworten: {subcriteria[0]['prompt']['query']}.

Dein Ton ist juristisch und professionell.

Beispieltext: {subcriteria[0]['prompt']['text_example']}
Beispielantwort: {subcriteria[0]['prompt']['answer_example']}
'''


clean_text = return_clean_pdf_text()
text_chunks = get_text_chunks()
vector_store = get_vectorstore(text_chunks)
get_retrieval_chain(vector_store)


print(final_prompt)