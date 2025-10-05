import asyncio
from telethon import TelegramClient, events

# ================= CONFIG =================
API_ID = 22071176                      # your Telegram API ID (from my.telegram.org)
API_HASH = "7ed5401b625a0a4d3c45caf12c87f166"  # your API HASH
BOT_TOKEN = "7402879073:AAFmS3FxnAMRDCdScW76TD9nwt19pXAIooQ"  # new bot token
AUTHORIZED_PARENT_IDS = {8032922682}  # your Telegram user ID
# =========================================

client = TelegramClient('parent_session', API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    print("Received:", event.sender_id, event.raw_text)
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        await event.respond("Unauthorized sender.")
        return

    text = (event.raw_text or "").strip().lower()
    if text == "/start":
        await event.respond("Parent bot online. Waiting for child device.")
    elif text == "!share_images":
        await event.respond("Command will be sent to child agent (once connected).")

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Parent bot started and listening...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
