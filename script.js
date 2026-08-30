function triggerAlert(alertType, customMessage = null) {
    const banner = document.getElementById('status-banner');
    
    showBanner("Sending emergency broadcast...", "info");

    let payload = { action: alertType };
    if (alertType === 'custom' || customMessage) {
        payload.custom_message = customMessage;
    }

    fetch('/send-sms', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showBanner(`✅ Alert Broadcasted successfully! ${data.message || ''}`, "success");
        } else {
            showBanner(`❌ Failed to dispatch alert: ${data.error || 'Unknown error'}`, "error");
        }
    })
    .catch(error => {
        console.error('Error sending alert:', error);
        showBanner("🚨 Connection Error: Ensure Flask server is running.", "error");
    });
}

function showBanner(message, type) {
    const banner = document.getElementById('status-banner');
    if (!banner) return;
    banner.textContent = message;
    banner.classList.remove('hidden', 'success', 'error', 'info');
    banner.classList.add(type);
    
    if (type === "success") {
        setTimeout(() => {
            banner.classList.add('hidden');
        }, 6000);
    }
}

