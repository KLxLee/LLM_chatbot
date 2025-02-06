import ipaddress
from typing import Any
from urllib.parse import quote

import httpx
from fastapi import Request
from pydantic import BaseModel
import logging as logger


TELEGRAM_IP_RANGES = [
    ipaddress.ip_network("149.154.160.0/20"),
    ipaddress.ip_network("91.108.4.0/22"),
]


class TelegramChannelInput(BaseModel):
    conversation_id: str
    utterance: str
    user_id: str | None = None
    bot_id: str | None = None
    message_id: int | None = None
    timestamp: int | None = None
    message_type: str = "text"
    metadata: dict[str, Any] | None = None


class TelegramChannel:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.telegram_api_url = f"https://api.telegram.org/bot{api_key}"

    @staticmethod
    async def webhook_adapter(request: Request) -> TelegramChannelInput:
        """
        Adapts incoming webhook data to a standardized ChannelInput object.

        Parameters:
            data (dict[str, Any]): The incoming webhook data.

        Returns:
            ChannelInput: The adapted channel input.
        """
        data = await request.json()
        message = data.get("message", {})
        chat = message.get("chat", {})
        user = message.get("from", {})

        utterance = message.get("text")

        if not utterance:  # Handle non-text messages
            if "photo" in message:
                utterance = "[Photo received]"
                message_type = "photo"
            elif "sticker" in message:
                utterance = "[Sticker received]"
                message_type = "sticker"
            elif "voice" in message:
                utterance = "[Voice message received]"
                message_type = "voice"
            elif "video" in message:
                utterance = "[Video received]"
                message_type = "video"
            elif "document" in message:
                utterance = "[Document received]"
                message_type = "document"
            else:
                utterance = "[Unknown message type]"
                message_type = "unknown"
        else:
            message_type = "text"

        return TelegramChannelInput(
            conversation_id=str(chat.get("id")),  # Chat ID
            utterance=utterance,
            user_id=str(user.get("id")),
            bot_id=str(data.get("bot", {}).get("id")),  # Bot ID (if available)
            message_id=message.get("message_id"),  # Message ID
            timestamp=message.get("date"),  # Unix timestamp
            message_type=message_type,  # Message type
            metadata={"chat_type": chat.get("type")},
        )

    async def authenticate_webhook_request(
        self, request: Request, secret_token: str
    ) -> bool:
        """Authenticates an incoming webhook request."""
        telegram_token = request.headers.get("X-Telegram-Bot-API-Secret-Token")
        if telegram_token != secret_token:
            return False

        if request.client is None or request.client.host is None:
            return False

        sender_ip = request.client.host  # Get sender's IP
        try:
            ip_addr = ipaddress.ip_address(sender_ip)
        except ValueError:  # Invalid IP format
            return False

        return any(ip_addr in net for net in TELEGRAM_IP_RANGES)

    async def send_message(self, conversation_id: str, message: str) -> bool:
        """Send a message to a Telegram chat."""
        response = await self._post_request(
            "sendMessage", {"chat_id": conversation_id, "text": message}
        )
        return bool(response.get("ok", False))

    async def initialize_webhook(self, url: str, secret_token: str) -> bool:
        """Set the Telegram webhook."""
        encoded_url = quote(url, safe=":/")
        print(encoded_url)
        response = await self._post_request(
            "setWebhook", {"url": encoded_url, "secret_token": secret_token}
        )
        return bool(response.get("ok", False))

    async def delete_webhook(self) -> bool:
        """Delete the existing Telegram webhook."""
        response = await self._post_request("deleteWebhook")
        return bool(response.get("ok", False))

    async def _post_request(
        self, endpoint: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Helper function to send an async POST request to Telegram API."""
        url = f"{self.telegram_api_url}/{endpoint}"
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data: dict[str, Any] = response.json()
                if not data.get("ok"):
                    logger.error(f"Telegram API error: {data.get('description')}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"Request failed: {e}")
                return {"ok": False}
            