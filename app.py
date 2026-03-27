import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# This part is critical - it fetches the key you put in Render
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
else:
    print("CRITICAL ERROR: GEMINI_API_KEY is missing!")

model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Dhrubo's AI Server is Live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the data from ManyChat
        data = request.get_json()
        if not data:
            return jsonify({"reply": "No data received"}), 400
            
        user_message = data.get("message", "Hi")
        
        # Ask Gemini for the answer
        response = model.generate_content(user_message)
        
        # Send the answer back to ManyChat
        return jsonify({"reply": response.text})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # This will tell us EXACTLY what went wrong in the ManyChat response body
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
