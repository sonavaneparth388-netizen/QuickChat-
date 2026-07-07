# Predefined QuickChat alert messages mapped directly to your new UI buttons
ALERT_MESSAGES = {
    "reach_office": "I have reached the office safely.",
    "left_office": "I have left from the office and am on my way.",
    "custom": "Quick update: Please check your phone or chat.",
    "call_urgent": "Call me urgently! It's important."
}

def get_message(alert_type):
    """
    Retrieves the text message for a given alert type.
    Defaults to a generic alert if the key doesn't match perfectly.
    """
    return ALERT_MESSAGES.get(alert_type, "QuickChat Alert: Please check your messages.")
