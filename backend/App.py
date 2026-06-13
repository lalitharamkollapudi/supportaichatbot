import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ai import generate_response
from chatbot import get_response

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    reply = generate_response(user_message) or get_response(user_message)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=True)