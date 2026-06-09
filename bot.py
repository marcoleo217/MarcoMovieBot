import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN   = os.environ["BOT_TOKEN"]
CHANNEL_ID  = os.environ["CHANNEL_ID"]
LAST_MSG_ID = int(os.environ.get("LAST_MSG_ID", "100"))


async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result.new_chat_member.status == "member":
        user = result.new_chat_member.user
        name = user.first_name or "ဧည့်သည်တော်"
        text = (
            f"🎬 မင်္ဂလာပါ {name} !\n\n"
            f"ကျွန်တော်တို့ Movie Channel မှ ကြိုဆိုပါတယ် 🙏\n\n"
            f"📌 ဇာတ်ကားရှာနည်း\n"
            f"ဇာတ်ကားအမည် ရိုက်ထည့်လိုက်ရင် ချက်ချင်းပေးပါမယ်\n\n"
            f"ဥပမာ — Avatar လို့ ရိုက်ကြည့်ပါ 🎥"
        )
        await context.bot.send_message(chat_id=result.chat.id, text=text)


async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()
    if not query or query.startswith("/"):
        return

    await update.message.reply_text("🔍 ရှာနေပါတယ်၊ ခဏစောင့်ပါ...")

    found_msgs = []
    scan_range = range(max(1, LAST_MSG_ID - 300), LAST_MSG_ID + 1)

    for msg_id in scan_range:
        try:
            fwd = await context.bot.forward_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id,
            )
            caption = (fwd.caption or fwd.text or "").lower()
            if query in caption:
                found_msgs.append(fwd)
            else:
                await fwd.delete()
        except Exception:
            continue

    if found_msgs:
        await update.message.reply_text(
            f"✅ '{update.message.text}' — {len(found_msgs)} ကား တွေ့ပါတယ် 🎬"
        )
    else:
        await update.message.reply_text(
            f"😔 '{update.message.text}' မရှိသေးပါဘူး\n\n"
            f"မကြာမီ တင်ပေးပါမယ် 🔔"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Movie Bot မှ ကြိုဆိုပါတယ်!\n\n"
        "ရှာချင်တဲ့ ဇာတ်ကားအမည် ရိုက်ထည့်လိုက်ပါ 👇"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    print("🤖 Bot စတင်နေပါပြီ...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
