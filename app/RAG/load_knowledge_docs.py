import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define directories containing PDFs and text files
directory = os.path.abspath(os.path.join(os.getcwd(), "knowledge_docs"))
PDF_DIR = directory + "/pdf_docs/"
TXT_DIR = directory + "/txt_docs/"
SYSPROMPT_DIR = directory + "system_prompt.txt"

# Initialize text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Adjust based on your use case
    chunk_overlap=100  # Helps maintain context across chunks
)

def load_local_pdf():
    pdf_docs = []
    # Load PDFs
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            loader = PyMuPDFLoader(os.path.join(PDF_DIR, file))
            doc_chunks = loader.load()
            if doc_chunks:
                for chunk in doc_chunks:
                    chunk.metadata = {"source": file}  # Track file name
                pdf_docs.append(doc_chunks)
                print("Loaded pdf: ", file)
    return pdf_docs

def load_local_txt():
    txt_docs = []
    # Load text files
    for file in os.listdir(TXT_DIR):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(TXT_DIR, file))
            doc_chunks = loader.load()
            if doc_chunks:
                for chunk in doc_chunks:
                    chunk.metadata = {"source": file}
                txt_docs.append(doc_chunks)
                print("Loaded txt file: ", file)

    return txt_docs

def load_system_prompt():
    txt_docs = []

    loader = TextLoader(os.path.join(SYSPROMPT_DIR, file))
    doc_chunks = loader.load()
    if doc_chunks:
        for chunk in doc_chunks:
            chunk.metadata = {"source": file}
        txt_docs.append(doc_chunks)
        print("Loaded txt file: ", file)

    return txt_docs
