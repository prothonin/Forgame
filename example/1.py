import asyncio
from telethon import TelegramClient, events, Button

# ================= CONFIG =================
API_ID = 22071176
API_HASH = "7ed5401b625a0a4d3c45caf12c87f166"
BOT_TOKEN = "7402879073:AAFmS3FxnAMRDCdScW76TD9nwt19pXAIooQ"
AUTHORIZED_PARENT_IDS = {8032922682}  # your Telegram ID
# =========================================

client = TelegramClient('parent_session', API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        await event.respond("Unauthorized sender.")
        return

    text = (event.raw_text or "").strip().lower()
    if text == "/start":
        await event.respond(
            "Parent bot online. Waiting for child device.",
            buttons=[
                [Button.inline("Get Images", b"get_images")],
                [Button.inline("Get Videos", b"get_videos")]
            ]
        )

@client.on(events.CallbackQuery)
async def callback(event):
    if event.sender_id not in AUTHORIZED_PARENT_IDS:
        return

    if event.data == b"get_images":
        await event.answer("Command sent: get images ✅")
        # Here you can trigger your child script to send images

    elif event.data == b"get_videos":
        await event.answer("Command sent: get videos ✅")
        # Trigger your child script to send videos

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Parent bot started and listening...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
