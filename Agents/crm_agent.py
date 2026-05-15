# Agents/crm_agent.py
import json
import os
from datetime import datetime

CRM_FILE = "Data/customers.json"

def load_customers():
    if os.path.exists(CRM_FILE):
        with open(CRM_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_customers(customers):
    with open(CRM_FILE, "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=2, ensure_ascii=False)

def crm_agent(state):
    print("📋 CRM Agent يعمل...")
    
    user_id = str(state.get("user_id", "unknown"))
    last_msg = state["messages"][-1].lower()
    
    customers = load_customers()
    
    # تسجيل عميل جديد
    if user_id not in customers:
        customers[user_id] = {
            "first_seen": datetime.now().isoformat(),
            "interactions": 0,
            "orders": [],
            "last_message": ""
        }
    
    # تحديث تفاعلات العميل
    customers[user_id]["interactions"] += 1
    customers[user_id]["last_message"] = last_msg[:100]
    customers[user_id]["last_active"] = datetime.now().isoformat()
    
    save_customers(customers)
    
    # أمر: عرض معلومات العميل
    if any(word in last_msg for word in ["معلوماتي", "my info", "عرض حسابي"]):
        info = customers[user_id]
        response = f"""📋 **معلومات حسابك:**

• عميل منذ: {info['first_seen'][:10]}
• عدد التفاعلات: {info['interactions']}
• آخر نشاط: {info['last_active'][:10]}

شكراً لثقتك في AoraFlow AI!"""
        
        state["messages"].append(response)
        return state
    
    # أمر: المساعدة
    if any(word in last_msg for word in ["crm", "عملاء", "مساعدة"]):
        response = """📋 **نظام إدارة العملاء - المساعدة**

الأوامر المتاحة:
• `معلوماتي` - عرض معلومات حسابك
• `طلباتي` - عرض طلباتك السابقة (قريباً)

سيتم تسجيل جميع تفاعلاتك تلقائياً."""
        
        state["messages"].append(response)
        return state
    
    # رد عادي (تسجيل فقط بدون رد خاص)
    state["messages"].append("✅ تم تسجيل تفاعلك.")
    return state
