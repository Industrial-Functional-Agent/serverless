import os
import json
import logging

from slackclient import SlackClient

from crawling import Crawler
from post_process import post_process


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
    crawler = Crawler()
    crawler.load_phantom(os.path.join(os.getcwd(),
                                      'phantomjs-2.1.1-linux-x86_64',
                                      'bin',
                                      'phantomjs'))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info("Event: " + str(event))
    message = crawler.crawling()
    message = post_process(message)
    logger.info("Message: " + str(message))

    return message

    # bot = SlackBot(slack_channel)
    # bot.send_message(message)
