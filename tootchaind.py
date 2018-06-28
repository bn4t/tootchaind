import hashlib
import json
import time
from time import time
import os
import re
from mastodon import Mastodon
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup


class Tootchaind:
    def __init__(self):
        self.pending_tx = []
        self.mastodon = None
        self.instance_url = 'https://toot.cafe'

        self.initialize_mastodon()

    def gen_genesis_block(self, nonce):
        # create the block
        block = {
            'index': 1,
            'timestamp': int(time.time()),
            'transactions': [],
            'nonce': nonce,
            'previous_hash': '0000000000000000000000000000000000000000000000000000000000000000',
        }

        # Toot the formatted block
        self.mastodon.status_post(json.dumps(block), visibility='unlisted')

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
            email = "tootchain@topikt.com"
            password = "tootchain@topikt.com"
            self.mastodon.log_in(email, password, to_file='user_cred.txt')

        # initialize Mastodon Client
        self.mastodon = Mastodon(
            client_id='client_cred.txt',
            access_token='user_cred.txt',
            api_base_url=self.instance_url
        )
