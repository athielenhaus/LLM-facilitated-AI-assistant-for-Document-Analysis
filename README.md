# LLM-facilitated AI Accreditation Procedure Assistant 
<img src="images/doc_check_screenshot.png" alt="drawing" width="700"/>

### Overview
This project uses Streamlit, OpenAI APIs and Langchain to create an online app which allows the user to upload PDF files and ask a Chatbot questions about them.

__The app currently does the following:__
- PDF import and text preprocessing:
    - imports PDF files
    - cleans text (removes uneccessary spaces, new lines, etc) and displays text in the User Interface (UI) for inspection
    - converts text into overlapping text chunks with a length of 1000 characters each
    - calculates the estimated embedding cost using tiktoken, and displays this in the UI
- Text embedding:
    - if the estimated cost is below the predetermined threshold, the user can click a button to embed the text chunks as vectors using OpenAIEmbeddings, and save them to a FAISS vector store
- Document Chatbot:
    - the user can use the DocBot tab in the user interface to submit queries about the documents
    - the queries are used in a similarity search to retrieve the most relevant text excerpts from the vector store
    - the excerpts are then submitted, along with the user's query, to ChatGPT using the OpenAI API
    - the API response is shown to the user

Check it out here: [https://acc-check.streamlit.app/](https://acc-check.streamlit.app/)

This chatbot assistant is a stepping-stone towards creating a more complex document analyzer and AI Accreditation Procedure Assistant.

### Background
In Germany, university- and higher-education programs must be regularly audited by external "Accreditation" agencies. The purpose of these audits is to ensure conformity with state-level education regulations, pertaining for instance to:

- the length of the degree programs 
- the degree types which can be awarded (M.Sc., B.A., B.Eng. etc.)
- the structure of the degree programs (use of appropriately sized modules)
- the proper implementation of European regulations (for example, the European Credit Transfer System - ECTS)
- etc.

An example of one such regulation:

>"The standard periods of study for full-time study are six, seven or eight semesters for bachelor's programs and four, three or two semesters for master's programs. For bachelor's degree programs, the standard period of study for full-time study is at least three years. For consecutive degree programs, the total standard period of full-time study is five years (ten semesters)." (Source: _Musterrechtsverordnung_, Stiftung Akkreditierungsrat)

#### Why an LLM-facilitated AI Accreditation Procedure Assistant?
To determine whether or not formal criteria are met, auditors review the official documentation provided by the higher education institution. This often includes hundreds of pages of documents, typically consisting of the syllabus, exam regulations (_Prüfungsordnung_), course descriptions (_Modulhandbuch_) and a variety of other documents.

Essentially, this part of the procedure is a simple search and check exercise which, however, due to the often vast amounts of documentation provided, can be tedious and time-consuming to complete. Formal HEI documentation can differ significantly in terms of structure and content from one institution to the next. 

__Project Objectives__
The goal of this project is therefore to: 
- parse formal HEI documents and retrieve content relevant to the official regulations
- generate conclusions and summarize findings with the help of an LLM
- provide a tool with a user interface which allows users to upload formal documents, and view generated conclusions and related source documents
- determine whether this is a viable approach in terms of costs and reliability

While there are presumably multiple use-cases for LLMs in the context of accreditation, the one described above may be among the simplest ones to achieve, also because data samples in the form of formal documents published on German HEI websites are readily available. 

#### Current Project Status:

An initial version of the app attempted to implement a full-fledged analysis tool, which submitted a catalog of questions about the document. However, the results were unsatisfactory, which is why for the moment it was decided to publish the simple version linked above. The corresponding code is found in the acc_prelim branch

### Challenges:

__Vector Search:__ in order to give the auditor peace of mind that the AI assistant's response is based on actual document content and not a hallucination, it is vital that the _most relevant_ text excerpts are retrieved from the document and displayed alongside the assistant's suggestion. It was attempted to achieve this via a vector search. However, slight differences in terminology and phrasing could significantly alter results. For instance, asking "How many _ECTS points_ does the program encompass?" could elicit a correct response, whereas "How many _credit points_ does the program encompass?" may result in an incorrect response, or the response "No relevant information could be found".
    - Two possible solutions have thus far been attempted:
        - before submitting the queries to the vector store, we search the document for the most important key words (for example "credit points" vs. "ECTS points", "bachelor" vs. "master", etc.), and adjust the queries accordingly. This method shows some promise.
        - use similar document search: using this method, the vector store is queried not with the actual question, but rather with a text which resembles the answer to the question. This involves two steps:
          - first, the LLM is used to generate a hypothetical answer. The instructions submitted to ChatGPT are something like "Generate a hypothetical answer to the following question: how many credit points does the university program encompass?". This results in a response similar to "The university program encompasses 180 credit points".
          - second, this response is used for a similarity search in the vector store. This is likely to generate more relevant results than submitting the initial query.
- Hallucinations - although the instructions submitted to ChatGPT advised it against hallucinating, this still happened on occassion

In the last weeks, additional tools have been published 

### Toolkit

the tools used include:

* Langchain: a relatively new library (released in October 2022) which simplifies working with LLMs. From this library I am using:
    - PDF loaders (PDFPlumber)
    - Text splitters: for splitting documents into chunks which can be processed for embedding purposes
    - OpenAI Embeddings: fast embeddings API which charges a small amount per submitted token.
    - Vector Store integrations: for saving embeddings to memory or disk (FAISS, ChromaDB...)
    - Retrieval chains: for conducting similarity searches in vector stores and submitting retrieved documents along with a query to an LLM
* OpenAI APIs: for accessing the OpenAI LLMs
* tiktoken: for converting text to tokens in order to estimate costs prior to embedding.
* Streamlit: a library for creating a simple frontend user interface.
* Unittest: for testing functions and classes

With the exception of the PDF loaders, this was my first time working with the tools above, which made it a fantastic learning experience.
