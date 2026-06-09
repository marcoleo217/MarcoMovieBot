import os
from pyrogram import Client, filters

# Render ရဲ့ Environment Variable ထဲကနေ တန်ဖိုးတွေကို ခေါ်ယူခြင်း
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

# Bot ကို စတင်ခြင်း
app = Client("MarcoBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("မင်္ဂလာပါ! ကျွန်တော် အဆင်သင့်ဖြစ်နေပါပြီ။")

# ဒီနေရာမှာ Bot စတင်လည်ပတ်ပါမယ်
if __name__ == "__main__":
    app.run()
