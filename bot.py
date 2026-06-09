import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    filters,
    ContextTypes,
)

# ─────────────────────────────────────────
# CONFIG — .env ဒါမှမဟုတ် Railway variables
# ─────────────────────────────────────────
BOT_TOKEN   = os.environ["BOT_TOKEN"]       # BotFather ကပေးတဲ့ token
CHANNEL_ID  = os.environ["CHANNEL_ID"]      # e.g. -1001234567890

# ─────────────────────────────────────────
# WELCOME MESSAGE
# ─────────────────────────────────────────
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Member အသစ် ဝင်လာရင် welcome ပေးတယ်"""
    result = update.chat_member
    if result.new_chat_member.status == "member":
        user = result.new_chat_member.user
        name = user.first_name or "ဧည့်သည်တော်"

        text = (
            f"🎬 မင်္ဂလာပါ {name} !\n\n"
            f"ကျွန်တော်တို့ Movie Channel မှ ကြိုဆိုပါတယ် 🙏\n\n"
            f"📌 ဇာတ်ကားရှာဖွေနည်း —\n"
            f"ဇာတ်ကားအမည် ရိုက်ထည့်လိုက်ရင် ချက်ချင်းပေးပါမယ်\n\n"
            f"ဥပမာ —  Avatar  လို့ ရိုက်ကြည့်ပါ 🎥"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Channel သွားကြည့်မယ်", url=f"https://t.me/{context.bot.username}")]
        ])

        await context.bot.send_message(
            chat_id=result.chat.id,
            text=text,
            reply_markup=keyboard
        )


# ─────────────────────────────────────────
# MOVIE SEARCH
# ─────────────────────────────────────────
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User ရိုက်တဲ့ movie name ကို channel မှာ ရှာပေးတယ်"""
    query = update.message.text.strip()

    if not query or query.startswith("/"):
        return

    await update.message.reply_text("🔍 ရှာနေပါတယ်၊ ခဏစောင့်ပါ...")

    found = []

    try:
        # Channel history မှ post ၂၀၀ ဆွဲယူပြီး ရှာတယ်
        async for message in context.bot.get_chat(CHANNEL_ID):
            break  # placeholder — offset loop အောက်မှာ

        # Telegram Bot API — channel post တွေ iterate လုပ်ဖို့
        # forwardFromChat နဲ့ getUpdates မသုံးဘဲ
        # stored message_id range နဲ့ ရှာတာ အကောင်းဆုံး

        offset = int(os.environ.get("LAST_MSG_ID", "1"))
        batch  = 200  # တစ်ခါ scan မည့် post အရေအတွက်

        for msg_id in range(max(1, offset - batch), offset + 1):
            try:
                msg = await context.bot.forward_message(
                    chat_id=update.message.chat_id,
                    from_chat_id=CHANNEL_ID,
                    message_id=msg_id,
                    disable_notification=True,
                )
                # caption ဒါမှမဟုတ် text မှာ query ပါရင်
                content = (msg.caption or msg.text or "").lower()
                if query.lower() in content:
                    found.append(msg)
                else:
                    # မတူရင် ဖျက်တယ် (forward ထားတာ clean လုပ်ဖို့)
                    await msg.delete()
            except Exception:
                continue  # message မရှိ / ဖျက်ထားပြီ ဆိုရင် skip

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
        return

    if found:
        await update.message.reply_text(
            f"✅ '{query}' အတွက် {len(found)} ကားတွေ့ပါတယ် 🎬\n"
            f"အပေါ်က forward လုပ်ပေးထားပါတယ်။"
        )
    else:
        await update.message.reply_text(
            f"😔 '{query}' မရှိသေးပါဘူး\n\n"
            f"📌 မကြာခင် တင်ပေးပါမယ် — Notification ဖွင့်ထားပါ 🔔"
        )


# ─────────────────────────────────────────
# /start command
# ─────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Movie Bot မှ ကြိုဆိုပါတယ်!\n\n"
        "ရှာချင်တဲ့ ဇာတ်ကားအမည် ရိုက်ထည့်လိုက်ပါ 👇"
    )


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))

    print("🤖 Bot စတင်နေပါပြီ...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
