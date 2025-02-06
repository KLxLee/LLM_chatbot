# LLM Chatbot
A custom knowledge chatbot project integrated with Telegram Bot.  
You can add PDF or text files to the dedicated folder in the repository.  
The knowledge documents will be embedded into the vector database during the application initialization stage.  
You can chat with the Telegram bot and receive responses from the LLM bot.

---

## Deployment Guide

### 1. Clone the repository and change the directory:
```bash
git clone https://github.com/KLxLee/LLM_chatbot
cd LLM_chatbot
```

### 2. Provide your OpenAI API key:
To reduce server hardware requirements, a local AI model is not implemented in this project.
1. Create an OpenAI account and obtain the API key. You can find the instructions here:  
   [How to Get OpenAI Access Token](https://docs.text-gen.com/_notes/old/general/Get+OpenAI+Access+Token).
2. Define your OpenAI API key in the `.env` file with the variable name `OPENAI_API_KEY`.

### 3. Expose a public port using NGROK:
NGROK is a cross-platform tool that allows developers to expose a local development server to the internet easily.  
For users who prefer not to set up a cloud server, NGROK can be used to expose a public port.
1. Set up a free NGROK account.
2. Define your NGROK authentication key in the `.env` file with the variable name `NGROK_AUTH_TOKEN`.

### 4. Integrate with Telegram Bot:
1. Create a Telegram bot and obtain the bot authentication key. Follow these tutorials:  
   - [How to Create a Telegram Bot](https://www.directual.com/lesson-library/how-to-create-a-telegram-bot)  
   - [YouTube Tutorial](https://www.youtube.com/watch?v=UQrcOj63S2o)
2. Define your Telegram Bot API key in the `.env` file with the variable name `TELEGRAM_API_KEY`.

### 5. Add Custom Knowledge Documents:
1. Under the `LLM_chatbot/knowledge_docs` directory, there are two folders: `pdf_docs` and `txt_docs`.
2. Add your text and PDF documents to the corresponding folders.

### 6. Start the Application:
1. Build and run the containers:
   ```bash
   docker-compose up
   ```
2. It may take some time to build the containers and embed the data into the vector store.

### 7. Chat with the Custom Knowledge Bot via Telegram:
1. After the application is running, you can start chatting with the Telegram bot and ask questions based on the custom knowledge provided.
2. If you use the example knowledge files provided, you can ask questions like:
   - "Summary about The Adventures of Sir Aldric"
   - "Moral of the story The Tale of Prince John"
   - "Please tell me about the IKEA light manual"

---

## Upcoming Features:
1. **Conversation History**: Keep track of the conversation history with the bot.
2. **Custom System Prompt**: Implement custom system prompts for better conversation control.