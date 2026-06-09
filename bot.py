import os
from pyrogram import Client, filters

# Environment Variables များ
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# Bot စတင်ခြင်း
app = Client("MarcoMovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply("မင်္ဂလာပါ! ကျွန်တော်က သင့်ရုပ်ရှင် Channel အတွက် အသင့်တော်ဆုံး Auto-Filter Bot ပါ။")

# ရုပ်ရှင်ရှာဖွေခြင်း (Auto-Filter)
@app.on_message(filters.text & ~filters.command(["start"]))
async def filter_handler(client, message):
    query = message.text
    # Channel ထဲက စာတွေကို ရှာဖွေခြင်း
    async for msg in client.search_messages(CHANNEL_ID, query=query):
        await client.copy_message(chat_id=message.chat.id, from_chat_id=CHANNEL_ID, message_id=msg.id)
        return
    await message.reply("တောင်းဆိုထားသော ရုပ်ရှင်အား မတွေ့ရှိပါ။")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
