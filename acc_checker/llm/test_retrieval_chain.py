from retrieval_chain import AnalysisExecutor
from langchain.docstore.document import Document
from acc_checker.text_prep.embedder import Embedder
from langchain.chains import RetrievalQA
import unittest

class TestAnalysisExecutor(unittest.TestCase):

    def setUp(self) -> None:
        self.criteria_set = {"crit1": "name1", "crit2": "name2"}
        self.doc1 = Document(page_content="hello", metadata={"source": "source_a"})
        self.doc2 = Document(page_content="world", metadata={"source": "source_b"})
        self.vector_store = Embedder([self.doc1, self.doc2]).vector_store
        self.ae = AnalysisExecutor(self.criteria_set, self.vector_store)
        self.retrieval_chain = self.ae.get_retrieval_chain(self.vector_store)


    def test_get_retrieval_chain(self):
        result = self.ae.get_retrieval_chain(self.vector_store)
        self.assertIsInstance(result, RetrievalQA)


    def test_get_llm_response_with_sources(self):
        prompt= "does 1 + 1 equal 4? Answer yes or no"
        response = self.ae.get_llm_response_with_sources(self.retrieval_chain, prompt)
        assert 'No' in response['result']
        assert response['source_documents'][0].page_content == 'hello'


    def test_combine_doc_strings(self):
        docs = [self.doc1, self.doc2]
        source_string = self.ae.combine_doc_strings(docs)
        self.assertEquals(source_string, "hello (source: source_a) world (source: source_b) ")


    def test_get_and_store_llm_response_and_source_docs(self):
        ### create example
        pass
        # get_and_store_llm_response_and_source_docs(crit_dict, retrieval_chain)
        # prompt = "is red the same as green? Answer yes or no, give a one-word response."
        # assert prompt.lower() == 'no'
