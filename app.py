import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# This pulls your API Key from Render's secret settings
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Dhrubo's AI is Online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data.get("message", "Hi")
    
    # The AI Instructions (You can change this part!)
    prompt = f"You are Dhrubo's assistant. Answer this in a cool, helpful style: {user_message}"
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Sorry, my brain is tired. Try again!"}), 500

if __name__ == '__main__':
    # Render needs it to run on port 10000 by default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)