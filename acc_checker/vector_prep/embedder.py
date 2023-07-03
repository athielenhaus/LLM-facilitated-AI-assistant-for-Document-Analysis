
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# create normal and Hypothetical Document Embedding (HyDE) vector stores
def get_vectorstore(text_chunks):

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    print('EMBEDDING COMPLETED!')

    return vectorstore