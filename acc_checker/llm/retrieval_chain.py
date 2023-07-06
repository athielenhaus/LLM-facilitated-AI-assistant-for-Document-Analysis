from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from acc_checker.functions import load_json
from acc_checker.vector_prep.embedder import get_vectorstore
from acc_checker.vector_prep.text_prep import return_clean_pdf_text, get_text_chunks


class AnalysisExecutor:

    def __init__(self, criteria_set_dict, vector_store):
        self.criteria_set = criteria_set_dict
        self.vector_store = vector_store
        self.retrieval_chain = self.get_retrieval_chain(vector_store)
        self.answer_list = self.get_and_store_all_llm_responses_and_source_docs(criteria_set_dict, self.retrieval_chain)

    def get_retrieval_chain(self, vector_store):
        llm = OpenAI(temperature=0.0)  # initialize LLM model
        #         turbo_llm = ChatOpenAI(temperature= 0.0, model_name='gpt-3.5-turbo')
        retrieval_chain = RetrievalQA.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            # memory = memory,
            return_source_documents=True)
        return retrieval_chain

    def get_llm_response_with_sources(self, retrieval_chain, prompt):
        response = retrieval_chain({"query": prompt})
        return response

    # source documents must be list containing <class 'langchain.schema.Document'> objects
    def combine_doc_strings(self, source_documents):
        if source_documents is None:
            raise Exception("No source document returned!")
        else:
            source_str = ""
            for d in source_documents:
                source_str += d.page_content
            return source_str

    def get_and_store_llm_response_and_source_docs(self, crit_dict, retrieval_chain):
        result = self.get_llm_response_with_sources(retrieval_chain, crit_dict["prompt"])
        crit_dict["response"] = result["result"]
        crit_dict["source"] = self.combine_doc_strings(result["source_documents"])

    # takes criteria set dict and langchain retrieval chain as arguments
    # returns list which is a version of the original criteria list, expanded to include LLM responses and retrieved source docs
    def get_and_store_all_llm_responses_and_source_docs(self, criteria_set_dict, retrieval_chain):
        criteria_and_response_list = criteria_set_dict['criteria_sets'][0]['criteria']
        for c in criteria_and_response_list:
            if c["subcriteria"]:
                for s in c["subcriteria"]:
                    if s["prompt"]:
                        self.get_and_store_llm_response_and_source_docs(s, retrieval_chain)
                    else:
                        raise Exception(f"Missing prompt for criterion: {c['name']}, subcriterion {s['name']}")
            elif c["prompt"]:
                self.get_and_store_llm_response_and_source_docs(c, retrieval_chain)
            else:
                raise Exception(f"Missing prompt for criterion: {c['name']}")

        return criteria_and_response_list




# # sets up a langchain retrieval chain consisting of an LLM and a vector store
# def get_retrieval_chain(vector_store):
#
#     llm = OpenAI(temperature=0.0)  # initialize LLM model
#
#     # turbo_llm = ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo')
#
#     # from_llm method takes llm, prompt (see prompt template) and  kwargs as arguments
#     retrieval_chain = RetrievalQA.from_llm(
#         llm=llm,
#         retriever=vector_store.as_retriever(search_kwargs={"k": 1}),
#         # memory = memory,
#         return_source_documents=True
#     )
#     return retrieval_chain
#
#
# def get_response_with_sources(query_list, retrieval_chain):
#     response_list = retrieval_chain.apply(query_list)
#
#     file_path = 'criteria_sets.json'
#     criteria_sets = load_json(file_path)
#     criteria = criteria_sets['criteria_sets'][0]['criteria']
#     for r in response_list:
#         pass
#
#
# # get queries / prompts from dict and combine them
# def prep_queries():
#     file_path = '../criteria_sets.json'
#     criteria_sets = load_json(file_path)
#     criteria = criteria_sets['criteria_sets'][0]['criteria']
#     for c in criteria:
#         pass
#
#     # save response to dict
#     # save doc to dict
#
# file_path = '../criteria_sets_simple.json'
# criteria_sets = load_json(file_path)
# criteria = criteria_sets['criteria_sets'][0]['criteria']
# subcriteria = criteria[0]['subcriteria']
# print(subcriteria[0]['prompt'])







# final_prompt = f'''Untersuche den Text um diese Frage zu beantworten: {subcriteria[0]['query']}.
#
# Dein Ton ist juristisch und professionell.
#
# Beispieltext: {subcriteria[0]['text_example']}
# Beispielantwort: {subcriteria[0]['answer_example']}
# '''

