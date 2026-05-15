# memory.py
import json
import os
from datetime import datetime

MEMORY_FILE = "memory/long_term_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    return []

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def add_to_memory(user_id, interaction):
    memory = load_memory()
    memory.append({
        "user_id": user_id,
        "interaction": interaction,
        "timestamp": datetime.now().isoformat()
    })
    save_memory(memory)

def get_user_history(user_id, limit=5):
    memory = load_memory()
    user_history = [item for item in memory if item.get("user_id") == user_id]
    return user_history[-limit:]
