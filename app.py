import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# This pulls your new March 27 key (U2gE) from Render settings
API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize the modern 2026 Google Client
client = genai.Client(api_key=API_KEY)

@app.route('/')
def home():
    return "Dhrubo's AI is Online and Modernized!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get data from ManyChat
        data = request.get_json()
        if not data:
            return jsonify({"reply": "No data received"}), 400
            
        user_message = data.get("message", "Hi")
        
        # Using the 2.5 Flash model - the current stable version for 2026
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=user_message
        )
        
        # Return the AI's answer back to ManyChat
        return jsonify({"reply": response.text})
    
    except Exception as e:
        print(f"Error: {e}")
        # If it fails, ManyChat will show you the exact reason here
        return jsonify({"reply": f"Technical issue: {str(e)}"}), 500

if __name__ == '__main__':
    # Render uses port 10000 by default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
