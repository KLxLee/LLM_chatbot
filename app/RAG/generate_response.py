from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from modules.vectorstore_client import vectorstore_client
from RAG.load_knowledge_docs import load_system_prompt

llm=ChatOpenAI(model="gpt-4o")

def generate_respond(utterance: str) -> str:

    template= """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use five sentences minimum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:
    """

    # system_prompt = load_system_prompt()

    retriever=vectorstore_client.as_retriever()
    prompt=ChatPromptTemplate.from_template(template)
    rag_chain=(
        {"context":retriever,"question":RunnablePassthrough()}
        |prompt
        |llm
        |StrOutputParser()
    )

    response=rag_chain.invoke(utterance)
    print(response)

    return response

    # response=rag_chain.invoke("write is the moral of SirAldric")
    # print(response)
    # response=rag_chain.invoke("please tell summary about ikea light switch manual")
    # print(response)
