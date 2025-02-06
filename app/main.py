import asyncio
from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI, Request
from modules.telegram_channel import TelegramChannel
import os
from pyngrok import ngrok
import uvicorn

from RAG.embedding_data import embedding_data
from RAG.generate_response import generate_respond

# Load environment variables
telegram_api_key = os.environ.get("TELEGRAM_API_KEY", "")
telegram_secret_token = os.environ.get("TELEGRAM_SECRET_TOKEN", "default_sercret_token")
ngrok_auth_token = os.environ.get("NGROK_AUTH_TOKEN", "")


# FastAPI app instance
app = FastAPI()

@app.post("/conversation")
async def telegram_webhook(request: Request):
    telg2 = TelegramChannel(os.environ.get("TELEGRAM_API_KEY", ""))
    if not await telg2.authenticate_webhook_request(request, telegram_secret_token):
        print("Telegram Secret token authenticate failed")
        return None
    
    input_data = await telg2.webhook_adapter(request)

    # Send a reply
    resp = generate_respond(input_data.utterance)

    await telg2.send_message(input_data.conversation_id, f"User: {input_data.utterance}\nBot: {resp}")

    return {"status": "ok"}

# Expose the server using pyngrok
def expose_with_ngrok():
    ngrok.set_auth_token(ngrok_auth_token)
    NgrokTunnel = ngrok.connect(8000)  # Expose port 8000
    print(NgrokTunnel)
    return NgrokTunnel.public_url

async def init_telegram_webhook(url):
    # asyncio.run(init_telegram_webhook(NGROK_PUBLIC_URL))
    print(url)
    telg = TelegramChannel(telegram_api_key)
    response = await telg.initialize_webhook(url+'/conversation', telegram_secret_token)

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
