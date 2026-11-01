import telebot
from threading import Thread
import os
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "8276343460:AAENJ23ULVEqAnwxfHVY4vVvIWSkYTGDJ1E")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "بوت محمد صباح شغال 24 ساعة"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(commands=['ipbypass'])
def ipbypass(m):
    bot.reply_to(m, "📱 فك حظر IP: وضع طيران 10ث - مسح بيانات انستا - شغل WARP - Proton VPN - اطعن من متصفح خفي)")

@bot.message_handler(func=lambda m: m.text and m.text.strip().lower() in ['هلا', 'هلو', 'هلا والله', 'سلام', 'السلام عليكم', 'سلام عليكم', 'مرحبا', 'مرحببا'])
def hla_reply(m):
    bot.reply_to(m, "هلا بيك حبيبي انتظر بين ما يجي محمد يجاوبك ❤️")

@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ['شلونك', 'شخبارك', 'شكو ماكو', 'شلون']))
def shlonak_reply(m):
    bot.reply_to(m, "بخير حبيبي انت شلونك؟ انتظر محمد هسه يجي يجاوبك")

@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ['معطل', 'حسابي معطل', 'انستا معطل', 'disabled', 'استرجاع', 'مسروق']))
def disabled_reply(m):
    text = """عندك موثق؟ دز يوزر + ايميل + رقم فقط

ما عندك موثق؟ انتظر سراك وخلي معلوماتك هنا من يوصلك سراك اقدملك:

Disabled Instagram Username: @يوزرك
Instagram Profile: https://www.instagram.com/يوزرك
Email: الايميل
Phone number: +964 كمل رقمك"""
    bot.reply_to(m, text)

@bot.message_handler(func=lambda m: True)
def general_reply(m):
    txt = m.text.lower() if m.text else ""
    if any(x in txt for x in ['هلا', 'هلو', 'سلام', 'مرحبا', 'شلونك', 'شخبارك', 'معطل', 'disabled', 'استرجاع', 'مسروق', 'ipbypass']):
        return
    bot.reply_to(m, "تمام حبيبي خلي معلوماتك هنا ومحمد من يجي يجاوبك مباشر")

Thread(target=run_flask, daemon=True).start()
bot.infinity_polling(timeout=60, long_polling_timeout=60)
