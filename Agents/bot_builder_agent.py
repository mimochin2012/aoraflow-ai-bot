# Agents/bot_builder_agent.py - نسخة متعددة اللغات (عربي/إنجليزي/فرنسي)
import os
from datetime import datetime

def detect_language(text):
    """اكتشاف اللغة: عربي، إنجليزي، فرنسي"""
    if not text:
        return "en"
    # فحص العربية
    if any(c in text for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"):
        return "ar"
    # فحص الفرنسية
    if any(c in text.lower() for c in "éèêëàâçôûïîœ"):
        return "fr"
    return "en"

def get_text(lang, key):
    """الحصول على النص حسب اللغة"""
    texts = {
        # العربية
        "ar": {
            "welcome": "🤖 **إنشاء بوت تليجرام جديد**\n\n📝 **الخطوة 1 من 3**\n\nما هو **اسم البوت** الذي تريد إنشاؤه؟\n\n(مثال: بوت_تذكيرات, عيادة_أسنان, بوت_خدمات)\n\n📌 *سيتم استخدام هذا الاسم للملف وللبوت نفسه*",
            "name_saved": "✅ **تم حفظ الاسم:** {name}\n\n📝 **الخطوة 2 من 3**\n\nماذا يفعل هذا البوت؟ (صف مهامه بالتفصيل)\n\n**اكتب وصفاً لمهام البوت:**",
            "tasks_saved": "✅ **تم حفظ المهام**\n\n📝 **الخطوة 3 من 3**\n\nالآن، أرسل **توكن البوت** من @BotFather.\n\n🔑 **كيف تحصل على التوكن:**\n1. اذهب إلى @BotFather في تليجرام\n2. أرسل `/newbot`\n3. اختر اسماً للبوت\n4. انسخ التوكن الذي سيرسله لك\n\n📌 **أرسل التوكن الآن:**",
            "bot_created": "✅ **تم إنشاء البوت بنجاح!**\n\n📌 **الاسم:** {name}\n📁 **الملف:** `Bots/{safe_name}.py`\n\n**📋 الخطوات التالية:**\n1. ✅ تم وضع التوكن تلقائياً\n2. شغّل البوت:\n   ```\n   C:\\Python314\\python.exe Bots/{safe_name}.py\n   ```\n3. اختبره في تليجرام\n\n🔁 لإنشاء بوت آخر، أرسل: `أنشئ لي بوت`",
            "start": "🤖 **إنشاء بوت تليجرام**\n\nلإنشاء بوت جديد، أرسل:\n`أنشئ لي بوت`\n\nسأقوم بمساعدتك خطوة بخطوة",
        },
        # الإنجليزية
        "en": {
            "welcome": "🤖 **Create a New Telegram Bot**\n\n📝 **Step 1 of 3**\n\nWhat is the **bot name** you want to create?\n\n(Example: reminder_bot, dental_clinic, service_bot)\n\n📌 *This name will be used for the file and the bot itself*",
            "name_saved": "✅ **Name saved:** {name}\n\n📝 **Step 2 of 3**\n\nWhat does this bot do? (Describe its tasks in detail)\n\n**Write the bot's description:**",
            "tasks_saved": "✅ **Tasks saved**\n\n📝 **Step 3 of 3**\n\nNow, send the **bot token** from @BotFather.\n\n🔑 **How to get the token:**\n1. Go to @BotFather on Telegram\n2. Send `/newbot`\n3. Choose a name for your bot\n4. Copy the token he sends you\n\n📌 **Send the token now:**",
            "bot_created": "✅ **Bot created successfully!**\n\n📌 **Name:** {name}\n📁 **File:** `Bots/{safe_name}.py`\n\n**📋 Next steps:**\n1. ✅ Token automatically added\n2. Run the bot:\n   ```\n   C:\\Python314\\python.exe Bots/{safe_name}.py\n   ```\n3. Test it on Telegram\n\n🔄 To create another bot, send: `create a bot`",
            "start": "🤖 **Create a Telegram Bot**\n\nTo create a new bot, send:\n`create a bot`\n\nI will help you step by step",
        },
        # الفرنسية
        "fr": {
            "welcome": "🤖 **Créer un nouveau bot Telegram**\n\n📝 **Étape 1 sur 3**\n\nQuel est le **nom du bot** que vous souhaitez créer ?\n\n(Exemple: bot_rappel, clinique_dentaire, bot_service)\n\n📌 *Ce nom sera utilisé pour le fichier et le bot lui-même*",
            "name_saved": "✅ **Nom enregistré:** {name}\n\n📝 **Étape 2 sur 3**\n\nQue fait ce bot ? (Décrivez ses tâches en détail)\n\n**Écrivez la description du bot :**",
            "tasks_saved": "✅ **Tâches enregistrées**\n\n📝 **Étape 3 sur 3**\n\nMaintenant, envoyez le **token du bot** depuis @BotFather.\n\n🔑 **Comment obtenir le token :**\n1. Allez sur @BotFather sur Telegram\n2. Envoyez `/newbot`\n3. Choisissez un nom pour votre bot\n4. Copiez le token qu'il vous envoie\n\n📌 **Envoyez le token maintenant :**",
            "bot_created": "✅ **Bot créé avec succès !**\n\n📌 **Nom:** {name}\n📁 **Fichier:** `Bots/{safe_name}.py`\n\n**📋 Prochaines étapes :**\n1. ✅ Token ajouté automatiquement\n2. Exécutez le bot :\n   ```\n   C:\\Python314\\python.exe Bots/{safe_name}.py\n   ```\n3. Testez-le sur Telegram\n\n🔄 Pour créer un autre bot, envoyez : `créer un bot`",
            "start": "🤖 **Créer un bot Telegram**\n\nPour créer un nouveau bot, envoyez :\n`créer un bot`\n\nJe vais vous aider étape par étape",
        }
    }
    return texts.get(lang, texts["en"]).get(key, "")

def bot_builder_agent(state):
    print("🤖 Bot Builder Agent (Multi-lang) يعمل...")
    
    last_msg = state["messages"][-1]
    lang = detect_language(last_msg)
    memory = state.get("memory", {})
    step = memory.get("step", "asking_name")
    
    # ========== الخطوة 1: سؤال الاسم ==========
    if step == "asking_name":
        if any(word in last_msg.lower() for word in ["بوت", "bot", "create", "انشاء", "créer", "nouveau"]):
            response = get_text(lang, "welcome")
            memory["step"] = "asking_tasks"
            state["memory"] = memory
            state["messages"].append(response)
            return state
        else:
            state["messages"].append(get_text(lang, "start"))
            return state
    
    # ========== الخطوة 2: سؤال المهام ==========
    if step == "asking_tasks":
        bot_name = last_msg.strip()
        safe_name = bot_name.replace(" ", "_").replace("-", "_").lower()
        memory["bot_name"] = bot_name
        memory["safe_name"] = safe_name
        
        response = get_text(lang, "name_saved").format(name=bot_name)
        memory["step"] = "asking_token"
        state["memory"] = memory
        state["messages"].append(response)
        return state
    
    # ========== الخطوة 3: سؤال التوكن ==========
    if step == "asking_token":
        tasks = last_msg.strip()
        memory["bot_tasks"] = tasks
        
        response = get_text(lang, "tasks_saved")
        memory["step"] = "creating_bot"
        state["memory"] = memory
        state["messages"].append(response)
        return state
    
    # ========== الخطوة 4: إنشاء البوت ==========
    if step == "creating_bot":
        token = last_msg.strip()
        bot_name = memory.get("bot_name", "AoraFlowBot")
        safe_name = memory.get("safe_name", "aoraflowbot")
        tasks = memory.get("bot_tasks", "")
        
        # كود البوت (نص إنجليزي لتجنب مشاكل الترميز)
        bot_code = f'''# -*- coding: utf-8 -*-
"""
AoraFlow Generated Bot: {bot_name}
Tasks: {tasks[:200]}
"""

import requests
import time

TOKEN = "{token}"

def send_message(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{{TOKEN}}/sendMessage"
        payload = {{"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error: {{e}}")

def handle_message(text):
    text = text.lower()
    if text == "/start":
        return "👋 Hello! I am {bot_name}\\n\\n{tasks[:200]}"
    elif text == "/help":
        return "📋 Available commands:\\n/start - Welcome\\n/help - Help"
    else:
        return "✅ Request received."

def main():
    print(f"🚀 {bot_name} is running...")
    last_update = 0
    url = f"https://api.telegram.org/bot{{TOKEN}}/getUpdates"
    
    while True:
        try:
            r = requests.get(url, params={{"offset": last_update + 1, "timeout": 30}}, timeout=35)
            data = r.json()
            for update in data.get("result", []):
                last_update = update["update_id"]
                msg = update.get("message")
                if msg and msg.get("text"):
                    chat_id = msg["chat"]["id"]
                    user_text = msg["text"]
                    reply = handle_message(user_text)
                    send_message(chat_id, reply)
        except Exception as e:
            print(f"Error: {{e}}")
            time.sleep(5)

if __name__ == "__main__":
    main()
'''

        bots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Bots")
        os.makedirs(bots_dir, exist_ok=True)
        file_path = os.path.join(bots_dir, f"{safe_name}.py")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(bot_code)
        
        response = get_text(lang, "bot_created").format(name=bot_name, safe_name=safe_name)
        
        # تنظيف الذاكرة
        state["memory"] = {}
        state["messages"].append(response)
        return state
    
    # رد افتراضي
    response = get_text(lang, "start")
    state["messages"].append(response)
    return state
