from slackclient import SlackClient


class SlackBot:
    def __init__(self, slack_token, channel):
        self.channel = channel
        self.slack_client = SlackClient(slack_token)

    def upload_file(self, file, filename=None):
        return self.slack_client.api_call(
            "files.upload",
            as_user=True,
            channels=self.channel,
            filename=filename,
            file=file,
        )

    def send_message(self, message):
        return self.slack_client.api_call(
            'chat.postMessage',
            as_user=True,
            channel=self.channel,
            text=message,
        )