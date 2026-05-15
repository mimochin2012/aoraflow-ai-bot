# graph.py - شامل مع Web Agent
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Agents.general_agent import general_agent
from Agents.data_agent import data_agent
from Agents.bot_builder_agent import bot_builder_agent
from Agents.payment_agent import payment_agent
from Agents.consulting_agent import consulting_agent
from Agents.web_agent import web_agent
from Agents.marketing_agent import marketing_agent

MEMORY_FILE = "user_memory.json"

def is_building_bot(user_id):
    user_id = str(user_id)
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get(user_id, {}).get("bot_step") in ["waiting_name", "waiting_tasks", "waiting_token"]
        except:
            pass
    return False

def run_supervisor(user_input, user_id, memory=None):
    if memory is None:
        memory = {}
    user_id = str(user_id)
    u = user_input.lower()

    if is_building_bot(user_id):
        state = {"messages": [user_input], "user_id": user_id, "pdf_to_send": None, "memory": memory}
        return bot_builder_agent(state)

    # البحث على الإنترنت (أولوية عالية)
    if any(w in u for w in ["خطة تسويقية", "marketing plan", "plan marketing", "منشور", "post", "publication", "عروض", "offers", "ترويج", "promote", "اعلان", "ad", "فوائد", "benefits", "avantages", "فكرة", "idea", "idée", "services"]):
        state = {"messages": [user_input], "user_id": user_id, "pdf_to_send": None, "memory": memory}
        return web_agent(state)

    # أوامر الدفع
    if any(w in u for w in ["خطة تسويقية", "marketing plan", "plan marketing", "منشور", "post", "publication", "عروض", "offers", "ترويج", "promote", "اعلان", "ad", "فوائد", "benefits", "avantages", "فكرة", "idea", "idée", "services"]):
        state = {"messages": [user_input], "user_id": user_id, "pdf_to_send": None, "memory": memory}
        return payment_agent(state)

    # استشارات
    if any(w in u for w in ["خطة تسويقية", "marketing plan", "plan marketing", "منشور", "post", "publication", "عروض", "offers", "ترويج", "promote", "اعلان", "ad", "فوائد", "benefits", "avantages", "فكرة", "idea", "idée", "services"]):
        state = {"messages": [user_input], "user_id": user_id, "pdf_to_send": None, "memory": memory}
        return consulting_agent(state)

    # تحليل ملفات
    if any(w in u for w in ["خطة تسويقية", "marketing plan", "plan marketing", "منشور", "post", "publication", "عروض", "offers", "ترويج", "promote", "اعلان", "ad", "فوائد", "benefits", "avantages", "فكرة", "idea", "idée", "services"]):
        state = {"messages": [user_input], "user_id": user_id, "pdf_to_send": None, "memory": memory}
        return data_agent(state)

    # إنشاء بوت
    if any(w in u for w in ["خطة تسويقية", "marketing plan", "plan marketing", "منشور", "post", "publication", "عروض", "offers", "ترويج", "promote", "اعلان", "ad", "فوائد", "benefits", "avantages", "فكرة", "idea", "idée", "services"]):
        state = {"messages": [user_input], "user_id": user_id, "pdf_to_send": None, "memory": memory}
        return bot_builder_agent(state)

        # تسويق وترويج
    if any(w in u for w in ["خطة تسويقية", "marketing plan", "plan marketing", "منشور", "post", "publication", "عروض", "offers", "ترويج", "promote", "اعلان", "ad", "فوائد", "benefits", "avantages", "فكرة", "idea", "idée", "services"]):
        state = {"messages": [user_input], "user_id": user_id, "pdf_to_send": None, "memory": memory}
        return marketing_agent(state)

    
    state = {"messages": [user_input], "user_id": user_id, "pdf_to_send": None, "memory": memory}
    return general_agent(state)

def run_supervisor_with_file(user_input, user_id, file_path, file_name, memory=None):
    if memory is None:
        memory = {}
    state = {"messages": [user_input], "user_id": str(user_id), "file_path": file_path, "file_name": file_name, "pdf_to_send": None, "memory": memory}
    return data_agent(state)

if __name__ == "__main__":
    print("✅ Supervisor ready with Web Agent")



