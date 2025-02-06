FROM python:3.12-slim

# Install dependencies
RUN pip install pyngrok fastapi uvicorn

# Copy application files
COPY . /app
WORKDIR /app

# Expose the app port
EXPOSE 8000

# Run the app and pyngrok tunnel
CMD ["python", "-c", "from pyngrok import ngrok; import uvicorn; ngrok.connect(8000); uvicorn.run('main:app', host='0.0.0.0', port=8000)"]
