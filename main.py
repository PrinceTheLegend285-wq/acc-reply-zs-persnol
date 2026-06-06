import asyncio
import time
import os
from telethon import TelegramClient, events

# 🔑 ENV VARIABLES (Render)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# 💬 AUTO REPLY MESSAGE (FINAL YOUR VERSION)
AUTO_REPLY_TEXT = (
    "🤖 Zshadow Legend is currently offline for a few months.\n"
    "I am unable to respond to messages right now.\n"
    "Massage Again Later\n\n"
    "— System by Zshadow Legend"
)

DELAY_SECONDS = 10  # anti-spam protection

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

        # 🔥 anti spam cooldown
        if user_id in cooldown:
            if now - cooldown[user_id] < DELAY_SECONDS:
                return

        cooldown[user_id] = now

        # typing delay
        await asyncio.sleep(2)

        # reply
        await event.respond(AUTO_REPLY_TEXT)


async def main():
    print("⚡ System Is Active And Running...")

    await client.connect()

    if not await client.is_user_authorized():
        print("❌ Session not found. Run login.py locally first.")
        return

    print("🚀 Auto Reply Started Successfully...")

    await client.run_until_disconnected()


asyncio.run(main())