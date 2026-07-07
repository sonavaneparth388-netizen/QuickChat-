function triggerAlert(alertType) {
    const banner = document.getElementById('status-banner');
    
    // Provide instant UI touch feedback by showing a sending state
    showBanner("Sending emergency broadcast...", "success");

    // Send the asynchronous POST request to our Flask app
    fetch('/send-alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ alert_type: alertType })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showBanner(`✅ Alert Broadcasted successfully to ${data.total_sent} recipients!`, "success");
        } else {
            showBanner(`❌ Failed to dispatch alert: ${data.error || 'Unknown error'}`, "error");
        }
    })
    .catch(error => {
        console.error('Error sending alert:', error);
        showBanner("🚨 Connection Error: Ensure Flask server is running locally.", "error");
    });
}

function showBanner(message, type) {
    const banner = document.getElementById('status-banner');
    banner.textContent = message;
    
    // Clear previous dynamic layout states
    banner.classList.remove('hidden', 'success', 'error');
    
    // Inject current active status type class
    banner.classList.add(type);
    
    // For successful sent logs, fade the notification out after 6 seconds
    if (message.includes("successfully")) {
        setTimeout(() => {
            banner.classList.add('hidden');
        }, 6000);
    }
}
