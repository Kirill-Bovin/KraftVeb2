from flask import Flask, request, render_template, redirect, flash, url_for
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="frontend/templates")
app.secret_key = "supersecretkey"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/", methods=["GET", "POST"])
def index():
    print("[DEBUG] Зашли в index()")
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        print(f"[DEBUG] Получено сообщение: {name=}, {email=}, {phone=}, {message=}")

        text = f"💬 Новое сообщение:\n👤 Имя: {name}\n📧 Email: {email}\n📞 Телефон: {phone}\n📝 Сообщение: {message}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text}

        try:
            r = requests.post(url, json=payload)
            print("[DEBUG] Telegram response:", r.status_code, r.text)
            r.raise_for_status()
            flash("Сообщение успешно отправлено!", "success")
        except Exception as e:
            print("[ERROR]", e)
            flash("Ошибка при отправке сообщения", "danger")

        return redirect(url_for("index"))

    return render_template("index.html")

@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render подставит свой порт
    app.run(host='0.0.0.0', port=port)