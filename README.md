[![pipeline status](https://gitlab.com/bn4t/tootchaind/badges/master/pipeline.svg)](https://gitlab.com/bn4t/tootchaind/commits/master)

# Tootchain

This is a bot running on the [Mastodon](https://joinmastadon.org) network with which you can store messages on a cryptographically verifiable blockchain.
The blockchain is also stored on Mastodon.

___
To create a so called transaction send a toot in following format:

`@tootchain@toot.cafe !tx YOUR_MESSAGE`


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

**Note:** The `previous_hash` field is differently generated. See [here](https://gitlab.com/bn4t/tootchaind/blob/master/tootchaind.py#L195).

### Genesis Block

The genesis blockhash is `0000000000000000000000000000000000000000000000000000000000000000`

### Structure

Structure of a block

````
{
  "height": 84,
  "timestamp": 1530597001,
  "transactions": [
      {
      "sender": "bn4t",
      "data": "Hello World!"
    }
  ],
  "nonce": 44973,
  "previous_hash": "3bf51b443e872ad38e041a4537e10fcd515000eb3cefea6dbc5f5e6bbfcf2955"
}
````

# Verify blocks

At the moment, blocks can unfortuantely only be verified manually, due to mastodons API limitations.

To verify a block you can use the [verify.py](https://gitlab.com/bn4t/tootchaind/blob/master/verify.py) script.

# Set up your own Tootchain bot

## Installation

The easiest way is to use the provided Docker image.

Run the image:

````
docker run --detach \
    --name tootchaind \
    --restart always \
    --env INSTANCE_URL=https://your.instance \
    --env BOT_EMAIL=bot@example.com \
    --env BOT_USERNAME=username \
    --env BOT_PW=your_password \
    registry.gitlab.com/bn4t/tootchaind:latest
````

## Adjust block time

To adjust the block time, you need to clone the repo, 
set the cron interval (found in `crontab.txt`) to your desired value and build the image.


# Thanks

I would like to thank [@Nolan](https://toot.cafe/@nolan) (Owner of toot.cafe Mastodon instance) for giving me permission to run this bot on his instance.

Thank you Nolan!
