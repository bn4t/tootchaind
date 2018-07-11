import hashlib
import json
import os
import re
import time
from time import time


class verify(object):

    @staticmethod
    def valid_proof():

        ##########################################################################################################################
        #                                                                                                                         #
        #                                                Edit these values                                                         #
        #                                                                                                                         #
        ##########################################################################################################################

        # Data of the block you want to verify (Example: Block 1245)
        timestamp = 1531293602
        nonce = 56833
        previous_hash = "3a0987f2f3c4f17338743a770e8e90c5ee95daa683311cad83ad90b9249bc664"
        data = []
        
        # Data of the previous block (Example: Block 1244)
        last_block_height = 1244
        last_block_timestamp = 1531293002
        last_block_transactions = []
        last_block_nonce = 64556
        last_block_previous_hash = "da3ac4375d5d65c8477cfda4f5a1bb5aa5d8e8218ad9beb1ad2a81892a27c1ab"


        ##########################################################################################################################
        
        last_block_data = json.dumps({"height":last_block_height, "timestamp":last_block_timestamp, "transactions":last_block_transactions, "nonce":last_block_nonce,
            "previous_hash":last_block_previous_hash}, sort_keys=True).encode()
        
        print(last_block_data)

        last_hash = hashlib.sha256(last_block_data).hexdigest()
        
        

        guess = f'{nonce}{timestamp}{previous_hash}{data}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # Debug
        if guess_hash[:4] == "7007":
            print("Block is valid! ( blockhash: " + guess_hash + " | nonce: " + str(nonce) + " | time: " + str(timestamp) + " | last_hash: " + last_hash + " | data: " + str(data))
        else:
            print("Block is invalid! ( blockhash: " + guess_hash + " | nonce: " + str(nonce) + " | time: " + str(timestamp) + " | last_hash: " + last_hash + " | data: " + str(data))
    

verifyc = verify()

verifyc.valid_proof()