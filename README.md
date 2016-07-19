# Insight-pyclient

This package allows to interact with the Bitpay's [Insight-API](https://github.com/bitpay/insight-api).

# Usage

In order to use the api, an instance of InsightApi must pe instantiated. It takes as parameter the location of the API
(with a slash at the end).

`api = InsightApi('http://local.lan/api')`

The module allows (or will) access to all the APIs methods. For more details about the content or whatever, you can go
see the origin documentation. The code is also documented so you can go there for more details. The following content
will just list the prototypes callable methods.

## Block

* `Block get_block(Sting blockHash)`
* `String get_block_hash(int blockHeight)`
* `String get_raw_block(String blockHash)`
* `[Block], length, BlockSummaryPagination get_block_summaries(int maxNumber, String date)`

## Transaction

* `Transaction get_transaction(String transaction_hash)`
* `String get_raw_transaction(String transaction hash)`

## Address

* `Address get_address(String address, Bool no_transactions=False, int transaction_from=None, int transaction_to=None)`
* `Int/Float get_address_balance(String address, Boolean inSatoshis=False)`
* `Int/Float get_address_total_received(String address, Boolean inSatoshis=False)`
* `Int/Float get_address_total_sent(String address, Boolean inSatoshis=False)`
* `Int/Float get_address_unconfirmed_balance(String address, Boolean inSatoshis=False)`
* `UnspentOutput get_unsent_outputs(String address)`
* `[UnspentOutput] get_unsent_output_for_many(String[] addresses)`
