from flask import Flask, request, jsonify
import requests
import threading
import time
import random
import base64
from cryptography.fernet import Fernet

app = Flask(__name__)

# --- ЗАШИФРОВАННЫЕ ДАННЫЕ ---
KEY = b'7l0DMAunb6CFNXNqQZEHOL4JLCgV2HWlYcUR-z_Z_yg='
ENCRYPTED_TOKEN = b'gAAAAABq-z2grnla8eMlUISXbjrGL6U_pDofi6qIYl6lsZ_v_ASDS_ytuB4I99IiEzSH4BCAIruMln7DdqFLs0jhyDyUV1R-bW8WcG_cnesq_AbvPaKmemFomlrbBk2OEwh3abMSAV7j'

cipher = Fernet(KEY)
GITHUB_TOKEN = cipher.decrypt(ENCRYPTED_TOKEN).decode()

GITHUB_REPO = "eueu55320-sys/AP-Bot"  # Проверь название репозитория!

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

@app.route('/api/update', methods=['POST'])
def update_html():
    data = request.json
    if data.get('key') != 'AP-SECRET-2609':
        return jsonify({"error": "Доступ запрещен"}), 403
    new_html = data.get('html')
    if not new_html:
        return jsonify({"error": "Нет HTML"}), 400
    res = requests.patch(f"{SUPABASE_URL}/rest/v1/interface?id=eq.1", headers=headers, json={"html_code": new_html})
    if res.status_code in [200, 204]:
        return jsonify({"status": "success"})
    return jsonify({"error": res.text}), 500

@app.route('/api/version', methods=['POST'])
def create_version():
    data = request.json
    if data.get('key') != 'AP-SECRET-2609':
        return jsonify({"error": "Доступ запрещен"}), 403
    version_name = data.get('version')
    if not version_name:
        return jsonify({"error": "Нет имени версии"}), 400
    url_get = f"https://api.github.com/repos/{GITHUB_REPO}/contents/index.html"
    res = requests.get(url_get, headers=GITHUB_HEADERS)
    if res.status_code != 200:
        return jsonify({"error": "index.html не найден"}), 404
    content_base64 = res.json()['content']
    url_put = f"https://api.github.com/repos/{GITHUB_REPO}/contents/versions/{version_name}/index.html"
    payload = {"message": f"Auto-backup {version_name}", "content": content_base64}
    res_put = requests.put(url_put, headers=GITHUB_HEADERS, json=payload)
    if res_put.status_code in [200, 201]:
        return jsonify({"status": "success"})
    return jsonify({"error": res_put.text}), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "online", "bot": "AP-Python-Bot"})

def run_bot():
    while True:
        phrases = ["Система активна.", "Сканирование завершено.", "Проверка связи..."]
        data = {"name": "PYTHON-BOT", "text": random.choice(phrases)}
        try:
            requests.post(f"{SUPABASE_URL}/rest/v1/messages", headers=headers, json=data)
        except: pass
        time.sleep(600)

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)