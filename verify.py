import hashlib
import json
import time
from time import time
import os
import re
from mastodon import Mastodon
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup


class Verify:

    def __init__(self):
        print("starting")
        print(self.last_hash())

    def last_block(self):
        json_tl = self.mastodon.timeline_home(limit=1)

        return json.loads(self.unescape_text(
            self.clean_html(json_tl[0]['content'])))  # returns the latest block from the timeline formatted as json

    def last_block_index(self):
        last_block_json = self.last_block()
        return int(last_block_json['index'])

    def last_proof(self):
        last_block_json = self.last_block()
        return int(last_block_json['proof'])

    def last_hash(self):

        print("last Hash:" + self.hash(self.last_block()))
        return str(self.hash(self.last_block()))

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
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

        if guess_hash[:4] == "0000":
            print(str(last_proof) + " | " + str(proof) + " | " + guess_hash)
        return guess_hash[:4] == "0000"

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
