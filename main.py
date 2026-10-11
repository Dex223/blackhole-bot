from flask import Flask, request, jsonify
import requests
import datetime
import os

app = Flask(__name__)

BOT_TOKEN = "8881791195:AAH4BKtTiBvtbdH3vVqjFUAvF1vz9fU473g"
MY_CHAT_ID = "1322035678"

LOG_FILE = "/tmp/visitors.txt"


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

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{now}] IP={ip} | ПК={computer}\n")
    except Exception as e:
        print(f"[LOG ERROR] {type(e).__name__}: {e}")

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
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "Пока никто не заходил."
    except Exception as e:
        content = f"Ошибка чтения лога: {type(e).__name__}: {e}"
    return f"<pre>{content}</pre>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
