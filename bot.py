import telebot
from threading import Thread
import os, json, time, requests
from flask import Flask

TOKEN = "8276343460:AAENJ23ULVEqAnwxfHVY4vVvIWSkYTGDJ1E"  # توكن محمد
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# اوامر تطلع بالقائمة
try:
    bot.set_my_commands([
        telebot.types.BotCommand("add", "➕ اضافة حساب للفحص"),
        telebot.types.BotCommand("check", "🔍 فحص حساب هسه"),
        telebot.types.BotCommand("list", "📋 قائمة الحسابات"),
        telebot.types.BotCommand("start", "▶️ تشغيل البوت")
    ])
except:
    pass


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

WATCH_FILE = "watched.json"

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

def check_username(username):
    username = username.replace("@","").strip().split()[0]
    if not username:
        return None
    try:
        url = f"https://www.instagram.com/{username}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        text = r.text.lower()
        # انستا من يكون معطل يرجع 404 او صفحة فيها sorry
        if r.status_code == 404:
            return False  # معطل
        if "sorry, this page isn't available" in text or "الصفحة غير متوفرة" in text or "this page isn't available" in text:
            return False
        if r.status_code == 200 and f'"{username}"' in text or username.lower() in text:
            # اذا البروفايل يفتح يعني رجع
            return True
        # لو 200 بس ما متاكدين نعتبره رجع احتياطا اذا ما اكو sorry
        if r.status_code == 200:
            return True
        return False
    except Exception as e:
        print(f"check error {username}: {e}")
        return None

# اوامر الاضافة والفحص
@bot.message_handler(commands=['add','اضافة','ضيف'])
def add_user(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "دز اليوزر مثل: /add @يوزرك")
        return
    username = parts[1].replace("@","").strip()
    data = load_watched()
    data[username] = {"added_by": m.chat.id, "status": "معطل"}
    save_watched(data)
    bot.reply_to(m, f"✅ تمت اضافة @{username} للفحص
راح افحصه كل 30 دقيقة واذا رجع انطيك خبر.
تقدر تفحصه هسه بـ /check @{username}")

@bot.message_handler(commands=['check','فحص','فحصه'])
def check_user(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "دز اليوزر مثل: /check @يوزرك")
        return
    username = parts[1].replace("@","").strip()
    bot.reply_to(m, f"⏳ جاري فحص @{username} ...")
    result = check_username(username)
    if result is None:
        bot.send_message(m.chat.id, f"⚠️ ما كدرت افحص @{username} هسه، جرب بعد شوية")
    elif result == True:
        bot.send_message(m.chat.id, f"✅ رجع
@{username} رجع يشتغل هسه!
https://www.instagram.com/{username}/")
    else:
        bot.send_message(m.chat.id, f"❌ معطل
@{username} بعده معطل")

@bot.message_handler(commands=['list','القائمة'])
def list_users(m):
    data = load_watched()
    if not data:
        bot.reply_to(m, "ما عندك حسابات بالفحص")
        return
    txt = "📋 الحسابات بالفحص:\n"
    for u in data:
        txt += f"@{u}\n"
    bot.reply_to(m, txt)

# الرد العادي - الكليشة
@bot.message_handler(func=lambda m: True)
def all_messages(m):
    txt = m.text or ""
    # اذا بيه امر فحص لا ترد بالكليشة
    if txt.startswith("/"):
        return
    bot.reply_to(m, TEMPLATE)

# فحص دوري كل 30 دقيقة
def auto_checker():
    while True:
        time.sleep(1800)  # 30 دقيقة
        try:
            data = load_watched()
            if not data:
                continue
            for username, info in list(data.items()):
                result = check_username(username)
                if result == True:
                    # رجع!
                    chat_id = info.get("added_by")
                    if chat_id:
                        try:
                            bot.send_message(chat_id, f"✅ رجع
الحساب @{username} رجع يشتغل هسه! مبروك 🎉\nhttps://www.instagram.com/{username}/")
                        except:
                            pass
                    # احذفه من القائمة بعد ما رجع او خليه
                    # data.pop(username)
            # save_watched(data)
        except Exception as e:
            print(f"auto error: {e}")

Thread(target=run_flask, daemon=True).start()
Thread(target=auto_checker, daemon=True).start()
bot.infinity_polling(timeout=60, long_polling_timeout=60)
