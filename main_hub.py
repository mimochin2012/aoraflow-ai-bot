# main_hub.py - مع دعم UTF-8 كامل
import os
import json
import telebot
import time
from datetime import datetime
from graph import run_supervisor, run_supervisor_with_file

CONFIG_PATH = "Config/config.json"
TOKEN = "8653457473:AAHtOJ_FMXZ2OJRsD46Z6OU1QRXii5gyFtM"
ADMIN_ID = 8525611542

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    TOKEN = config.get("TELEGRAM_TOKEN", TOKEN)
    ADMIN_ID = config.get("ADMIN_ID", ADMIN_ID)

bot = telebot.TeleBot(TOKEN)

# تعيين الترميز الافتراضي لجميع الردود
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def log_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("Logs", exist_ok=True)
    with open(f"Logs/main_{datetime.now().strftime('%Y%m%d')}.log", 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {event}\n")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "⛔ هذا البوت مخصص للمدير فقط.")
        return
    welcome_msg = """👋 مرحباً أيها المدير!

نظام AoraFlow AI جاهز للعمل.

الأوامر المتاحة:
/status     - حالة النظام
/agents     - قائمة الموظفين الأذكياء
/clear      - مسح ذاكرة المحادثة
/chat [طلبك] - توجيه أمر للـ Agents

مثال: /chat أنشئ لي بوت حجوزات"""
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=['clear'])
def clear_memory(message):
    if message.chat.id != ADMIN_ID:
        return
    # حذف ذاكرة المستخدم من ملف user_memory.json
    mem_file = "user_memory.json"
    if os.path.exists(mem_file):
        with open(mem_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if str(message.chat.id) in data:
            del data[str(message.chat.id)]
            with open(mem_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        bot.reply_to(message, "✅ تم مسح ذاكرة المحادثة.")
    else:
        bot.reply_to(message, "✅ لا توجد ذاكرة محفوظة.")

@bot.message_handler(commands=['status'])
def status(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.reply_to(message, f"✅ النظام يعمل\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@bot.message_handler(commands=['agents'])
def list_agents(message):
    if message.chat.id != ADMIN_ID:
        return
    agents_list = """🧠 الـ Agents المتاحة:
1. 🤖 Bot Builder Agent
2. 📊 Data Analyst Agent
3. 👥 Sales Agent
4. 📢 Marketing Agent
5. 💼 Consulting Agent
6. 🛡️ Security Agent
7. 📋 CRM Agent
8. 📊 Report Agent
9. 💰 Payment Agent"""
    bot.reply_to(message, agents_list)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.chat.id != ADMIN_ID:
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in ['.csv', '.xlsx', '.xls']:
            bot.reply_to(message, "❌ نوع الملف غير مدعوم. أرسل CSV أو Excel فقط.")
            return
        uploads_dir = "Uploads"
        os.makedirs(uploads_dir, exist_ok=True)
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        bot.reply_to(message, f"📥 تم استلام: {file_name}\n🔄 جاري التحليل...")
        memory = {}  # سيتم تحميلها لاحقاً إذا أردت
        result = run_supervisor_with_file("تحليل هذا الملف", ADMIN_ID, file_path, file_name, memory)
        for msg in result.get("messages", []):
            if len(msg) > 4000:
                for i in range(0, len(msg), 4000):
                    bot.reply_to(message, msg[i:i+4000])
            else:
                bot.reply_to(message, msg)
        pdf_path = result.get("pdf_to_send")
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf_file:
                bot.send_document(message.chat.id, pdf_file, caption="📄 التقرير الكامل")
            os.remove(pdf_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)[:200]}")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if message.chat.id != ADMIN_ID:
        return
    user_input = message.text.strip()
    if not user_input:
        return
    bot.reply_to(message, "🔄 جاري التوجيه إلى المدير التنفيذي...")
    try:
        # تحميل ذاكرة المستخدم من ملف (اختياري)
        mem_file = "user_memory.json"
        memory = {}
        if os.path.exists(mem_file):
            with open(mem_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                memory = data.get(str(message.chat.id), {})
        result = run_supervisor(user_input, ADMIN_ID, memory)
        # حفظ الذاكرة المحدثة
        if result.get("memory"):
            if os.path.exists(mem_file):
                with open(mem_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
            data[str(message.chat.id)] = result["memory"]
            with open(mem_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        final_response = result.get("messages", ["حدث خطأ."])[-1]
        # إرسال الرد مع تجنب أخطاء الترميز
        try:
            bot.reply_to(message, final_response[:3000])
        except UnicodeEncodeError:
            # إذا فشل، حاول الترميز كـ UTF-8
            bot.reply_to(message, final_response[:3000].encode('utf-8', 'ignore').decode('utf-8'))
        # إرسال PDF إن وجد
        pdf_path = result.get("pdf_to_send")
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf_file:
                bot.send_document(message.chat.id, pdf_file, caption="📄 التقرير المرفق")
            os.remove(pdf_path)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)[:200]}")

print("🚀 AoraFlow AI CEO is running...")
log_event("تم تشغيل المدير التنفيذي")

# تم التعليق: التشغيل عبر webhook في main.py

