import requests
import random
import os
from cryptography.fernet import Fernet

# Твои данные
KEY = b'7l0DMAunb6CFNXNqQZEHOL4JLCgV2HWlYcUR-z_Z_yg='
ENCRYPTED_TOKEN = b'gAAAAABq-z2grnla8eMlUISXbjrGL6U_pDofi6qIYl6lsZ_v_ASDS_ytuB4I99IiEzSH4BCAIruMln7DdqFLs0jhyDyUV1R-bW8WcG_cnesq_AbvPaKmemFomlrbBk2OEwh3abMSAV7j'

cipher = Fernet(KEY)
GITHUB_TOKEN = cipher.decrypt(ENCRYPTED_TOKEN).decode()

GITHUB_REPO = "eueu55320-sys/AP-Bot" 

SUPABASE_URL = "https://kvpzrpqwbsrgyxsgcowc.supabase.co"
SUPABASE_KEY = "sb_publishable_jlSw4v_rY_fD0if0WtkzDw_0qxlVmqA"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def send_message():
    phrases = ["Система AP-Secure активна.", "Сканирование завершено.", "Проверка связи..."]
    data = {"name": "PYTHON-BOT", "text": random.choice(phrases)}
    try:
        r = requests.post(f"{SUPABASE_URL}/rest/v1/messages", headers=headers, json=data)
        print(f"Статус: {r.status_code}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    send_message()
