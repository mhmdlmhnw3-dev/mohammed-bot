import telebot
from threading import Thread
import os
import requests
from flask import Flask

TOKEN = "8276343460:AAENJ23ULVEqAnwxfHVY4vVvIWSkYTGDJ1E"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running 24h"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

TEMPLATE = """Disabled Instagram Username: @يوزرك
Instagram Profile: https://www.instagram/يوزرك
Email: الايميل
phone number:+964كمل رقمك
ماعندك موثق انتظر سراك خلي معلوماتك هنا واجيكم واحد واحد ب سره"""

def check_username(username):
    username = username.replace("@","").strip()
    if not username:
        return None
    try:
        url = f"https://www.instagram.com/{username}/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url, headers=headers, timeout=10)
        txt = r.text.lower()
        if r.status_code == 404:
            return False
        if "sorry, this page isn't available" in txt or "this page isn't available" in txt:
            return False
        if r.status_code == 200:
            return True
        return False
    except:
        return None

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, TEMPLATE)

@bot.message_handler(commands=['add','ضيف','اضافة'])
def add(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "مثال: /add @يوزرك")
        return
    bot.reply_to(m, f"تمت اضافة @{parts[1].replace('@','')} للفحص - استخدم /check @{parts[1].replace('@','')}")

@bot.message_handler(commands=['check','فحص','فحصه'])
def check(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "مثال: /check @يوزرك")
        return
    username = parts[1].replace("@","").strip()
    bot.reply_to(m, f"⏳ جاري فحص @{username}...")
    res = check_username(username)
    if res is None:
        bot.send_message(m.chat.id, f"⚠️ ما كدرت افحص @{username}")
    elif res:
        bot.send_message(m.chat.id, f"✅ رجع\n@{username} رجع يشتغل!\nhttps://www.instagram.com/{username}/")
    else:
        bot.send_message(m.chat.id, f"❌ معطل\n@{username} بعده معطل")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    if m.text and m.text.startswith('/'):
        return
    bot.reply_to(m, TEMPLATE)

Thread(target=run_flask, daemon=True).start()
bot.infinity_polling()
