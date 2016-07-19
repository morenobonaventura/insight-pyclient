# Insight-pyclient

This package allows to interact with the Bitpay's [Insight-API](https://github.com/bitpay/insight-api).

## Usage

In order to use the api, an instance of InsightApi must pe instantiated. 
It takes as parameter the location of the API (with a slash at the end).

`api = InsightApi('http://local.lan/api')`

The module allows (or will) access to all the APIs methods. For more 
details about the content or whatever, you can go see the origin
documentation. The code is also documented so you can go there for 
more details. The following content will just list the prototypes
 callable methods.

### Block

* `Block get_block(Sting blockHash)`
* `String get_block_hash(int blockHeight)`
* `String get_raw_block(String blockHash)`
* `[Block], length, BlockSummaryPagination get_block_summaries(int maxNumber, String date)`

### Transaction

* `Transaction get_transaction(String transaction_hash)`
* `String get_raw_transaction(String transaction hash)`

### Address

* `Address get_address(String address, Bool no_transactions=False, int transaction_from=None, int transaction_to=None)`
* `Int/Float get_address_balance(String address, Boolean inSatoshis=False)`
* `Int/Float get_address_total_received(String address, Boolean inSatoshis=False)`
* `Int/Float get_address_total_sent(String address, Boolean inSatoshis=False)`
* `Int/Float get_address_unconfirmed_balance(String address, Boolean inSatoshis=False)`
* `[UnspentOutput] get_unsent_output_for_many(String[] addresses)`
* `[UnspentOutput] get_unsent_outputs(String address)`
* `[Transaction], totalReturned, returnedFrom, returnedTo get_transaction_for_addresses(String[] addresses, int transaction_from=None, int transaction_to=None)`
* `[Transaction] get_all_transactions_for_address(String address)`

## Advances uses

While using the package, you may want to customize some things. There 
are multiple attributes that allows you to do that. To use it, you may
change some values of your InsightApi instance.

### General

* `timeout`: To define how many time it is going to take before the
request timeout. Is 20 seconds by default.

### Authentication

The basic and digest authentication are supported. If both are activated
the script will prioritize the digest authentication.

* `basicAuth`: Activates the basic authentication, false by default
* `digestAuth`: Activates the digest authentication, false by default
* `userName`: Must be set if the authentication is enabled
* `password`: Must be set if the authentication is enabled

### Try hard mode

Sometimes, having an answer is really important. In this purpose, the 
try mode allows to continue making requests to the service until a valid 
return code is given. Each time the request fails, the time to wait 
before making a request again is configurable.

* `try_hard`: False by default, allows to enable or disable the mode
* `time_multiplier`: Each time the request fails, the time to wait will
 be multiplicated by this value
* `max_wait_time`: The maximum time (in seconds) to wait between two 
requests
* `verbose_try_hard`: If set to True, will print the exception
