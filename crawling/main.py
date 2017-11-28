import os
import json
import logging

from slackclient import SlackClient
from crawling import crawling


# slack_channel = os.getenv('SLACK_CHANNEL')
# slack_token = os.getenv('SLACK_TOKEN')

# if slack_channel is None:
#     raise Exception('Expected to find slack channel at environment variable \
#                      SLACK_CHANNEL, found nothing')
# if slack_token is None:
#     raise Exception('Expected to find slack token at environment variable \
#                      SLACK_TOKEN, found nothing')


class SlackBot:
    def __init__(self, channel):
        self.channel = channel
        self.slack_client = SlackClient(slack_token)

    def upload_file(self, file, filename=None):
        self.slack_client.api_call(
            "files.upload",
            as_user=True,
            channels=self.channel,
            filename=filename,
            file=file,
        )

    def send_message(self, message):
        self.slack_client.api_call(
            'chat.postMessage',
            as_user=True,
            channels=self.channel,
            text=message,
        )


def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info("Event: " + str(event))
    message = crawling()
    logger.info("Message: " + str(message))

    return message

    # bot = SlackBot(slack_channel)
    # bot.send_message(message)
