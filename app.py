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

def load_contacts_data():
    contacts_env = os.environ.get("CONTACTS_JSON")
    if contacts_env:
        try:
            return json.loads(contacts_env)
        except Exception as e:
            print("Error parsing CONTACTS_JSON env:", e)
    if os.path.exists('contacts.json'):
        try:
            with open('contacts.json', 'r') as file:
                return json.load(file)
        except Exception:
            pass
    return []

@app.route('/contacts.json')
def get_contacts():
    return jsonify(load_contacts_data())

@app.route('/send-sms', methods=['POST'])
def send_sms():
    try:
        data = request.get_json() or {}
        action = data.get('action')
        custom_msg = data.get('custom_message') or data.get('alert_type')

        if not action and not custom_msg:
            return jsonify({"success": False, "error": "No action or message provided"}), 400
        
        message_text = get_message(action, custom_msg)
        contacts = load_contacts_data()
        
        dispatch_result = dispatch_to_all(contacts, message_text)
        return jsonify(dispatch_result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
