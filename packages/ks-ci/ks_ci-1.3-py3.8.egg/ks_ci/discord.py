"""
Module handles Dicord functionality
"""
import json
import requests

class DiscordEndpointNotSupported(Exception):
    pass

class DiscordAPI():

    base_url = "https://discordapp.com/api/"

    def __init__(self, channel_id, bot_token):
        self.channel_id = channel_id
        self.bot_token = bot_token

    def get_headers(self):
        return  { "Authorization":"Bot {}".format(self.bot_token),
            "User-Agent":"",
            "Content-Type":"application/json", }
    

    def get_api_url(self, endpoint):
        if endpoint == 'messages':
            return "{}/channels/{}/messages".format(self.base_url, self.channel_id)
        else:
            raise DiscordEndpointNotSupported

    def send_message(self, content):
        json_payload =  json.dumps({"content": content})
        r = requests.post(self.get_api_url('messages'), headers = self.get_headers(), data = json_payload)
