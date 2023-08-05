import ssl
import certifi
import slack
from slack.errors import SlackApiError
from django.conf import settings


class SlackBot:
    def __init__(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = slack.WebClient(token=settings.SLACK_TOKEN, ssl=ssl_context)
        self.id = self.client.api_call('auth.test')['user_id']

    def send_message(self, channel_id, message):
        try:
            if isinstance(message, str):
                response = self.client.chat_postMessage(channel=channel_id, text=message)
            else:
                response = self.client.chat_postMessage(channel=channel_id, **message)
            if response["ok"]:
                print(f"Message sent to channel {channel_id}")
                return True
            else:
                print(f"Failed to send message to user {channel_id}. Error: {response['error']}")
                return False
        except SlackApiError as e:
            print(f"Error sending message to user {channel_id}: {e}")
            return False

    def get_users_in_channel(self, channel_id):
        try:
            response = self.client.conversations_members(channel=channel_id)
            users = response["members"]
            return users
        except SlackApiError as e:
            print(f"Error fetching users in channel {channel_id}: {e}")
            return []

    def get_bot_channel(self, channel_name):
        try:
            response = self.client.conversations_list(types="public_channel,private_channel")
            channels = response["channels"]

            for channel in channels:
                if channel['name'] == channel_name:
                    return channel
            return None
        except SlackApiError as e:
            print(f"Error fetching bot channels: {e}")
            return None