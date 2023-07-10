from langchain.document_loaders import PDFPlumberLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

class FileProcessor:

    def __init__(self, file):

        self.file = file
        self.loaded_data = self.load_data(file)
        self.cleaned_text = ""
        self.text_chunks = None
        self.text_length = 0
        self.nr_tokens = 0
        self.price = 0
        self.token_price = 0

    def load_data(self, file):
        loader = PDFPlumberLoader(file)
        data = loader.load()
        return data




