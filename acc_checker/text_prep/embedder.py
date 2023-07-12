from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv


class Embedder():

    def __init__(self, text_chunks):
        self.vector_store = self.get_vectorstore(text_chunks)

    def get_vectorstore(self, docs):
        load_dotenv()
        if docs is not None:
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
            return vectorstore
        else:
            pass

# class Embedder:
#
#     def __init__(self, text_chunks):
#         self.text_chunks = text_chunks
#         self.vectorstore = self.get_vectorstore(self.text_chunks)
#
#     def get_vectorstore(self, text_chunks):
#         embeddings = OpenAIEmbeddings()
#         vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#         print('EMBEDDING COMPLETED!')
#
#         return vectorstore
