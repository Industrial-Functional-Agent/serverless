import logging
import os

from crawling import Crawler
from slack_bot import SlackBot

slack_channel = os.getenv('SLACK_CHANNEL')
slack_token = os.getenv('SLACK_TOKEN')

if slack_channel is None:
    raise Exception('Expected to find slack channel at environment variable \
                     SLACK_CHANNEL, found nothing')
if slack_token is None:
    raise Exception('Expected to find slack token at environment variable \
                     SLACK_TOKEN, found nothing')


def handler(event, context):
    crawler = Crawler()
    crawler.load_phantom(os.path.join(os.getcwd(),
                                      'bin',
                                      'phantomjs'))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info("Event: " + str(event))
    posts = crawler.crawling()
    text = "\n".join(map(str, posts))
    logger.info("Message: " + text)

    if posts:
        bot = SlackBot(slack_token, slack_channel)
        a = bot.send_message(text)

        return a
