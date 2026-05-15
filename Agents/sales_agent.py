# Agents/sales_agent.py
import json
import os
from datetime import datetime

def sales_agent(state):
    print("💰 Sales Agent يعمل...")
    
    last_msg = state["messages"][-1].lower()
    
    # قائمة الخدمات والأسعار
    products = {
        "bot_basic": {"name": "بوت تليجرام أساسي", "price": 99, "description": "بوت للردود التلقائية والترحيب"},
        "bot_advanced": {"name": "بوت تليجرام متقدم", "price": 249, "description": "بوت مع قاعدة بيانات ولوحة تحكم"},
        "data_analysis": {"name": "تحليل بيانات شامل", "price": 149, "description": "تحليل ملفات CSV/Excel مع رسوم بيانية"},
        "ai_consulting": {"name": "استشارة ذكاء اصطناعي", "price": 99, "description": "استشارة 60 دقيقة مع خبير AI", "unit": "hour"},
        "subscription": {"name": "اشتراك شهري", "price": 49, "description": "دعم مستمر وتحديثات شهرية", "unit": "month"}
    }
    
    # تخزين معلومات العميل
    user_id = state.get("user_id", "unknown")
    customers_file = "Data/customers.json"
    
    def load_customers():
        if os.path.exists(customers_file):
            with open(customers_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_customers(customers):
        os.makedirs("Data", exist_ok=True)
        with open(customers_file, 'w', encoding='utf-8') as f:
            json.dump(customers, f, indent=2, ensure_ascii=False)
    
    # ==================== التعرف على طلب العميل ====================
    
    # طلب سعر منتج معين
    for key, product in products.items():
        if product["name"] in last_msg or key in last_msg:
            response = f"""💰 **عرض سعر: {product['name']}**

📝 **الوصف:** {product['description']}
💵 **السعر:** ${product['price']}
{'⏱️ الوحدة: ' + product.get('unit', 'مرة واحدة') if product.get('unit') else '✅ دفع مرة واحدة'}

**لطلب هذا المنتج، أرسل:** `اطلب {product['name']}`

أو تواصل معنا للحصول على عرض مخصص."""
            state["messages"].append(response)
            return state
    
    # طلب عرض أسعار كامل
    if any(word in last_msg for word in ["الأسعار", "prices", "قائمة الأسعار", "كامل"]):
        response = "💰 **قائمة أسعار AoraFlow AI:**\n\n"
        for key, product in products.items():
            unit = product.get('unit', 'مرة واحدة')
            response += f"• **{product['name']}**: ${product['price']} ({unit})\n"
            response += f"  {product['description']}\n\n"
        response += "لطلب أي خدمة، اكتب: `اطلب [اسم الخدمة]`"
        state["messages"].append(response)
        return state
    
    # طلب شراء
    if any(word in last_msg for word in ["اطلب", "buy", "شراء", "أريد"]):
        for key, product in products.items():
            if product["name"] in last_msg or key in last_msg:
                # تسجيل العميل
                customers = load_customers()
                if str(user_id) not in customers:
                    customers[str(user_id)] = []
                
                order = {
                    "product": product["name"],
                    "price": product["price"],
                    "date": datetime.now().isoformat(),
                    "status": "pending"
                }
                customers[str(user_id)].append(order)
                save_customers(customers)
                
                response = f"""✅ **تم استلام طلبك!**

📦 **المنتج:** {product['name']}
💰 **السعر:** ${product['price']}

**الخطوات التالية:**
1️⃣ سيتم التواصل معك خلال 24 ساعة
2️⃣ تأكيد الطلب وإتمام الدفع
3️⃣ تسليم المنتج خلال 3 أيام

شكراً لثقتك في AoraFlow AI! 🚀
"""
                state["messages"].append(response)
                return state
    
    # طلب خصم أو مفاوضة
    if any(word in last_msg for word in ["خصم", "discount", "تخفيض", "تفاوض"]):
        response = """🎯 **عروضنا الحالية:**

• خصم 10% على أول طلب
• خصم 15% عند طلب خدمتين أو أكثر

يمكننا أيضاً تقديم عرض مخصص حسب ميزانيتك. أرسل تفاصيل مشروعك وسنرد عليك خلال ساعة."""
        state["messages"].append(response)
        return state
    
    # استفسار عام عن المبيعات
    response = """💼 **كيف يمكنني مساعدتك في المبيعات؟**

أخبرني بما تريد:
• `أسعار` - لعرض قائمة الأسعار الكاملة
• `سعر [اسم الخدمة]` - للحصول على عرض سعر محدد
• `اطلب [اسم الخدمة]` - لشراء منتج
• `خصم` - للاستفسار عن العروض والتخفيضات

**خدماتنا:**
- بوت تليجرام أساسي ($99)
- بوت تليجرام متقدم ($249)
- تحليل بيانات شامل ($149)
- استشارة ذكاء اصطناعي ($99/ساعة)
- اشتراك شهري ($49/شهر)"""
    
    state["messages"].append(response)
    return state
