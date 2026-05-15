# Agents/marketing_agent.py - متخصص في الترويج لـ AoraFlow AI
import os
import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gpt-oss:20b-cloud"

def detect_language(text):
    if any(c in text for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"):
        return "ar"
    if any(c in text.lower() for c in "éèêëàâçôûïîœ"):
        return "fr"
    return "en"

def call_ollama(prompt):
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=60)
        return r.json().get("response", "لم أتمكن من إنشاء المحتوى.")
    except:
        return "⚠️ خطأ في الاتصال."

def marketing_agent(state):
    print("📢 Marketing Agent (AoraFlow AI) يعمل...")
    last_msg = state["messages"][-1]
    lang = detect_language(last_msg)
    u = last_msg.lower()

    # وصف خدمات AoraFlow AI (للاستخدام الداخلي)
    aoraflow_services = {
        "ar": "خدمات AoraFlow AI: تحليل البيانات مع تقارير PDF، إنشاء بوتات تليجرام تفاعلية، استشارات ذكاء اصطناعي، نظام دفع بالعملات الرقمية (USDT/PayPal)، تسويق ومبيعات، إدارة علاقات العملاء، تقارير أداء، أمان.",
        "en": "AoraFlow AI services: Data analysis with PDF reports, interactive Telegram bot creation, AI consulting, crypto payment system (USDT/PayPal), marketing & sales, CRM, performance reports, security.",
        "fr": "Services AoraFlow AI : analyse de données avec rapports PDF, création de bots Telegram interactifs, conseil en IA, système de paiement en cryptomonnaies (USDT/PayPal), marketing & ventes, CRM, rapports de performance, sécurité."
    }

    # إنشاء منشور ترويجي لـ AoraFlow AI
    if any(w in u for w in ["منشور", "post", "publication", "ترويج", "promote", "اعلان", "ad"]):
        prompt = f"""اكتب منشوراً تسويقياً قصيراً (لـ Telegram أو وسائل التواصل) يروّج لـ AoraFlow AI، وهو نظام ذكاء اصطناعي متكامل يقدم:
- تحليل البيانات وتقارير PDF
- إنشاء بوتات تليجرام تلقائياً
- استشارات ذكاء اصطناعي
- دفع بالعملات الرقمية (USDT/PayPal)
- إدارة العملاء والتقارير

المنشور يجب أن يكون جذاباً، موجزاً (أقل من 400 حرف)، ويحتوي على دعوة للتواصل مع البوت: @DataAnalyst_ai_bot
اللغة: {lang}"""
        post = call_ollama(prompt)
        response = f"📢 **منشور ترويجي لـ AoraFlow AI**\n\n{post}"
        state["messages"].append(response)
        return state

    # إنشاء خطة تسويقية لـ AoraFlow AI
    if any(w in u for w in ["خطة تسويقية", "marketing plan", "plan marketing", "استراتيجية", "strategy"]):
        prompt = f"""ضع خطة تسويقية شاملة لخدمة AoraFlow AI (نظام ذكاء اصطناعي ذاتي التشغيل عبر Telegram). اذكر:
- الجمهور المستهدف (رواد الأعمال، الشركات الصغيرة، المطورين).
- قنوات التسويق المقترحة (Telegram, Instagram, LinkedIn, إعلانات مدفوعة).
- محتوى مقترح (دروس، عروض، شهادات).
- جدول زمني (شهر واحد).
- ميزانية تقريبية (منخفضة، متوسطة).

اللغة: {lang}"""
        plan = call_ollama(prompt)
        response = f"📢 **الخطة التسويقية لـ AoraFlow AI**\n\n{plan}"
        state["messages"].append(response)
        return state

    # عرض فوائد AoraFlow AI
    if any(w in u for w in ["فوائد", "benefits", "avantages", "لماذا", "why"]):
        if lang == "ar":
            response = """✨ **لماذا تختار AoraFlow AI؟**

• 🚀 **تشغيل ذاتي 24/7** – يعمل بدون تدخل بشري.
• 📊 **تحليل فوري** للملفات مع تقارير PDF احترافية.
• 🤖 **إنشاء بوتات تليجرام** حسب طلبك (اسم ← مهام ← توكن).
• 💰 **دفع بالعملات الرقمية** (USDT, PayPal) – آمن وسريع.
• 🌐 **دعم متعدد اللغات** (عربي، إنجليزي، فرنسي).
• 🔒 **أمان وخصوصية** – بياناتك تبقى محلية.

جرب الآن: @DataAnalyst_ai_bot"""
        elif lang == "fr":
            response = """✨ **Pourquoi choisir AoraFlow AI ?**

• 🚀 **Fonctionnement autonome 24/7** – sans intervention humaine.
• 📊 **Analyse instantanée** de fichiers avec rapports PDF.
• 🤖 **Création de bots Telegram** à la demande.
• 💰 **Paiement en cryptomonnaies** (USDT, PayPal).
• 🌐 **Multilingue** (arabe, anglais, français).
• 🔒 **Sécurité et confidentialité** – données locales.

Essayez maintenant : @DataAnalyst_ai_bot"""
        else:
            response = """✨ **Why choose AoraFlow AI?**

• 🚀 **24/7 autonomous operation** – no human intervention.
• 📊 **Instant file analysis** with PDF reports.
• 🤖 **Telegram bot creation** on demand.
• 💰 **Cryptocurrency payments** (USDT, PayPal).
• 🌐 **Multi-language** (Arabic, English, French).
• 🔒 **Security & privacy** – local data.

Try now: @DataAnalyst_ai_bot"""
        state["messages"].append(response)
        return state

    # عرض الأسعار والخدمات
    if any(w in u for w in ["خدمات", "services", "prestations", "أسعار", "prices", "prix"]):
        if lang == "ar":
            response = """📋 **خدمات AoraFlow AI والأسعار (USDT/PayPal):**

• تحليل بيانات (PDF + توصيات): $29
• بوت تليجرام أساسي: $99
• بوت تليجرام متقدم: $249
• استشارة ذكاء اصطناعي (ساعة): $99
• اشتراك شهري (دعم وتحديثات): $49

للطلب أو الاستفسار: @DataAnalyst_ai_bot"""
        elif lang == "fr":
            response = """📋 **Services AoraFlow AI et prix (USDT/PayPal) :**

• Analyse de données (PDF + recommandations) : 29 $
• Bot Telegram de base : 99 $
• Bot Telegram avancé : 249 $
• Conseil en IA (1 heure) : 99 $
• Abonnement mensuel (support et mises à jour) : 49 $

Pour commander ou vous renseigner : @DataAnalyst_ai_bot"""
        else:
            response = """📋 **AoraFlow AI services and prices (USDT/PayPal):**

• Data analysis (PDF + insights): $29
• Basic Telegram bot: $99
• Advanced Telegram bot: $249
• AI consulting (1 hour): $99
• Monthly subscription (support & updates): $49

To order or inquire: @DataAnalyst_ai_bot"""
        state["messages"].append(response)
        return state

    # اقتراح فكرة تسويقية جديدة
    if any(w in u for w in ["فكرة", "idea", "idée", "اقتراح", "suggestion"]):
        prompt = f"""اقترح فكرة تسويقية مبتكرة للترويج لـ AoraFlow AI (نظام ذكاء اصطناعي عبر تليجرام). يجب أن تكون الفكرة منخفضة التكلفة وسهلة التنفيذ، مثل مسابقة، عرض مجاني، أو شراكة مع مؤثرين.
اللغة: {lang}"""
        idea = call_ollama(prompt)
        response = f"💡 **فكرة تسويقية لـ AoraFlow AI**\n\n{idea}"
        state["messages"].append(response)
        return state

    # رد المساعدة الافتراضي
    if lang == "ar":
        response = """📢 **مساعد التسويق والترويج لـ AoraFlow AI**

أستطيع مساعدتك في:
• إنشاء منشور ترويجي: `منشور`
• وضع خطة تسويقية: `خطة تسويقية`
• عرض فوائد النظام: `فوائد`
• عرض الخدمات والأسعار: `خدمات`
• اقتراح فكرة تسويقية: `فكرة`

كيف يمكنني الترويج لـ AoraFlow AI اليوم؟"""
    elif lang == "fr":
        response = """📢 **Assistant marketing et promotion pour AoraFlow AI**

Je peux vous aider à :
• Créer une publication promotionnelle : `publication`
• Élaborer un plan marketing : `plan marketing`
• Afficher les avantages : `avantages`
• Afficher les services et prix : `services`
• Proposer une idée marketing : `idée`

Comment puis-je promouvoir AoraFlow AI aujourd'hui ?"""
    else:
        response = """📢 **Marketing & Promotion Assistant for AoraFlow AI**

I can help you with:
• Create a promotional post: `post`
• Create a marketing plan: `marketing plan`
• Show benefits: `benefits`
• Show services and prices: `services`
• Suggest a marketing idea: `idea`

How can I promote AoraFlow AI today?"""
    state["messages"].append(response)
    return state
