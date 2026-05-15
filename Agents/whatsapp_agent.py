# Agents/whatsapp_agent.py
import requests
import json

EVOLUTION_API_URL = "http://localhost:8080"

def send_whatsapp_message(phone: str, message: str):
    """إرسال رسالة واتساب"""
    try:
        payload = {
            "number": phone,
            "message": message
        }
        response = requests.post(f"{EVOLUTION_API_URL}/message/sendText", json=payload, timeout=10)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": f"فشل الاتصال بـ WhatsApp: {e}"}

def whatsapp_agent(state):
    print("📱 WhatsApp Agent يعمل...")
    last_msg = state["messages"][-1]
    
    response = f"✅ تم استلام طلبك عبر WhatsApp: {last_msg[:80]}...\nسيتم معالجته قريباً."
    
    state["messages"].append(f"[WhatsApp] {response}")
    return state
