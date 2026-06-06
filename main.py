import asyncio
import time
import os
from telethon import TelegramClient, events
from flask import Flask
import threading

# ================== 🔑 ENV ==================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# ================== 💬 AUTO REPLY ==================
AUTO_REPLY_TEXT = (
    "🤖 Zshadow Legend is currently offline for a few months.\n"
    "I am unable to respond to messages right now.\n"
    "Message Again Later\n\n"
    "— System by Zshadow Legend"
)

DELAY_SECONDS = 10

# ================== 🤖 TELETHON ==================
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
    print("📩 Message detected:", event.raw_text)

    if event.is_private:
        user_id = event.sender_id
        now = time.time()

        # anti spam
        if user_id in cooldown:
            if now - cooldown[user_id] < DELAY_SECONDS:
                return

        cooldown[user_id] = now

        await asyncio.sleep(2)

        print("↩️ Reply sent")
        await event.respond(AUTO_REPLY_TEXT)

# ================== 🌐 FLASK (KEEP ALIVE) ==================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running ✅"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================== 🚀 MAIN ==================
async def main():
    print("⚡ System Is Active And Running...")

    await client.connect()

    if not await client.is_user_authorized():
        print("❌ Session not found. Run login.py locally first.")
        return

    print("🚀 Auto Reply Started Successfully...")

    await client.run_until_disconnected()

# ================== 🧵 THREAD START ==================
threading.Thread(target=run_web).start()

# ================== ▶️ RUN ==================
asyncio.run(main())