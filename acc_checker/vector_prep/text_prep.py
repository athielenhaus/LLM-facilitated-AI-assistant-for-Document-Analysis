import io
import re
import tiktoken
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
from PyPDF2 import PdfReader

# class TextProcessor():
#     file = None



def extract_text_by_page(file):
    # with open(pdf_path, 'rb') as fh:
    for page in PDFPage.get_pages(file,
                                  caching=True,
                                  check_extractable=True):
        resource_manager = PDFResourceManager()

        fake_file_handle = io.StringIO()

        converter = TextConverter(resource_manager,
                                  fake_file_handle)

        page_interpreter = PDFPageInterpreter(resource_manager,
                                              converter)

        page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

        yield text

        # close open handles
        converter.close()
        fake_file_handle.close()


# text extracted via PDFminer has hyphens from line-breaks, therefore we create a regex function
def replace_hyphens(text):
    pattern = r'([a-z])-([a-z])'  # Pattern to match 'lowercase letter - lowercase letter'
    replacement = r'\1\2'  # Replacement pattern is equivalent to ''

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)

    # Iterate over the matches and replace the hyphen-separated lowercase letters
    for match in matches:
        text = text.replace(f'{match[0]}-{match[1]}', f'{match[0]}{match[1]}')
    return text


def return_clean_pdf_text(file):    # note - a filepath will NOT work
    doc = extract_text_by_page(file)
    pages = [page for page in doc]

    # replace hyphens and a string ("\x0c") automatically added by PDFminer at end of each page
    cleaned_pages = [replace_hyphens(page).replace("\x0c", "") for page in pages]

    cleaned_text = ''.join(cleaned_pages)
    return cleaned_text



# split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        # separator= "\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    return chunks



# get number of tokens which will be submitted for embedding as well as price
def get_nr_of_tokens_and_price(chunks, price_per_1k_tokens):
    '''takes as arguments chunks created via previous function as well as price which can be researched on OpenAI website
    (https://openai.com/pricing)'''

    nr_tokens = 0

    for chunk in chunks:
        enc = tiktoken.get_encoding("p50k_base")
        chunk_tokens = enc.encode(chunk)
        nr_tokens += len(chunk_tokens)

    price = round((nr_tokens / 1000) * price_per_1k_tokens, 4)

    return nr_tokens, price


def process_text(pdf_doc):
    # take uploaded PDF, extract and clean text
    st.session_state.cleaned_text = return_clean_pdf_text(pdf_doc)

    # obtain text length
    st.session_state.text_length = len(st.session_state.cleaned_text)

    # break into text chunks for embedding
    text_chunks = get_text_chunks(st.session_state.cleaned_text)

    # get number of tokens and price. Note that due to text overlap we use text_chunks variable (not cleaned_text)
    st.session_state.nr_tokens, st.session_state.price = get_nr_of_tokens_and_price(text_chunks, 0.0001)

    # communicate this to user
    text_len_cont.write(st.session_state.text_length)
    token_nr_container.write(st.session_state.nr_tokens)
    price_container.write(st.session_state.price)
    clean_text_exp.text_area("", st.session_state.cleaned_text, height=500)
    if embed_button:
        # get vector store
        with fact_container.spinner("Processing"):
            st.session_state.vector_store = get_vectorstore(text_chunks)
            fact_container.write("Embedding completed!")