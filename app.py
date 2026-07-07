from flask import Flask, render_template, request, jsonify
from messages import get_message
from sms_service import dispatch_to_all
import json
import os

# Yahan humne Flask ko bol diya ki agar templates folder na mile, toh direct root se padh le
app = Flask(__name__, template_folder='.', static_folder='static')

@app.route('/')
def home():
    # Agar templates folder me hai ya root me, dono jagah check karega
    if os.path.exists('templates/index.html'):
        return render_template('templates/index.html')
    return render_template('index.html')

@app.route('/send-sms', methods=['POST'])
def send_sms():
    try:
        data = request.get_json()
        if not data or 'action' not in data:
            return jsonify({"success": False, "error": "No action provided"}), 400
        
        action = data['action']
        message_text = get_message(action)
        
        with open('contacts.json', 'r') as file:
            contacts = json.load(file)
            
        dispatch_result = dispatch_to_all(contacts, message_text)
        return jsonify(dispatch_result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
