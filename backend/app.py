from flask import Flask, request, jsonify
from flask_cors import CORS
from model import get_response
from filters import is_offensive
from utils import format_chat_log, save_chat_log_to_csv

app = Flask(__name__)
CORS(app)
chat_sessions = {}
chat_logs = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "default")
    user_input = data["message"]

    if is_offensive(user_input):
        return jsonify({"response": "Let's keep things respectful. Want to talk about what’s bothering you?"})

    history = chat_sessions.get(user_id)
    response, history = get_response(user_input, history)
    chat_sessions[user_id] = history
    chat_logs.append(format_chat_log(user_input, response))

    log_entry = format_chat_log(user_input,response)
    save_chat_log_to_csv(log_entry)
  
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)