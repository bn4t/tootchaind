# Tootchain

**This bot is currently in beta. The blockchain might be deleted at any time.**

This is a bot running on the [Mastodon](https://joinmastadon.org) network with which you can store messages on a cryptographically verifiable blockchain.
The blockchain is also stored on Mastodon.

___
To create a so called transaction send a toot in following format:

`@tootchain_test@toot.cafe !tx YOUR_MESSAGE`


## Technical info

- **Block time:** 10 minutes
- **Max tx/block:** 3 transactions
- **Hash function:** sha256

### Blockhash

The blockhash is calculated using following method:
````
blockhash = sha256([NONCE][TIMESTAMP][PREV_BLOCKHASH][DATA])
````

Every blockhash starts with `7007` (`TOOT` written in numbers)

### Genesis Block

The genesis blockhash is `0000000000000000000000000000000000000000000000000000000000000000`

### Structure

Structure of a block

````
{
  "height": 3,
  "timestamp": 1530187688,
  "transactions": [
    {
      "sender": "bn4t",
      "data": "Hello World!"
    }
  ],
  "nonce": 131384,
  "previous_hash": "700766aa540f604809a86db178d1c96dccaea5af45632c47fe310382b268a71d"
}
````