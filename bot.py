import telebot
from threading import Thread
import os
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "8276343460:AAENJ23ULVEqAnwxfHVY4vVvIWSkYTGDJ1E")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

TEMPLATE = """Disabled Instagram Username: @يوزرك
Instagram Profile: https://www.instagram/يوزرك
Email: الايميل
phone number:+964كمل رقمك
ماعندك موثق انتظر سراك خلي معلوماتك هنا واجيكم واحد واحد ب سره"""

@bot.message_handler(func=lambda m: True)
def all_messages(m):
    bot.reply_to(m, TEMPLATE)

Thread(target=run_flask, daemon=True).start()
bot.infinity_polling(timeout=60, long_polling_timeout=60)
