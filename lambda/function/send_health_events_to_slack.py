import boto3
from botocore.config import Config
import os

from slack_sdk import WebClient

def notify(slack_token, slack_channel, message):
    client = WebClient(token=slack_token)
    client.chat_postMessage(
        channel=slack_channel,
        blocks = blocks(message),
        text = f"{message.service} {message.eventType}",
    )

def get_token():
    aws_config = Config(
        region_name=os.environ.get('AWS_REGION'),
    )
    secret_manager = boto3.client('secretsmanager', config=aws_config)
    secret_response = secret_manager.get_secret_value(
            SecretId = os.environ.get('SLACK_TOKEN_ARN'),
        )

    return secret_response["SecretString"]

def blocks(message):
    blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":alert: An event has occurred on the AWS Health Dashboard :alert:" if message.alert else "An event has occurred on the AWS Health Dashboard"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Event Type*: `{message.eventType}` *Service*: `{message.service}` \n*Account*: `{message.account}` *Region*: `{message.region}`"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message.description.replace("\\n", "\n")
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Further details can be found on the <{message.url}|Health Dashboard>"
                }
            }
        ]
    return blocks

class Message:
    def __init__(self, event):
        self.account = event['account']
        self.alert = False
        self.region = event['region']
        self.service = event['detail']['service']
        self.url = str("https://phd.aws.amazon.com/phd/home#/account/event-log?eventID=" + event['detail']['eventArn'])

        if len(event['detail']['eventDescription'][0]['latestDescription']) > 3000:
            self.description = "Event description exceeds character limit."
        else:
            self.description = event['detail']['eventDescription'][0]['latestDescription']


        if 'eventTypeCategory' in event['detail']:
            match event['detail']['eventTypeCategory']:
                case "accountNotification":
                    self.eventType = "Notification"
                case "issue":
                    self.eventType = "Issue"
                    self.alert = True
                case "scheduledChange":
                    self.eventType = "Scheduled Change"
                case "":
                    self.eventType = "Unknown"
                case _:
                    self.eventType = event['detail']['service']
        else:
            self.eventType = event['detail']['service']



def lambda_handler(event, context):
    print(event)
    slack_token = get_token()
    slack_channel = os.environ['SLACK_CHANNEL']
    message = Message(event)
    notify(slack_token, slack_channel, message)
