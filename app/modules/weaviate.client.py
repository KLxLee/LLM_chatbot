import asyncio
from typing import Any

import weaviate
from weaviate.exceptions import WeaviateBaseError


class WeaviateClientManager:
    _weaviate_client = None

    @classmethod
    def initialise_vector_store(cls, bot_id: str = "") -> WeaviateVectorStore:
        try:
            client = cls.get_client()
            # bot_id maps to tenant_id on our vector database
            vector_store = WeaviateVectorStore(
                weaviate_client=client,
                index_name="Vecs",
                client_kwargs={"tenant_id": bot_id},
            )

            return vector_store
        except Exception as e:
            logger.error(f"Error when loading vector_store: {e}")
            raise

    @staticmethod
    def delete_tenant_and_data() -> None:
        pass

    @classmethod
    def get_client(cls) -> weaviate.Client:
        if cls._weaviate_client == None:
            try:
                weaviate_url = f"http://{settings.VECTOR_DB_HTTP_HOST}:{settings.VECTOR_DB_HTTP_PORT}"
                api_key = settings.VECTOR_DB_API_KEY

                cls._weaviate_client = weaviate.Client(
                    weaviate_url, weaviate.auth.AuthApiKey(api_key)
                )

            except Exception as e:
                logger.error(f"Error to create Weaviate client: {e}")
                raise
        return cls._weaviate_client

    @classmethod
    async def check_connection(cls) -> bool:
        try:
            client = cls.get_client()

            if await asyncio.to_thread(client.is_ready):
                logger.info("Weaviate Vector DB connection is ready")
                return True
            else:
                return False
        except WeaviateBaseError as e:
            logger.error(f"Failed to connect to Weaviate Vector DB: {e}")
            return False
