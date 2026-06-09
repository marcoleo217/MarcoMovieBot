import os
from pyrogram import Client, filters

# Render settings ထဲမှာ ထည့်ထားတဲ့ variables တွေကို ခေါ်သုံးတာပါ
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("MyMovieBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Bot is online and working!")

if __name__ == "__main__":
    app.run()
