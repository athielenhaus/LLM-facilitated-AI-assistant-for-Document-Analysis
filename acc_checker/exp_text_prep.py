from acc_checker.vector_prep.text_prep import return_clean_pdf_text, get_text_chunks
from acc_checker.vector_prep.embedder import get_vectorstore
from dotenv import load_dotenv

load_dotenv()
file_path = 'C:/Users/Arne/Downloads/Prüfungsordnungen/TH Köln Ba Erneuerbare Energien.pdf'

with open(file_path, 'rb') as fh:
    clean_text = return_clean_pdf_text(fh)
    text_chunks = get_text_chunks(clean_text)
    vector_store = get_vectorstore(text_chunks)

print(vector_store)