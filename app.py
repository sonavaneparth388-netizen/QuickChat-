from flask import Flask, render_template, request, jsonify
from messages import get_message
from sms_service import dispatch_to_all
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-sms', methods=['POST'])
def send_sms():
    try:
        # Grab the JSON data sent from index.html
        data = request.get_json()
        if not data or 'action' not in data:
            return jsonify({"success": False, "error": "No action provided"}), 400
        
        action = data['action']
        
        # 1. Translate the key button action into the actual text phrase
        message_text = get_message(action)
        
        # 2. Load your verified target contacts configuration list
        # (Assuming your JSON file is named contacts.json)
        with open('contacts.json', 'r') as file:
            contacts = json.load(file)
            
        # 3. Fire the real live payload over the Twilio Gateway API
        dispatch_result = dispatch_to_all(contacts, message_text)
        
        return jsonify(dispatch_result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Running on local development portal interface host
    app.run(host='0.0.0.0', port=5000, debug=True)
