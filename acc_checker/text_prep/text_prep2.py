from langchain.document_loaders import PDFPlumberLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
import tempfile
import os
import re


class FileProcessor:

    def __init__(self):

        self.file = None
        # self.loaded_data = self.load_data(self.file)
        self.cleaned_text = ""
        self.text_chunks = None
        self.text_length = 0
        self.nr_tokens = 0
        self.price = 0
        self.token_price = 0


    def save_as_temp_file_and_get_data(self, file_obj):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_path = temp_file.name

            # Write the contents of the file-type object to the temporary file
            temp_file.write(file_obj.read())
            data = self.load_data(temp_path)

            temp_file.close()
            os.remove(temp_path)

        return data


    # PDFPlumberLoader.load() returns list with page content and metadata for each page in PDF
    def load_data(self, file_path):
        loader = PDFPlumberLoader(file_path)
        data = loader.load()
        return data


    def clean_docs(self, data):
        cleaned_docs = []
        for doc in data:
            text = doc.page_content
            clean_content = re.sub(r'\n{2,}', '###!!!###', text).replace('-\n', '').replace('\n',' ').replace('###!!!###','\n\n')
            cleaned_doc = Document(page_content=clean_content, metadata=doc.metadata)
            cleaned_docs.append(cleaned_doc)
        return cleaned_docs

    def get_full_text(self, docs):
        full_text = ''
        for doc in docs:
            full_text += doc.page_content
        return full_text

    def get_text_chunks(self, full_text, chunk_size=1000, chunk_overlap=200):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", "(?<=\. )", " ", ""],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        text_chunks = text_splitter.create_documents([full_text])
        return text_chunks

