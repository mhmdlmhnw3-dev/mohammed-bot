import telebot
from threading import Thread
import os, json, time, requests
from datetime import datetime
from flask import Flask

TOKEN = "8276343460:AAENJ23ULVEqAnwxfHVY4vVvIWSkYTGDJ1E"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Unban Monitor Bot Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

WATCH_FILE = "watched.json"

TEMPLATE = """Disabled Instagram Username: @يوزرك
Instagram Profile: https://www.instagram/يوزرك
Email: الايميل
phone number:+964كمل رقمك
ماعندك موثق انتظر سراك خلي معلوماتك هنا واجيكم واحد واحد ب سره"""

def load_watched():
    if not os.path.exists(WATCH_FILE):
        return {}
    try:
        with open(WATCH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_watched(data):
    with open(WATCH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_username_available(username):
    """يرجع True اذا اليوزر متاح (مثل Unban Monitor) False اذا بعده محجوز/معطل"""
    username = username.replace("@","").strip()
    if not username:
        return None
    try:
        url = f"https://www.instagram.com/{username}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html"
        }
        r = requests.get(url, headers=headers, timeout=15)
        text = r.text.lower()
        # اذا 404 او صفحة Sorry يعني متاح
        if r.status_code == 404:
            return True  # متاح مثل Unban Monitor
        if "sorry, this page isn't available" in text:
            return True  # متاح
        if r.status_code == 200:
            return False  # بعده محجوز/معطل
        return False
    except Exception as e:
        print(f"check error {username}: {e}")
        return None

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"🔥 Unban Monitor Bot\n\n{TEMPLATE}\n\n📋 الاوامر:\n/add @يوزر - مراقبة\n/check @يوزر - فحص فوري\n/list - القائمة")

@bot.message_handler(commands=['add','ضيف','اضافة'])
def add_user(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "مثال: /add @k6ux")
        return
    username = parts[1].replace("@","").strip()
    data = load_watched()
    data[username] = {
        "added_by": m.chat.id,
        "added_at": datetime.now().isoformat(),
        "status": "watching"
    }
    save_watched(data)
    bot.reply_to(m, f"✅ تمت اضافة @{username} للمراقبة\nراح ابلغك من يصير متاح مثل Unban Monitor")

@bot.message_handler(commands=['check','فحص','فحصه'])
def check_user(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "مثال: /check @k6ux")
        return
    username = parts[1].replace("@","").strip()
    bot.reply_to(m, f"⏳ جاري فحص @{username}...")
    res = check_username_available(username)
    now_str = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
    if res is None:
        bot.send_message(m.chat.id, f"⚠️ ما كدرت افحص @{username} هسه")
    elif res == True:
        # مثل صيغة Unban Monitor بالصورة
        bot.send_message(m.chat.id, f"You can use @{username} again\nTAT: 0h 0m\nTime: {now_str}\nBy: @{bot.get_me().username}")
    else:
        bot.send_message(m.chat.id, f"❌ @{username} بعده معطل/محجوز\nTime: {now_str}")

@bot.message_handler(commands=['list','القائمة'])
def list_users(m):
    data = load_watched()
    if not data:
        bot.reply_to(m, "ما عندك يوزرات بالمراقبة")
        return
    txt = "📋 قائمة المراقبة (مثل Unban Monitor):\n"
    for u in data:
        txt += f"@{u}\n"
    bot.reply_to(m, txt)

@bot.message_handler(func=lambda m: True)
def all_messages(m):
    if m.text and m.text.startswith('/'):
        return
    bot.reply_to(m, TEMPLATE)

def auto_checker():
    """يفحص كل 2 دقيقة مثل قناة Unban Monitor"""
    while True:
        time.sleep(120)
        try:
            data = load_watched()
            if not data:
                continue
            for username, info in list(data.items()):
                res = check_username_available(username)
                if res == True:  # صار متاح!
                    chat_id = info.get("added_by")
                    if chat_id:
                        now_str = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
                        try:
                            bot.send_message(chat_id, f"You can use @{username} again\nTAT: -\nTime: {now_str}\nBy: @{bot.get_me().username}")
                        except:
                            pass
                        # احذفه بعد ما بلغ
                        data.pop(username, None)
                        save_watched(data)
        except Exception as e:
            print(f"auto error: {e}")

Thread(target=run_flask, daemon=True).start()
Thread(target=auto_checker, daemon=True).start()
bot.infinity_polling()
