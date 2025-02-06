from modules.weaviate_client import weaviate_client
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_openai import OpenAIEmbeddings

class VectorStore:
    _vector_store = None

    @classmethod
    def get_vectorstore_client(cls) -> WeaviateVectorStore:
        if cls._vector_store == None:
            try:
                cls._vector_store = WeaviateVectorStore(client=weaviate_client,index_name="LangChain_Project_EmbeddingIndex",embedding=OpenAIEmbeddings(),text_key="text")

            except Exception as e:
                print(f"Error to create Vector Store client: {e}")
                raise
        return cls._vector_store   

vectorstore_client = VectorStore.get_vectorstore_client()
