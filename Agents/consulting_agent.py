# Agents/consulting_agent.py - إصدار نصي فقط (بدون PDF، مع حفظ txt)
import os
import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gpt-oss:120b-cloud"
CONSULTING_DIR = "Consulting"
os.makedirs(CONSULTING_DIR, exist_ok=True)

def detect_language(text):
    if any(c in text for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"):
        return "ar"
    return "en"

def call_ollama(prompt):
    try:
        payload = {"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.3, "num_predict": 1500}}
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        return r.json().get("response", "Unable to generate consultation.")
    except Exception as e:
        return f"Error: {str(e)[:100]}"

def consulting_agent(state):
    print("💼 Consulting Agent يعمل...")
    last_msg = state["messages"][-1]
    lang = detect_language(last_msg)
    user_id = state.get("user_id", "unknown")

    if any(w in last_msg.lower() for w in ["استشارة", "consulting", "نصيحة", "advice"]):
        if lang == "ar":
            prompt = f"""أنت خبير استشاري أعمال وتقني. قدم استشارة احترافية باللغة العربية مفصلة.

طلب العميل: {last_msg}

التنسيق المطلوب:
1. **تحليل المشكلة أو الفرصة**
2. **الحلول المقترحة (2-3 حلول)**
3. **خطة تنفيذية من 5 خطوات**
4. **الأدوات والتقنيات الموصى بها**
5. **الميزانية التقريبية والعائد المتوقع**
6. **مصادر ومراجع مفيدة**

كن عملياً ومحدداً."""
        else:
            prompt = f"""You are a business and technical consultant. Provide a detailed professional consultation in English.

Client request: {last_msg}

Format:
1. **Problem/Opportunity Analysis**
2. **Proposed Solutions (2-3)**
3. **Implementation Steps (5 steps)**
4. **Recommended Tools & Technologies**
5. **Estimated Budget & Expected ROI**
6. **Useful Resources & References"""
        
        consultation = call_ollama(prompt)
        
        # حفظ النص في ملف txt
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_path = os.path.join(CONSULTING_DIR, f"consult_{user_id}_{timestamp}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Request: {last_msg}\n\n{consultation}")
        
        # إرسال الرد النصي فقط (بدون PDF)
        if lang == "ar":
            response = f"""💼 **استشارة احترافية**

{consultation}

📁 تم حفظ الاستشارة في ملف نصي: `{txt_path}`

💡 هل تريد استشارة أخرى؟"""
        else:
            response = f"""💼 **Professional Consultation**

{consultation}

📁 Consultation saved to: `{txt_path}`

💡 Need another consultation?"""
        
        state["messages"].append(response)
        return state
    
    # رد المساعدة
    if lang == "ar":
        response = """💼 **خدمة الاستشارات الاحترافية**

للاستشارة، أرسل:
`استشارة: [وصف طلبك]`

مثال: `استشارة: كيف أختار منصة التجارة الإلكترونية المناسبة لمشروعي الصغير؟`

ستحصل على رد نصي مفصل (بدون PDF حالياً لضمان جودة العرض)."""
    else:
        response = """💼 **Professional Consulting Service**

To request a consultation, send:
`consulting: [describe your request]`

Example: `consulting: how to choose the right e-commerce platform for my small business?`

You will receive a detailed text reply (PDF temporarily disabled for Arabic support)."""
    
    state["messages"].append(response)
    return state
