# parent.py
from telethon import TelegramClient, events, Button

API_ID = 22071176
API_HASH = "7ed5401b625a0a4d3c45caf12c87f166"
BOT_TOKEN = "8361124114:AAEtfKO6fvehW-207xoCMcVKmWsU6oWI_8E"
AUTHORIZED_PARENT_IDS = {8032922682}  # your Telegram user ID

client = TelegramClient('parent_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Only respond to your messages (parent ID)
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        await event.respond("Unauthorized sender.")
        return

    text = (event.raw_text or "").strip().lower()
    if text == "!start":
        await event.respond("Parent bot online. Waiting for child device.")
        return

    # The child will send "Device connected" message automatically with a button

@client.on(events.CallbackQuery)
async def callback(event):
    # Parent can click button, which is handled by child
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        return
    # just acknowledge the click
    await event.answer("Button clicked — command sent to child.")

client.run_until_disconnected()
