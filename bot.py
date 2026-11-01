import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

WELCOME = """هلا بيك حبيبي انا بوت محمد صباح
اكتبلي شنو تحتاج:
- الاسعار
- التوصيل
- التواصل
"""

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    
    if "/start" in text:
        await update.message.reply_text(WELCOME)
    elif "سلام" in text or "هلا" in text or "مرحبا" in text:
        await update.message.reply_text("وعليكم السلام حبيبي محمد صباح يرحب بيك شلون اكدر اساعدك؟")
    elif "سعر" in text or "بشكد" in text:
        await update.message.reply_text("تدلل، دزلي اسم المنتج او الخدمة وانطيك السعر بالتفصيل")
    elif "توصيل" in text:
        await update.message.reply_text("عندنا توصيل لكل محافظات العراق، كربلاء - بغداد - البصرة وكل مكان")
    elif "رقم" in text or "تواصل" in text:
        await update.message.reply_text("تكدر تتواصل وياي هنا مباشرة، او دزلي رقمك واتصل بيك")
    else:
        await update.message.reply_text(f"وصلتني: '{update.message.text}'\nاني بوت محمد صباح الذكي، راح ارد عليك قريبا. اكتب /start")

def main():
    if not TOKEN:
        print("ERROR: BOT_TOKEN not set")
        return
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, reply))
    print("Bot is running 24h...")
    app.run_polling()

if __name__ == "__main__":
    main()
