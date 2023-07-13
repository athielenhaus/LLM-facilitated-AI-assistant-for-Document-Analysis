# AI Accreditation Assistant 

## Brief Introduction to Higher Education Quality Assurance in Germany
For decades, German university- and higher-education programs have been audited by external "Accreditation" agencies. 
The purpose of these audits is to ensure conformity with state-level education regulations. These include formal, objective requirements, pertaining for example to:

- the length of degree programs
- the degree types which can be awarded
- the structure of the degree programs
- the proper implementation of European regulations (for example, the European Credit Transfer System - ECTS)
- etc.

An example of one such regulation:

>"The standard periods of study for full-time study are six, seven or eight semesters for bachelor's programs and four, three or two semesters for master's programs. For bachelor's degree programs, the standard period of study for full-time study is at least three years. For consecutive degree programs, the total standard period of full-time study is five years (ten semesters)." (Source: _Musterrechtsverordnung_, Stiftung Akkreditierungsrat)

#### Current quality assurance procedure
To determine whether or not these formal criteria are met, auditors review the official documentation provided by the higher education institution. This documentation typically includes:

- the syllabus
- the examination regulations (_Prüfungsordnung_), 
- the module catalog (_Modulhandbuch_) 

...and a variety of other documents. Auditors summarize their findings in an official Accreditation Report, which is submitted to the federal German Accreditation Board.
Essentially, this part of the procedure is a simple search and check exercise which, however, due to the often vast amounts of documentation provided, can be tedious to complete. Formal HEI documentation can differ significantly in terms of structure and content from one institution to the next. 

#### Project Objectives

The goal of this project is to: 
- parse formal HEI documents
- retrieve content relevant to the official criteria
- with the help of a Large Language Model (LLM), generate conclusions and summarize findings
- provide a tool with a user interface which allows users to upload formal documents, and view generated conclusions and related source documents
- determine whether this is a viable approach in terms of costs

While there are presumably multiple use-cases for LLMs in the context of accreditation, the one described above may be among the simplest ones to achieve, also because data samples in the form of formal documents published on German HEI websites are readily available. 

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
