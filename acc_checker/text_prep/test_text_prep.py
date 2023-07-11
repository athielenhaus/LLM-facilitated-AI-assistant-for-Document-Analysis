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


    def test_get_text_chunks(self):
        fp = FileProcessor()
        text = "This is a simple random test string\n\nfor checking recursive splitting. It should\nsplit on double new lines, new lines, end of sentences and finally spaces."
        text_chunks = fp.get_text_chunks(text, 50, 0)
        assert text_chunks[0].page_content == "This is a simple random test string"
        assert text_chunks[1].page_content == "for checking recursive splitting. It should"


    def test_combine_chunks_with_metadata(self):
        fp = FileProcessor()
        doc1 = Document(page_content="this is a test string. Hallelujah!", metadata={"test_info": "a"})
        doc2 = Document(page_content="this is another, somewhat longer test string", metadata={"test_info": "b"})
        text_chunk1 = Document(page_content="this is a test string.")
        text_chunk2 = Document(page_content="somewhat longer test string")
        original_chunks = [text_chunk1, text_chunk2]
        chunks_with_metadata = fp.combine_chunks_with_metadata([doc1, doc2], [text_chunk1, text_chunk2])
        assert chunks_with_metadata[0].page_content == "this is a test string."
        assert chunks_with_metadata[0].metadata == {"test_info": "a"}
        assert chunks_with_metadata[1].page_content == "somewhat longer test string"
        assert chunks_with_metadata[1].metadata == {"test_info": "b"}
        assert len(chunks_with_metadata) == len(original_chunks)


if __name__ == '__main__':
    unittest.main()