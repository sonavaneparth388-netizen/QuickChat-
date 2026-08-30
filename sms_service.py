import os
import json
import urllib.request
import urllib.error
from twilio.rest import Client

def load_env_file():
    """Reads .env file and sets environment variables if not already set."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = val

load_env_file()

def send_sendgrid_email(to_email, subject, body_text):
    """Dispatches email notification via SendGrid v3 API."""
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender_email = os.environ.get("SENDER_EMAIL")
    
    if not api_key or not sender_email:
        return False, "SendGrid API key or sender email not configured"
        
    url = "https://api.sendgrid.com/v3/mail/send"
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": sender_email, "name": "QuickChat Alert"},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body_text}]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            if response.status in (200, 202):
                return True, "Email dispatched"
            return False, f"HTTP {response.status}"
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8', errors='ignore')
        return False, f"SendGrid error ({e.code}): {err_msg}"
    except Exception as e:
        return False, str(e)

def dispatch_to_all(contacts, message_text):
    """
    Loops through all contacts and dispatches payload via Twilio SMS (and SendGrid Email if configured).
    """
    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_token = os.environ.get("TWILIO_AUTH_TOKEN")
    messaging_service_sid = os.environ.get("MESSAGING_SERVICE_SID")

    if not twilio_sid or not twilio_token:
        return {"success": False, "error": "Twilio credentials missing in Environment (.env or Render Env)"}

    client = Client(twilio_sid, twilio_token)
    success_count = 0
    errors = []
    
    # Clean output message body formatted as requested: "Parth : <Message>"
    formatted_body = f"Parth : {message_text}"

    for contact in contacts:
        name = contact.get("name", "Unknown")
        phone = contact.get("phone")
        email = contact.get("email")

        # 1. Twilio SMS Dispatch
        if phone:
            try:
                msg_kwargs = {
                    "body": formatted_body,
                    "to": phone
                }
                if messaging_service_sid:
                    msg_kwargs["messaging_service_sid"] = messaging_service_sid

                client.messages.create(**msg_kwargs)
                success_count += 1
            except Exception as e:
                errors.append(f"SMS Error to {name} ({phone}): {str(e)}")

        # 2. SendGrid Email Dispatch (if email is provided for contact)
        if email:
            sent_ok, err = send_sendgrid_email(email, formatted_body, formatted_body)
            if not sent_ok:
                errors.append(f"Email Error to {name} ({email}): {err}")

    if success_count > 0:
        return {"success": True, "message": f"Successfully sent alert to {success_count} contact(s).", "errors": errors}
    else:
        return {"success": False, "error": "Failed to send alert to any contact.", "details": errors}

