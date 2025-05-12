from slack_sdk.webhook import WebhookClient
import os
from dotenv import load_dotenv

load_dotenv()


# Replace with your actual Slack Webhook URL
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')


def send_slack_alert(message):
    """Send an alert to a Slack channel via webhook."""
    webhook = WebhookClient(SLACK_WEBHOOK_URL)
    response = webhook.send(text=message)
    if response.status_code != 200:
        print(f"Failed to send Slack alert: {response.body}")
