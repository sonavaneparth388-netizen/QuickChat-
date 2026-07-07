import os
from twilio.rest import Client

# Yeh lines ab system/Render ke Environment Variables se keys uthayengi
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
MESSAGING_SERVICE_SID = os.environ.get("MESSAGING_SERVICE_SID")

def send_sms_alert(contact_name, phone_number, message_text):
    """
    Sends an actual live text message via your Twilio Messaging Service.
    """
    try:
        # Check configuration safety
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            return {"success": False, "error": "Twilio credentials missing in Environment Variables"}

        # Initialize the live Twilio API client connection
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Dispatch the message
        message = client.messages.create(
            messaging_service_sid=MESSAGING_SERVICE_SID,
            body=f"Alert from Parth: {message_text}",
            to=phone_number
        )
        
        print(f" Live SMS sent to {contact_name}")
        return {"success": True, "sid": message.sid}

    except Exception as e:
        print(f"❌ Error sending to {contact_name}: {str(e)}")
        return {"success": False, "error": str(e)}
