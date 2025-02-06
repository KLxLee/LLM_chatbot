import weaviate

client = weaviate.Client("http://localhost:8080")  # Change to your Weaviate URL



schema = {
    "classes": [
        {
            "class": "Document",
            "vectorizer": "none",  # Disable built-in vectorizer if using external embeddings
            "properties": [
                {"name": "text", "dataType": ["string"]},
            ],
        }
    ]
}

client.schema.create(schema)

import openai

openai.api_key = "your-openai-api-key"

def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

data = [
    "The quick brown fox jumps over the lazy dog.",
    "Weaviate is a vector database.",
]

with client.batch as batch:
    for text in data:
        embedding = get_embedding(text)
        batch.add_data_object(
            {"text": text}, "Document", vector=embedding
        )

query_text = "What is Weaviate?"
query_vector = get_embedding(query_text)

result = client.query.get("Document", ["text"]).with_near_vector(
    {"vector": query_vector}
).with_limit(1).do()

print(result)