import os
from text_prep2 import FileProcessor
from langchain.docstore.document import Document
import unittest

class TestFileProcessor(unittest.TestCase):


    def test_initiate_class(self):
        fp = FileProcessor()


    def test_load_data(self):
        fp = FileProcessor()
        data = fp.load_data('test.pdf')
        assert 'Foo-bar ban-anas Py-Charm' in data[0].page_content


    def test_save_as_temp_file_and_get_data(self):   # can take file
        fp = FileProcessor()
        with open('test.pdf', 'rb') as file:
            data = fp.save_as_temp_file_and_get_data(file)
        assert 'Foo-bar ban-anas Py-Charm' in data[0].page_content

    def test_clean_docs(self):
        fp = FileProcessor()
        doc1 = Document(page_content="\nsome sam-\nple text\n\nnew heading", metadata={"source": "local"})
        doc2 = Document(page_content="\n\n\n\n\n\n\nsome more sam-\nple text\n\nnew heading\neven more text", metadata={"source": "local"})
        test_docs= [doc1, doc2]
        cleaned_docs = fp.clean_docs(test_docs)
        assert cleaned_docs[0].page_content == " some sample text\n\nnew heading"
        assert cleaned_docs[1].page_content == "\n\nsome more sample text\n\nnew heading even more text"

    def test_get_full_text(self):
        fp = FileProcessor()
        doc1 = Document(page_content= "Hello ")
        doc2 = Document(page_content="World")
        full_text = fp.get_full_text([doc1, doc2])
        assert full_text == 'Hello World'


    def test_split_text_recursively(self):
        text = "This is a simple random test string\n\n for checking recursive splitting. It should split on double new lines, new lines, end of sentences and finally spaces."
        text_chunks = split_text_recursively(text, )
        assert text_chunks[0] == "This is a simple random test string"





if __name__ == '__main__':
    unittest.main()