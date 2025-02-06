from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

from RAG.load_knowledge_docs import load_local_txt, load_local_pdf
from modules.vectorstore_client import vectorstore_client

def embedding_data():
    try:
        txt_files=load_local_txt()
        text_splitter=CharacterTextSplitter(chunk_size=500,chunk_overlap=0)
        for txt_file in txt_files:
            chunks=text_splitter.split_documents(txt_file)
            vectorstore_client.add_documents(chunks)

        pdf_files=load_local_pdf()
        pdf_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Adjust based on your use case
            chunk_overlap=100  # Helps maintain context across chunks
            )
        for pdf_file in pdf_files:
            chunks=pdf_splitter.split_documents(pdf_file)
            vectorstore_client.add_documents(chunks)

    except Exception as e:
        raise("Failed to embedded data into vector db: ", e)
