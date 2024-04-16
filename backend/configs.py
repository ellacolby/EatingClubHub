import requests
import json
import base64
import os
import dotenv

dotenv.load_dotenv()

class Configs:
    def __init__(self):
        self.CONSUMER_KEY = os.environ['CONSUMER_KEY']
        self.CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
        self.BASE_URL= os.environ['BASE_URL']
        self.REFRESH_TOKEN_URL= os.environ['REFRESH_TOKEN_URL']
        self.USERS = "/users"
        self._refreshToken(grant_type="client_credentials")

    def _refreshToken(self, **kwargs):
        req = requests.post(
            self.REFRESH_TOKEN_URL, 
            data=kwargs, 
            headers={
                "Authorization": "Basic " + base64.b64encode(bytes(self.CONSUMER_KEY + ":" + self.CONSUMER_SECRET, "utf-8")).decode("utf-8")
            },
        )
        text = req.text
        response = json.loads(text)
        self.ACCESS_TOKEN = response["access_token"]