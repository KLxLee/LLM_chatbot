import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from modules.telegram_channel import TelegramChannel
import os
from pyngrok import ngrok
import uvicorn

from RAG.embedding_data import embedding_data
from RAG.generate_response import generate_respond

load_dotenv(override=True)
telegram_api_key = os.environ.get("TELEGRAM_API_KEY", "")
telegram_secret_token = os.environ.get("TELEGRAM_SECRET_TOKEN", "default_sercret_token")
ngrok_auth_token = os.environ.get("NGROK_AUTH_TOKEN", "")


# FastAPI app instance
app = FastAPI()

# # Define a Pydantic model for the input data
# class Query(BaseModel):
#     text: str  # The text input query to send to the LLM

# # OpenAI API Key setup (ensure you have your OpenAI API key)
# openai.api_key = "your-openai-api-key-here"

# @app.post("/get-llm-response/")
# async def get_llm_response(query: Query):
#     try:
#         # Send the query to OpenAI's GPT model (you can change 'text-davinci-003' to any GPT model)
#         response = openai.Completion.create(
#             model="text-davinci-003",  # Or another model
#             prompt=query.text,
#             max_tokens=150  # Adjust token limit based on your needs
#         )

#         # Return the LLM response
#         return {"response": response.choices[0].text.strip()}

#     except Exception as e:
#         # If there's an error (e.g., API issue), return an HTTP exception
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import Request

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    telg2 = TelegramChannel(os.environ.get("TELEGRAM_API_KEY", ""))
    if telg2.authenticate_webhook_request(request, telegram_secret_token):
        print("auth")
    else:
        print("Not auth")
        return None
    input_data = await telg2.webhook_adapter(request)
    print(input_data)
    print(input_data.utterance)
    print(input_data.conversation_id)
    # Send a reply
    resp = generate_respond(input_data.utterance)

    await telg2.send_message(input_data.conversation_id, f"You said: {input_data.utterance} \n {resp}")

    return {"status": "ok"}

# UVICORN_CONFIG: dict[str, Any] = {
#     "host": "0.0.0.0",
#     "port": 8000,
#     "reload": settings.HOT_RELOAD,
#     "server_header": False,
# }


# Expose the server using pyngrok
def expose_with_ngrok():
    # Kuan Lim NGROK ID
    ngrok.set_auth_token(ngrok_auth_token)
    NgrokTunnel = ngrok.connect(8000)  # Expose port 8000
    print(NgrokTunnel)
    return NgrokTunnel.public_url

async def init_telegram_webhook(url):
    # asyncio.run(init_telegram_webhook(NGROK_PUBLIC_URL))
    print(url)
    telg = TelegramChannel(telegram_api_key)
    response = await telg.initialize_webhook(url+'/telegram-webhook', 'SECRET_TOKEN')

    return response

if __name__ == "__main__":
    print("Please wait patiently for embedding data into vector database")
    print(f"Calling function: {embedding_data.__name__}")
    embedding_data()

    NGROK_PUBLIC_URL = expose_with_ngrok()

    # Run the asynchronous function synchronously
    response = asyncio.run(init_telegram_webhook(NGROK_PUBLIC_URL))
    if response: 
        print("Success set telegram webhook")
    else: 
        print("Failed set telegram webhook")

    print("Starting uvicorn server")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
