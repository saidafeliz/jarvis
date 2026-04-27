import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = 36011625
API_HASH = "4241f5c811609c083ef6a75647c1037f"
PHONE = "+998998250055"

async def main():
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start(phone=PHONE)
    session_str = client.session.save()
    with open("session_string.txt", "w", encoding="utf-8") as f:
        f.write(session_str)
    print("SESSION SAVED TO FILE")

asyncio.run(main())
