# Tootchain


## Block

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
  "height": 123,
  "timestamp": 1530168776,
  "transactions": [
    {
        "sender": "bn4t@toot.cafe",
        "data": "Hello World!"
    }
  ],
  "nonce": 1234,
  "previous_hash": "7fdcde7c3f0db44f3f7ff62b0d0ecc828536b8576f48ab690e6a49adaecc5105"
}
````