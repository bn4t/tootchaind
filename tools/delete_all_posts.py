import json
import os
import re
from time import time

from mastodon import Mastodon


class Tootchaind:

    def __init__(self):
        self.mastodon = None

        # instance url
        self.instance_url = os.environ['INSTANCE_URL']

        # To make this bot working add the credentials of an account
        self.username = os.environ['BOT_USERNAME']
        self.email = os.environ['BOT_EMAIL']
        self.password = os.environ['BOT_PW']

        self.initialize_mastodon()

    # initialize Mastodon
    def initialize_mastodon(self):
        if not os.path.isfile("client_cred.txt"):
            print("Creating app")
            self.mastodon = Mastodon.create_app(
                'tootchaind',
                to_file='client_cred.txt',
                api_base_url=self.instance_url
            )

        # Fetch access token if I didn't already
        if not os.path.isfile("user_cred.txt"):
            print("Logging in")
            self.mastodon = Mastodon(
                client_id='client_cred.txt',
                api_base_url=self.instance_url
            )

            self.mastodon.log_in(self.email, self.password, to_file='user_cred.txt')

        # initialize Mastodon Client
        self.mastodon = Mastodon(
            client_id='client_cred.txt',
            access_token='user_cred.txt',
            api_base_url=self.instance_url
        )

    def delete_all_statuses(self):
        
        Mastodon.status_delete(id)
  

tootchain = Tootchaind()
