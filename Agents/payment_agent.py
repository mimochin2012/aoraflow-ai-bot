# Agents/payment_agent.py - نظام دفع USDT + PayPal
import json
import os
from datetime import datetime

# ========== إعدادات الدفع ==========
WALLET_ADDRESS = "0xEaF93FE60C7A250Ea2EaCCe1477909BB4251183c"
NETWORK = "BNB Smart Chain (BEP-20)"
PAYPAL_EMAIL = "hichemam.ha@gmail.com"
PAYPAL_CURRENCY = "USD"
PAYMENTS_FILE = "Data/payments.json"

def load_payments():
    os.makedirs("Data", exist_ok=True)
    if os.path.exists(PAYMENTS_FILE):
        with open(PAYMENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_payments(payments):
    with open(PAYMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(payments, f, indent=2, ensure_ascii=False)

def detect_language(text):
    if any(c in text for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"):
        return "ar"
    return "en"

def payment_agent(state):
    print("💰 Payment Agent يعمل...")
    user_id = str(state.get("user_id"))
    last_msg = state["messages"][-1].lower()
    lang = detect_language(last_msg)
    payments = load_payments()

    # عرض طرق الدفع
    if any(w in last_msg for w in ["/pay", "دفع", "pay", "usdt", "payment", "طرق الدفع"]):
        if lang == "ar":
            response = f"""💳 **طرق الدفع المتاحة:**

1️⃣ **USDT (BEP‑20)** – عنوان المحفظة: `{WALLET_ADDRESS}`
2️⃣ **PayPal** – البريد الإلكتروني: `{PAYPAL_EMAIL}`

📌 **كيف تدفع عبر PayPal؟**
- أرسل المبلغ إلى `{PAYPAL_EMAIL}` (اختر "إرسال إلى صديق" لتجنب الرسوم)
- بعد الإرسال، أرسل:
  `تأكيد الدفع PayPal [رقم المعاملة]`
- سيتم تأكيد طلبك وتفعيل الخدمة.

💰 للاطلاع على الأسعار: أرسل `سعر`"""
        else:
            response = f"""💳 **Payment methods available:**

1️⃣ **USDT (BEP‑20)** – Wallet address: `{WALLET_ADDRESS}`
2️⃣ **PayPal** – Email: `{PAYPAL_EMAIL}`

📌 **How to pay via PayPal?**
- Send the amount to `{PAYPAL_EMAIL}` (choose "Send to a friend" to avoid fees)
- After sending, send:
  `confirm PayPal payment [transaction ID]`
- Your request will be confirmed and service activated.

💰 For prices, send `price`"""
        state["messages"].append(response)
        return state

    # تأكيد الدفع عبر PayPal
    if "تأكيد الدفع paypal" in last_msg or "confirm paypal payment" in last_msg:
        parts = last_msg.split()
        txid = parts[-1] if len(parts) > 3 else "unknown"
        if user_id not in payments:
            payments[user_id] = []
        payments[user_id].append({
            "method": "PayPal",
            "txid": txid,
            "amount": None,
            "status": "pending",
            "date": datetime.now().isoformat(),
            "service": None
        })
        save_payments(payments)
        if lang == "ar":
            response = f"✅ تم استلام إثبات الدفع عبر PayPal (رقم: {txid}). سيتم مراجعته قريباً."
        else:
            response = f"✅ PayPal payment proof received (ID: {txid}). Will be reviewed shortly."
        state["messages"].append(response)
        return state

    # تأكيد الدفع عبر USDT (عام)
    if "تأكيد الدفع" in last_msg and "paypal" not in last_msg:
        parts = last_msg.split()
        txid = parts[-1] if len(parts) > 2 else "unknown"
        if user_id not in payments:
            payments[user_id] = []
        payments[user_id].append({
            "method": "USDT",
            "txid": txid,
            "amount": None,
            "status": "pending",
            "date": datetime.now().isoformat(),
            "service": None
        })
        save_payments(payments)
        if lang == "ar":
            response = f"✅ تم استلام إثبات الدفع (TxID: {txid}). سيتم مراجعته."
        else:
            response = f"✅ Payment proof received (TxID: {txid}). Will be reviewed."
        state["messages"].append(response)
        return state

    # عرض الأسعار
    if any(w in last_msg for w in ["سعر", "price", "تكلفة"]):
        if lang == "ar":
            response = """💵 **قائمة الأسعار (بالدولار، يُدفع عبر USDT أو PayPal):**

• تحليل بيانات (تقرير PDF + توصيات): $29
• بوت تليجرام أساسي: $99
• بوت تليجرام متقدم: $249
• استشارة ذكاء اصطناعي (ساعة): $99
• اشتراك شهرى (دعم وتحديثات): $49

للدفع، أرسل `/pay` ثم اتبع التعليمات."""
        else:
            response = """💵 **Price list (USD, paid via USDT or PayPal):**

• Data analysis (PDF report + insights): $29
• Basic Telegram bot: $99
• Advanced Telegram bot: $249
• AI consulting (1 hour): $99
• Monthly subscription (support & updates): $49

To pay, send `/pay` and follow the instructions."""
        state["messages"].append(response)
        return state

    # أمر admin لعرض المدفوعات المعلقة
    if last_msg.startswith("/payments") and user_id == "8525611542":
        pending = []
        for uid, trans in payments.items():
            for t in trans:
                if t.get("status") == "pending":
                    pending.append(f"User {uid}: {t['method']} - {t['txid']} ({t['date']})")
        if pending:
            response = "📋 **المدفوعات المعلقة:**\n" + "\n".join(pending)
        else:
            response = "✅ لا توجد مدفوعات معلقة."
        state["messages"].append(response)
        return state

    # رد افتراضي
    if lang == "ar":
        response = "💰 للدفع عبر USDT أو PayPal، أرسل `/pay`. لعرض الأسعار، أرسل `سعر`."
    else:
        response = "💰 To pay via USDT or PayPal, send `/pay`. For prices, send `price`."
    state["messages"].append(response)
    return state
