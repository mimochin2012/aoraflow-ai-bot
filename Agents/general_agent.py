# Agents/general_agent.py - يستخدم OpenRouter API (مجاني)
import os
import requests
import re

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "YOUR_FREE_KEY_HERE")  # ستحصل على مفتاح مجاني من openrouter.ai
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def detect_language(text):
    if re.search(r'[ابتثجحخدذرزسشصضطظعغفقكلمنهوي]', text):
        return "ar"
    if re.search(r'[éèêëàâçôûïîœ]', text.lower()):
        return "fr"
    return "en"

def call_openrouter(prompt, lang):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        # استخدام نموذج مجاني
        data = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }
        resp = requests.post(OPENROUTER_URL, json=data, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ خطأ API: {resp.status_code}"
    except Exception as e:
        return f"⚠️ فشل الاتصال بالذكاء الاصطناعي: {str(e)[:100]}"

def general_agent(state):
    print("💬 General Agent (AI via OpenRouter) يعمل...")
    user_msg = state["messages"][-1]
    lang = detect_language(user_msg)

    if lang == "ar":
        prompt = f"""أنت مساعد ذكي لنظام AoraFlow AI، وهو منصة متكاملة تقدم خدمات:
- تحليل البيانات وإنشاء تقارير PDF
- إنشاء بوتات تليجرام تفاعلية
- استشارات ذكاء اصطناعي
- دفع بالعملات الرقمية (USDT/PayPal)
- تسويق وترويج رقمي
- إدارة العملاء (CRM)
- تقارير أداء وأمان

المستخدم يسأل: {user_msg}

قم بالرد بشكل مفيد ومختصر، في حدود خدمات AoraFlow AI فقط. إذا كان السؤال خارج هذه الخدمات، قل بلطف أنك متخصص فقط في خدمات AoraFlow AI.
"""
    elif lang == "fr":
        prompt = f"""Vous êtes un assistant intelligent pour AoraFlow AI... (contenu similaire en français) ... L'utilisateur demande: {user_msg}"""
    else:
        prompt = f"""You are an intelligent assistant for AoraFlow AI... User asks: {user_msg}"""

    ai_response = call_openrouter(prompt, lang)
    state["messages"].append(ai_response)
    return state
