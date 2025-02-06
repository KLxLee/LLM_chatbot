import os
import weaviate
from weaviate.connect import ConnectionParams


class WeaviateClientManager:
    _weaviate_client = None

    @classmethod
    def get_client(cls, connection_params: ConnectionParams) -> weaviate.WeaviateClient:
        if cls._weaviate_client == None:
            try:
                cls._weaviate_client = weaviate.WeaviateClient(connection_params)
                cls._weaviate_client.connect()

            except Exception as e:
                print(f"Error to create Weaviate client: {e}")
                raise
        return cls._weaviate_client

weaviate_host = os.environ.get("WEAVIATE_HOST", "localhost")
connection_params = ConnectionParams(
    http={
        "host": "weaviate",  # Use the service name of the Weaviate container
        "port": 8080,
        "secure": False,  # Set to True if using HTTPS
    },
    grpc={
        "host": "weaviate",  # Use the service name for gRPC
        "port": 50051,
        "secure": False,  # Set to True if using secure gRPC
    }
)
weaviate_client = WeaviateClientManager.get_client(connection_params)
