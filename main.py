from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔑 ENV variables (Render me set karna)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")      # PRAKRITI-AI_VERIFY
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")      # Meta access token
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# ---------------- VERIFY WEBHOOK ----------------
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid token", 403


# ---------------- RECEIVE MESSAGE ----------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("INCOMING:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        reply = f"🙏 Namaste!\nMain *Prakriti AI* hoon 🌱\nAapne likha: {text}"

        send_message(sender, reply)

    except Exception as e:
        print("ERROR:", e)

    return "ok", 200


# ---------------- SEND MESSAGE ----------------
def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    r = requests.post(url, json=payload, headers=headers)
    print("SEND STATUS:", r.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
