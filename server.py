import requests
import random
import base64
from cryptography.fernet import Fernet

# --- ТВОИ ЗАШИФРОВАННЫЕ ДАННЫЕ ---
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

GITHUB_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# --- 1. Отправка сообщения в чат ---
def send_message():
    phrases = ["Система AP-Secure активна.", "Сканирование завершено.", "Проверка связи..."]
    data = {"name": "PYTHON-BOT", "text": random.choice(phrases)}
    try:
        r = requests.post(f"{SUPABASE_URL}/rest/v1/messages", headers=headers, json=data)
        print(f"Сообщение отправлено. Статус: {r.status_code}")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

# --- 2. Создание версии (бэкап в GitHub) ---
def create_version(version_name):
    print(f"Создание версии {version_name}...")
    url_get = f"https://api.github.com/repos/{GITHUB_REPO}/contents/index.html"
    res = requests.get(url_get, headers=GITHUB_HEADERS)
    if res.status_code != 200:
        print("Ошибка: index.html не найден в репозитории.")
        return

    content_base64 = res.json()['content']
    url_put = f"https://api.github.com/repos/{GITHUB_REPO}/contents/versions/{version_name}/index.html"
    payload = {"message": f"Auto-backup {version_name}", "content": content_base64}
    
    res_put = requests.put(url_put, headers=GITHUB_HEADERS, json=payload)
    if res_put.status_code in [200, 201]:
        print(f"Версия {version_name} успешно сохранена!")
    else:
        print(f"Ошибка сохранения версии: {res_put.text}")

# --- 3. Проверка команд из базы (если ты оставил их в чате) ---
def check_commands():
    url = f"{SUPABASE_URL}/rest/v1/messages?select=*&order=created_at.desc&limit=1"
    res = requests.get(url, headers=headers)
    if res.status_code == 200 and res.json():
        msg = res.json()[0]
        # Если кто-то (Админ) написал в чат команду "!version v1.0"
        if msg['name'] == 'ADMIN' and msg['text'].startswith('!version '):
            version_name = msg['text'].split(' ')[1]
            create_version(version_name)

if __name__ == "__main__":
    send_message()
    check_commands() # Проверяем, не просил ли ты создать версию
