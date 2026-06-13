from flask import Flask, request, jsonify, render_template_string
from chatbot import get_response

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartSupport AI Chatbot</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 420px; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); display: flex; flex-direction: column; height: 580px; }
        .chat-header { background: #2c3e50; color: white; padding: 16px 20px; border-radius: 12px 12px 0 0; font-size: 16px; font-weight: bold; }
        .chat-header span { font-size: 12px; color: #a0aec0; display: block; margin-top: 2px; }
        .chat-messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
        .message { max-width: 80%; padding: 10px 14px; border-radius: 18px; font-size: 14px; line-height: 1.4; }
        .user { background: #2c3e50; color: white; align-self: flex-end; border-radius: 18px 18px 4px 18px; }
        .bot { background: #f0f2f5; color: #2d3748; align-self: flex-start; border-radius: 18px 18px 18px 4px; }
        .chat-input { display: flex; padding: 12px; border-top: 1px solid #e2e8f0; gap: 8px; }
        .chat-input input { flex: 1; padding: 10px 14px; border: 1px solid #e2e8f0; border-radius: 24px; outline: none; font-size: 14px; }
        .chat-input button { background: #2c3e50; color: white; border: none; padding: 10px 18px; border-radius: 24px; cursor: pointer; font-size: 14px; }
        .chat-input button:hover { background: #34495e; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            SmartSupport AI
            <span>🟢 Online — Ask me anything</span>
        </div>
        <div class="chat-messages" id="messages">
            <div class="message bot">Hi! I'm SmartSupport AI. How can I help you today?</div>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Type your message..." onkeypress="if(event.key==='Enter') sendMessage()" />
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const messages = document.getElementById('messages');
            const text = input.value.trim();
            if (!text) return;

            messages.innerHTML += `<div class="message user">${text}</div>`;
            input.value = '';
            messages.scrollTop = messages.scrollHeight;

            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            messages.innerHTML += `<div class="message bot">${data.reply}</div>`;
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = get_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)