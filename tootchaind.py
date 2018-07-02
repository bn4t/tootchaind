import hashlib
import json
import os
import re
import time
from time import time

from bs4 import BeautifulSoup
from mastodon import Mastodon


class Tootchaind:

    def __init__(self):
        self.pending_tx = []
        self.mastodon = None

        # instance url
        self.instance_url = os.environ['INSTANCE_URL']

        # To make this bot working add the credentials of an account
        self.username = os.environ['BOT_USERNAME']
        self.email = os.environ['BOT_EMAIL']
        self.password = os.environ['BOT_PW']

        self.initialize_mastodon()

        # generate genesis block if there is no previous one
        timeline = self.mastodon.timeline_home()
        if len(timeline) < 1:
            self.gen_genesis_block()
            return

        # retrieve txs and create a block
        self.retrieve_tx()
        self.create_block()

    # create the genesis block
    def gen_genesis_block(self):

        nonce = self.proof_of_work('0000000000000000000000000000000000000000000000000000000000000000', [])

        block = {
            'height': 0,
            'timestamp': int(time()),
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

            self.mastodon.log_in(self.email, self.password, to_file='user_cred.txt')

        # initialize Mastodon Client
        self.mastodon = Mastodon(
            client_id='client_cred.txt',
            access_token='user_cred.txt',
            api_base_url=self.instance_url
        )

    # create new transaction
    def new_transaction(self, sender, data):

        tx_data = sender + data

        # Enforce 70 character limit per tx so blocks don't exceed the 500 characters which fit into a toot
        if len(tx_data) > 70:
            return False

        self.pending_tx.append({
            'sender': sender,
            'data': data,
        })

        return True

    # create a new block
    def create_block(self):

        to_include_transactions = []

        # Choose transactions to include in block
        for _ in range(3):

            # check if array is empty
            if self.pending_tx:
                # add transaction to block and remove it from the array
                to_include_transactions.append(self.pending_tx[0])
                self.pending_tx.pop(0)

        previous_hash = self.last_hash()
        nonce = self.proof_of_work(previous_hash, to_include_transactions)

        # create the block
        block = {
            'height': self.block_height() + 1,
            'timestamp': int(time()),
            'transactions': to_include_transactions,
            'nonce': nonce,
            'previous_hash': previous_hash,
        }

        # Toot the formatted block
        self.mastodon.status_post(json.dumps(block), visibility='unlisted')

    # calculates the nonce
    def proof_of_work(self, previous_hash, data):

        nonce = 0
        while self.valid_proof(nonce, previous_hash, data) is False:
            nonce += 1

        return nonce

    def retrieve_tx(self):
        json_notif = self.mastodon.notifications()

        # iterate through notifications
        for i, current_notif in enumerate(json_notif):
            notif_id = current_notif['id']

            # check if the notification type is mention
            if current_notif['type'] == 'mention':

                # fill in variables
                username = str(current_notif['account']['username'])
                content = str(current_notif['status']['content'])

                startswith_string = '<p><span class="h-card"><a href="' + self.instance_url + '/@' + self.username + '" class="u-url mention">@<span>' + self.username + '</span></a></span> !tx '

                # check if the correct command is used
                if content.startswith(startswith_string):

                    # use substring of content without the command and mention
                    data = content[len(startswith_string):]
                    clean_data = self.clean_html(data)

                    # only include transaction if it doesn't exceeds the length limit
                    if self.new_transaction(username, clean_data):
                        print("processed tx")

                        # exit loop after processing 3 notifications
                        if i is 2:
                            return

            # delete notification no matter what type it is
            self.mastodon.notifications_dismiss(notif_id)

    #####################################
    #               Utils               #
    #####################################

    def last_block(self):
        json_tl = self.mastodon.timeline_home(limit=1)

        return json.loads(self.unescape_text(
            self.clean_html(json_tl[0]['content'])))  # returns the latest block from the timeline formatted as json

    @staticmethod
    def unescape_text(text):

        soup = BeautifulSoup(text, "html.parser")
        return soup.text

    @staticmethod
    def clean_html(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def block_height(self):
        last_block_json = self.last_block()
        return int(last_block_json['height'])

    def last_hash(self):
        block = self.last_block()

        blockdata = json.dumps(block, sort_keys=True).encode()
        blockhash = hashlib.sha256(blockdata).hexdigest()

        return blockhash

    @staticmethod
    def valid_proof(nonce, previous_blockhash, data):
        timestamp = int(time())

        guess = f'{nonce}{timestamp}{previous_blockhash}{data}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # Debug
        if guess_hash[:4] == "7007":
            print("guessed hash: " + guess_hash + " | nonce: " + str(
                nonce) + " | time: " + str(timestamp) + " | prev_hash: " + previous_blockhash + " | data: " + str(data))

        return guess_hash[:4] == "7007"


blockchain = Tootchaind()
