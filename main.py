from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

BOT_TOKEN = "8881791195:AAHKLjXzt3Mvrq5Vg42kdbf_Z2YhRxMb5SU"
MY_CHAT_ID = "1322035678"


def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": MY_CHAT_ID, "text": text}, timeout=10)
        print(f"[TG] {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"[TG ERROR] {type(e).__name__}: {e}")


@app.route("/")
def index():
    return "Black Hole Tracker is running!"


@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json(silent=True) or {}
    computer = data.get("computer", "неизвестно")

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("/home/Dex23/mysite/visitors.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] IP={ip} | ПК={computer}\n")

    msg = (
        f"Black Hole запущен!\n"
        f"Компьютер: {computer}\n"
        f"IP: {ip}\n"
        f"Время: {now}"
    )
    send_to_telegram(msg)
    return jsonify({"status": "ok"}), 200


@app.route("/visitors", methods=["GET"])
def visitors():
    try:
        with open("/home/Dex23/mysite/visitors.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "Пока никто не заходил."
    return f"<pre>{content}</pre>"