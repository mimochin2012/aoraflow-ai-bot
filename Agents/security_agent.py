# Agents/security_agent.py
import subprocess

def security_agent(state):
    print("🛡️ Security Agent يعمل...")
    
    # فحص بسيط للعمليات
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        output = result.stdout.lower()
        suspicious = ['powershell', 'cmd.exe', 'mshta', 'wscript']
        found = [p for p in suspicious if p in output]
        if found:
            response = f"⚠️ تم اكتشاف عمليات مشبوهة: {', '.join(found)}"
        else:
            response = "✅ النظام آمن. لا توجد عمليات مشبوهة."
    except Exception as e:
        response = f"❌ خطأ في فحص الأمان: {e}"
    
    state["messages"].append(response)
    return state
