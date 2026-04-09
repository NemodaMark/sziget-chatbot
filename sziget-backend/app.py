import time
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_engine import SzigetChatbot

app = Flask(__name__)
CORS(app)

bot = SzigetChatbot(threshold=0.15)


@app.route("/api/guest-chat", methods=["POST"])
def guest_chat():
    body = request.get_json(silent=True)

    if not body or "message" not in body:
        return jsonify({"error": "Hiányzó 'message' mező a kérésben."}), 400

    user_message = str(body.get("message", "")).strip()
    history = body.get("messages", [])

    result = bot.get_response(user_message)

    all_messages = []
    for i, msg in enumerate(history):
        role = msg.get("role", "user")
        all_messages.append({
            "id": i + 1,
            "role": role,
            "content": msg.get("content", ""),
            "speakerLabel": "FLO MONDJA" if role == "assistant" else "TE",
            "createdAt": msg.get("createdAt", datetime.datetime.now().isoformat())
        })

    all_messages.append({
        "id": int(time.time() * 1000),
        "role": "assistant",
        "content": result["answer"],
        "speakerLabel": "FLO MONDJA",
        "createdAt": datetime.datetime.now().isoformat()
    })

    return jsonify({"chat": {"messages": all_messages}}), 200


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "kb_size": len(bot.questions)}), 200


if __name__ == "__main__":
    print("🎪 Sziget Chatbot API indul – http://127.0.0.1:8000")
    app.run(debug=True, host="0.0.0.0", port=8000)
