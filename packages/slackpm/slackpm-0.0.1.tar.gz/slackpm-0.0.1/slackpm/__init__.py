import json
import requests


def send_message(webhook_url, message):
    slack_data = {'text': message}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'ERROR: Request to Slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
