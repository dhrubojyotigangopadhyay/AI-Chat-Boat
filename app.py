import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Fetch the key from Render
API_KEY = os.environ.get("GEMINI_API_KEY")

# Setup the new Client
client = genai.Client(api_key=API_KEY)

@app.route('/')
def home():
    return "Dhrubo's AI is Online and Modernized!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        user_message = data.get("message", "Hi")
        
        # New syntax for Gemini 1.5 Flash
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_message
        )
        
        return jsonify({"reply": response.text})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": f"Technical issue: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
