from langchain.document_loaders import PDFPlumberLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
import tempfile
import os
import pdfplumber


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


    def save_as_temp_file(self, file_obj):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_path = temp_file.name

            # Write the contents of the file-type object to the temporary file
            temp_file.write(file_obj.read())

            os.remove(temp_path)


    def load_data(self, file_path):
        loader = PDFPlumberLoader(file_path)
        data = loader.load()
        return data



fp= FileProcessor()
data = fp.load_data('test.pdf')
print(data)
