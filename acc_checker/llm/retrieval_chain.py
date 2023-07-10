from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA


class AnalysisExecutor:


    def __init__(self, criteria_set, vector_store):
        self.criteria_set = criteria_set
        self.vector_store = vector_store
        self.retrieval_chain = self.get_retrieval_chain(vector_store)
        self.answer_list = self.get_and_store_all_llm_responses_and_source_docs(criteria_set, self.retrieval_chain)


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
    def get_and_store_all_llm_responses_and_source_docs(self, criteria_set, retrieval_chain):
        criteria_and_response_set = criteria_set
        for c in criteria_and_response_set:
            if "subcriteria" in c:
                for s in c["subcriteria"]:
                    if s["prompt"]:
                        self.get_and_store_llm_response_and_source_docs(s, retrieval_chain)
                    else:
                        raise Exception(f"Missing prompt for criterion: {c['name']}, subcriterion {s['name']}")
            elif c["prompt"]:
                self.get_and_store_llm_response_and_source_docs(c, retrieval_chain)
            else:
                raise Exception(f"Missing prompt for criterion: {c['name']}")

        return criteria_and_response_set



