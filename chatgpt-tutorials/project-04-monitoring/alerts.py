import os
import requests

def alert(app_message):
    """
    The alert function is responsible for sending alert messages 
    to a specified webhook URL. It retrieves the webhook URL from 
    the environment variable "WEBHOOK_URL". If the environment variable 
    is not set, it prints an error message and returns without sending 
    the alert. If the alert message is empty, it also returns without 
    sending the alert. The function constructs a payload with the alert 
    message and sends it as a POST request to the webhook URL. It handles 
    any exceptions that may occur during the request and prints appropriate 
    messages for debugging purposes.
    """
    url = os.getenv("WEBHOOK_URL")
    if not url:
        print("Error: WEBHOOK_URL environment variable is not set.")
        return

    # Check if app_message is empty before sending the alert. 
    # If it is empty, print an error message and return without sending the alert.
    if not app_message:
        print("Error: Alert message is empty.")
        return
    
    # Create a payload dictionary with the alert message to be sent to the webhook. 
    # The payload is structured as a JSON object with a "text" field containing the alert message.
    payload = {"text": app_message}

    # Send the alert message to the specified webhook URL using a POST request. If the request is successful, print the status code of the response. If an exception occurs during the request, catch it and print an error message along with the exception details. Additionally, print the response and the payload for debugging purposes.
    try:
        # Send a POST request to the specified webhook URL with the payload as JSON data. The response from the server is stored in the 'response' variable.
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"webhook sent: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"webhook failed: {e}")
        print("DEBUG payload:", payload)