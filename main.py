import asyncio
import time
import os
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

AUTO_REPLY_TEXT = (
    "🤖 Zshadow Legend is currently offline for some months.\n"
    "He are unable to respond to messages right now.\n"
    "Massage again later."
    "System By Zshadow Legend."
)

DELAY_SECONDS = 10

client = TelegramClient(
    "auto_reply_session",
    API_ID,
    API_HASH,
    device_model="Zshadow Auto Reply",
    system_version="Zshadow OS",
    app_version="AutoReply v1.0"
)

cooldown = {}

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:

        user_id = event.sender_id
        now = time.time()

        if user_id in cooldown:
            if now - cooldown[user_id] < DELAY_SECONDS:
                return

        cooldown[user_id] = now

        await asyncio.sleep(2)
        await event.respond(AUTO_REPLY_TEXT)

async def main():
    print("⚡ System Is Active And Running...")
    await client.run_until_disconnected()

client.start = lambda: None  # safety patch (optional)
client.loop.run_until_complete(main())