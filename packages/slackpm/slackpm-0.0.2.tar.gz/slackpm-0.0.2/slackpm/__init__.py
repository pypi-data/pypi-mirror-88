import json
import requests


def send_message(webhook_url, subject, message):
    slack_data = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": subject
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }

    try:
        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'ERROR: Request to Slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
    except Exception as e:
        print(f'ERROR: Failed posting message!\nMessage - {e}')


def send_plain_message(webhook_url, message):
    slack_data = {'text': message}

    try:
        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'ERROR: Request to Slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
    except Exception as e:
        print(f'ERROR: Failed posting message!\nMessage - {e}')
