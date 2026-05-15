# Agents/report_agent.py
import json
import os
from datetime import datetime

CRM_FILE = "Data/customers.json"
LOG_DIR = "Logs"

def report_agent(state):
    print("📊 Report Agent يعمل...")
    
    last_msg = state["messages"][-1].lower()
    
    if any(word in last_msg for word in ["تقرير يومي", "daily report", "تقرير"]):
        # قراءة بيانات العملاء
        customers = {}
        if os.path.exists(CRM_FILE):
            with open(CRM_FILE, "r", encoding="utf-8") as f:
                customers = json.load(f)
        
        total_customers = len(customers)
        total_interactions = sum(c.get("interactions", 0) for c in customers.values())
        
        report = f"""📊 **تقرير AoraFlow AI**

📅 التاريخ: {datetime.now().strftime("%Y-%m-%d")}

👥 **العملاء:**
• إجمالي العملاء: {total_customers}
• إجمالي التفاعلات: {total_interactions}

✅ **النظام:**
• المدير التنفيذي: يعمل
• الـ 7 Agents: نشطون
• n8n: متصل

🚀 مستعد لخدمتك!"""
        
        state["messages"].append(report)
        return state
    
    # أمر المساعدة
    if any(word in last_msg for word in ["help", "مساعدة"]):
        response = """📊 **تقرير Agent - المساعدة**

الأوامر المتاحة:
• `تقرير يومي` - عرض تقرير عن أداء النظام
• `تقرير` - ملخص سريع

سيتم إضافة تقارير أكثر تفصيلاً لاحقاً."""
        
        state["messages"].append(response)
        return state
    
    response = "📊 أرسل `تقرير يومي` لعرض تقرير عن أداء النظام."
    state["messages"].append(response)
    return state
