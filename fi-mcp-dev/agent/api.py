from flask import Flask, request, jsonify
from agent import run_financial_agent
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        print(f"📨 User message received: {user_message}")

        # Replace this with real agent logic later
        response = {"reply": f"Echo: {user_message}"}
        print(f"📤 Responding with: {response}")

        return jsonify(response)
    except Exception as e:
        print(f"❌ Error in /chat: {e}")
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
