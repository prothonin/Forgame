# parent.py
from telethon import TelegramClient, events
import os

API_ID = 22071176
API_HASH = "7ed5401b625a0a4d3c45caf12c87f166"
BOT_TOKEN = "8361124114:AAEtfKO6fvehW-207xoCMcVKmWsU6oWI_8E"
AUTHORIZED_PARENT_IDS = {8032922682}  # your Telegram user id

client = TelegramClient('parent_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        await event.respond("Unauthorized sender.")
        return

    text = (event.raw_text or "").strip().lower()

    if text == "!start":
        await event.respond("Parent bot online. Commands: !share_images")
        return

    if text == "!share_images":
        # forward this command to child bot (child.py) somehow
        await event.respond("Command sent to child agent (via Telegram).")
        return

client.run_until_disconnected()
