import telebot
from threading import Thread
import os

# التوكن - اخذته من اللي دزيته
TOKEN = os.environ.get("BOT_TOKEN", "9000239411:AAGPt7XTL1T58qOmkA5ReqfF7x7zk_8bQMM")

bot = telebot.TeleBot(TOKEN)

# ===== كودك القديم - فك حظر IP =====
@bot.message_handler(commands=['ipbypass'])
def ipbypass(m):
    bot.reply_to(m, "📱 فك حظر IP: وضع طيران 10ث - مسح بيانات انستا - شغل WARP - Proton VPN - اطعن من متصفح خفي)")

# ===== الكود الجديد الي طلبته - رد على كل كلمة =====

# 1- اذا كتب هلا / سلام / مرحبا
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower() in ['هلا', 'هلو', 'هلا والله', 'سلام', 'السلام عليكم', 'سلام عليكم', 'مرحبا', 'مرحببا'])
def hla_reply(m):
    bot.reply_to(m, "هلا بيك حبيبي انتظر بين ما يجي محمد يجاوبك ❤️")

# 2- اذا كتب شلونك / شخبارك
@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ['شلونك', 'شخبارك', 'شكو ماكو', 'شلون']))
def shlonak_reply(m):
    bot.reply_to(m, "بخير حبيبي انت شلونك؟ انتظر محمد هسه يجي يجاوبك")

# 3- اذا كتب حسابي معطل / استرجاع / disabled
@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ['معطل', 'حسابي معطل', 'انستا معطل', 'disabled', 'استرجاع', 'مسروق']))
def disabled_reply(m):
    text = """عندك موثق؟ دز يوزر + ايميل + رقم فقط

ما عندك موثق؟ انتظر سراك وخلي معلوماتك هنا من يوصلك سراك اقدملك:

Disabled Instagram Username: @يوزرك
Instagram Profile: https://www.instagram.com/يوزرك
Email: الايميل
Phone number: +964 كمل رقمك"""
    bot.reply_to(m, text)

# 4- اي شي ثاني
@bot.message_handler(func=lambda m: True)
def general_reply(m):
    txt = m.text.lower() if m.text else ""
    if any(x in txt for x in ['هلا', 'هلو', 'سلام', 'مرحبا', 'شلونك', 'شخبارك', 'معطل', 'disabled', 'استرجاع', 'مسروق', 'ipbypass']):
        return
    bot.reply_to(m, "تمام حبيبي خلي معلوماتك هنا ومحمد من يجي يجاوبك مباشر")

print("اهلا بيك ببوت محمد صباح - البوت شغال بالتوكن...")

bot.infinity_polling(timeout=60, long_polling_timeout=60)
