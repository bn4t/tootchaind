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