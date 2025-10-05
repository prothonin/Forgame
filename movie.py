from telethon import TelegramClient
import asyncio

# Replace with your own API credentials
api_id = 22071176
api_hash = '7ed5401b625a0a4d3c45caf12c87f166'

channel = 'jsiciscjeici'
message_id = 3

client = TelegramClient('anon', api_id, api_hash)

async def main():
    await client.start()
    msg = await client.get_messages(channel, ids=message_id)
    
    if msg and msg.media:
        def progress(downloaded_bytes, total_bytes):
            percent = downloaded_bytes * 100 / total_bytes
            print(f"\rDownloaded: {percent:.2f}%", end='')

        path = await msg.download_media(
            file='movie.mp4',
            progress_callback=progress
        )
        print(f"\nDownload complete! Saved as: {path}")
    else:
        print("No media found in this post.")

asyncio.run(main())
