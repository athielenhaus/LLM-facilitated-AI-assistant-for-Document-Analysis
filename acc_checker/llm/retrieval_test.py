from retrieval_chain import AnalysisExecutor

def test_get_retrieval_chain():


def test_get_llm_response_with_sources():


def test_combine_doc_strings():
    ### create doc
    AnalysisExecutor.combine_doc_strings()


def test_get_and_store_llm_response_and_source_docs():
    ### create example
    get_and_store_llm_response_and_source_docs(self, crit_dict, retrieval_chain)
    prompt = "is red the same as green? Answer yes or no, give a one-word response."
    assert prompt.lower() == 'no'
