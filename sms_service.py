import os
from twilio.rest import Client

# Environment Variables
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
MESSAGING_SERVICE_SID = os.environ.get("MESSAGING_SERVICE_SID")

def dispatch_to_all(contacts, message_text):
    """
    Loops through all verified contacts and dispatches the live payload via Twilio.
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return {"success": False, "error": "Twilio credentials missing in Render Env"}
        
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    success_count = 0
    errors = []

    # Contacts list par iterate karein
    for contact in contacts:
        name = contact.get("name", "Unknown")
        phone = contact.get("phone")
        
        if not phone:
            continue
            
        try:
            message = client.messages.create(
                messaging_service_sid=MESSAGING_SERVICE_SID,
                body=f"Alert from Parth: {message_text}",
                to=phone
            )
            success_count += 1
        except Exception as e:
            errors.append(f"Error sending to {name}: {str(e)}")

    if success_count > 0:
        return {"success": True, "message": f"Successfully sent to {success_count} contacts.", "errors": errors}
    else:
        return {"success": False, "error": "Failed to send to any contact.", "details": errors}
