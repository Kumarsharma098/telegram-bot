import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import *

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = [
    "@MainChannel",
    "@NetflixCity",
    "@PremiumCity"
]

def start(update, context):
    text = "👋 Welcome!\n\n👇 Please join all channels:\n"
    for ch in CHANNELS:
        text += f"➡️ {ch}\n"

    btn = [[InlineKeyboardButton("✅ JOINED", callback_data="check")]]
    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(btn))

def check(update, context):
    q = update.callback_query
    bot = context.bot
    user = q.from_user.id

    for ch in CHANNELS:
        try:
            st = bot.get_chat_member(ch, user).status
            if st in ["left", "kicked"]:
                q.edit_message_text("❌ Join all channels!")
                return
        except:
            q.edit_message_text("⚠ Bot ko channel me admin banao!")
            return

    btn = [[InlineKeyboardButton("📱 Mobile Tracker", callback_data="track")]]
    q.edit_message_text("✔ Verified!\n👇 Choose:", reply_markup=InlineKeyboardMarkup(btn))

def track_menu(update, context):
    q = update.callback_query
    q.edit_message_text("📞 Send 10 digit mobile number:")
    context.user_data["await"] = True

def handle(update, context):
    if context.user_data.get("await"):
        num = update.message.text.strip()
        if not num.isdigit() or len(num) != 10:
            update.message.reply_text("❌ Valid 10 digit number bhejo.")
            return

        update.message.reply_text("⏳ Searching...")

        url = f"https://splexxo-bhai.vercel.app/api/seller?mobile={num}&key=SPLEXXO"
        try:
            data = requests.get(url).json().get("data")
            if not data:
                update.message.reply_text("❌ No info found!")
                return

            msg = "📱 Information:\n\n"
            for k, v in data.items():
                if v and v != "N/A" and v != "null":
                    msg += f"• {k.upper()}: {v}\n"

            update.message.reply_text(msg)

        except Exception as e:
            update.message.reply_text("⚠ Error: " + str(e))

        context.user_data["await"] = False

up = Updater(BOT_TOKEN, use_context=True)
dp = up.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(check, pattern="check"))
dp.add_handler(CallbackQueryHandler(track_menu, pattern="track"))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))

up.start_polling()
up.idle()
