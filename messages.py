# Predefined QuickChat alert messages mapped directly to UI buttons
ALERT_MESSAGES = {
    "reach_college": "Reached at college",
    "reach_office": "Reached at office",
    "left_college": "Left from college",
    "left_office": "Left from office",
    "call_urgent": "Call me urgent"
}

def get_message(alert_type, custom_message=None):
    """
    Retrieves the formatted text message for a given alert type or custom message.
    """
    if custom_message and custom_message.strip():
        return custom_message.strip()
    
    if alert_type in ALERT_MESSAGES:
        return ALERT_MESSAGES[alert_type]
    
    # If action is not a preset key (e.g. user passed custom text directly as action)
    if alert_type and alert_type != "custom":
        return alert_type.strip()
        
    return "Call me urgent"

