import hashlib
import json
import time
from time import time
import os
import re
from mastodon import Mastodon
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup


class Blockchain:

    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        self.mastodon = None
        self.instance_url = 'https://toot.cafe'

        self.initialize_mastodon()


    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        to_mine_transactions = []

        # Choose transactions to include in block
        for _ in range(3):

            # check if array is empty
            if self.current_transactions:
                # add transaction to block and remove it from the array
                to_mine_transactions.append(self.current_transactions[0])
                self.current_transactions.pop(0)


        # create the block
        block = {
            'index': self.last_block_index()+1,
            'timestamp': time(),
            'transactions': to_mine_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }

        # Toot the formatted block
        self.mastodon.status_post(json.dumps(block, indent=2, sort_keys=True), visibility='unlisted')

        # Append the block to the chain
        # self.chain.append(block)
        return block

    def new_transaction(self, sender, data):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param data: data
        :return: The index of the Block that will hold this transaction
        """

        # Enforce 40 character limit so blocks don't exceed the 500 characters which fit into a toot
        if len(data) > 50:
            print("Max. character limit is 40!")
            return

        self.current_transactions.append({
            'sender': sender,
            'data': data,
        })

        return self.last_block_index() + 1

    def last_block(self):
        json_tl = self.mastodon.timeline_home(limit=1)

        return json.loads(self.unescape_text(self.clean_html(json_tl[0]['content'])))  # returns the latest block from the timeline formatted as json

    def last_block_index(self):
        last_block_json = self.last_block()
        return int(last_block_json['index'])

    def last_proof(self):
        last_block_json = self.last_block()
        return int(last_block_json['proof'])

    def last_hash(self):
        return str(self.hash(self.last_block()))

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(str(block), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
        """

        last_proof = self.last_proof()
        last_hash = self.last_hash()

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    # initialize Mastodon
    def initialize_mastodon(self):
        if not os.path.isfile("bot_clientcred.txt"):
            print("Creating app")
            self.mastodon = Mastodon.create_app(
                'tootchaind',
                to_file='bot_clientcred.txt',
                api_base_url=self.instance_url
            )

        # Fetch access token if I didn't already
        if not os.path.isfile("bot_usercred.txt"):
            print("Logging in")
            self.mastodon = Mastodon(
                client_id='bot_clientcred.txt',
                api_base_url=self.instance_url
            )
            email = "zawuzeme@99pubblicita.com"
            password = "zawuzeme@99pubblicita.com"
            self.mastodon.log_in(email, password, to_file='bot_usercred.txt')

        self.mastodon = Mastodon(
            client_id='bot_clientcred.txt',
            access_token='bot_usercred.txt',
            api_base_url=self.instance_url
        )

    def unescape_text(self, text):
        """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""

        soup = BeautifulSoup(text, "html.parser")
        return soup.text

    def chunks(s, n):
        """Produce `n`-character chunks from `s`."""
        for start in range(0, len(s), n):
            yield s[start:start + n]

    def clean_html(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def get_notifications(self):
        json_notif = self.mastodon.notifications()

        # iterate through notifications
        for i, current_notif in enumerate(json_notif):
            # check if the notification type is mention
            if current_notif['type'] == 'mention':

                # fill in variables
                username = str(current_notif['account']['username'])
                content = str(current_notif['status']['content'])

                # check if the correct command is used
                if content.startswith('<p><span class="h-card"><a href="https://toot.cafe/@testblckchn" class="u-url '
                                      'mention">@<span>testblckchn</span></a></span> !tx '):
                    # use substring of content without the command
                    data = content[128:]
                    clean_data = self.clean_html(data)

                    self.new_transaction(username, clean_data)
                    print("finished notification")

        # clear notifications
        self.mastodon.notifications_clear()


# Instantiate the Node
app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work()

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.last_hash()
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/newtx', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['data'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


# check for new mentions
@app.route('/mention', methods=['GET'])
def check_for_new_tx():
    blockchain.get_notifications()
    return "t"


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

app.run(host='0.0.0.0', port=port)
