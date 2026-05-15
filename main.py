# main.py - لـ Render (webhook باستخدام python-telegram-bot)
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from graph import run_supervisor

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8080))

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    await update.message.reply_text("👋 مرحباً بك في AoraFlow AI!\nأرسل /help للمساعدة.")

async def help_command(update: Update, context):
    help_text = """📋 **الأوامر المتاحة:**
/start - الترحيب
/help - هذه المساعدة
/status - حالة النظام
/agents - قائمة الـ Agents

📌 يمكنك أيضاً إرسال:
• ملف CSV/Excel للتحليل
• `أنشئ لي بوت` لإنشاء بوت جديد
• `استشارة: ...` للحصول على استشارة
• `ابحث عن ...` للبحث
• `/pay` لعرض طرق الدفع"""
    await update.message.reply_text(help_text)

async def status(update: Update, context):
    await update.message.reply_text("✅ النظام يعمل بشكل طبيعي.")

async def agents(update: Update, context):
    agents_list = """🧠 الـ Agents المتاحة:
1. 🤖 Bot Builder
2. 📊 Data Analyst
3. 👥 Sales
4. 📢 Marketing
5. 💼 Consulting
6. 🛡️ Security
7. 📋 CRM
8. 📊 Report
9. 💰 Payment
10. 🌐 Web (تجريبي)
11. 💬 General (AI)"""
    await update.message.reply_text(agents_list)

async def handle_message(update: Update, context):
    user_id = update.effective_user.id
    user_input = update.message.text
    result = run_supervisor(user_input, user_id)
    response = result.get("messages", ["حدث خطأ."])[-1]
    await update.message.reply_text(response[:4000])

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("agents", agents))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_webhook(listen="0.0.0.0", port=PORT, url_path=TELEGRAM_TOKEN, webhook_url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")

if __name__ == "__main__":
    main()
