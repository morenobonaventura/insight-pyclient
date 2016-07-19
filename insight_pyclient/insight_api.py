# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import requests
import json
import time
import traceback

from requests.auth import HTTPDigestAuth

from .block import Block, BlockSummaryPagination
from .transaction import Transaction
from .exception import APIException, ParamException
from .address import Address, UnspentOutput
from .utils import *


class InsightApi(object):
    """
    This class once instantiated allows to make requests to the given insight api instance.

    @ivar address: The address of the instance of the API. It must end with a slash. Example: http://local.lan/api/
    @type address: String
    @ivar try_hard: If this option is enabled, the requests will be done in loop while it does not return an http \
    code equal to 200. See make_request for more details
    @type try_hard: Boolean
    @ivar time_multiplier: How the wait time (seconds) will increase with try_hard between each request
    @ivar max_wait_time: The maximum time (seconds) to wait between two requests in try_hard mode
    @ivar verbose_try_hard: To display the stacktrace and the incriminated URL when request fails
    @ivar timeout: The timeout for the requests in seconds
    @ivar basicAuth: Allows to enable a basic HTTP authentication
    @type basicAuth: Boolean
    @ivar digestAuth: Allows to enable a digest HTTP authentication
    @type digestAuth: Boolean
    @ivar userName: The username that will be used if the digest or the basic authentication is enabled
    @type userName: String
    @ivar password: The password that will be used if the digest or the basic authentication is enabled
    @type password: String
    """

    def __init__(self, address, try_hard=False):
        self.address = address
        self.try_hard = try_hard
        self.time_multiplier = 2
        self.max_wait_time = 120
        self.verbose_try_hard = False
        self.timeout = 1
        self.basicAuth = False
        self.digestAuth = False
        self.userName = None
        self.password = None

    def make_request(self, url, wait_time=1, expected_http_return=200):
        """
        Allows to make get request to the API. It can make usage of the try hard option that allows to continue making \
        requests util is get
        @param url: The url to request
        @param wait_time: The time (seconds) to wait before making another request if the try_hard option is enabled
        @type wait_time: Int
        @param expected_http_return: Allows to throw an exception if the http return code is not equal to it
        @type expected_http_return: int
        @return: The result given by the request module
        """
        try:
            if self.digestAuth:
                res = requests.get(self.address + url, timeout=self.timeout, auth=(self.userName, self.password))
            elif self.basicAuth:
                res = requests.get(self.address + url, timeout=self.timeout, auth=HTTPDigestAuth(self.userName, self.password))
            else:
                res = requests.get(self.address + url, timeout=self.timeout)
            if res.status_code != expected_http_return:
                raise APIException("Wrong status code", res.status_code, res.text, url)
            return res
        except Exception as ex:
            if not self.try_hard:
                raise ex
            if self.verbose_try_hard:
                print(traceback.format_exc())
                print('Waiting ' + str(wait_time) + ' seconds before next request.')
            time.sleep(wait_time)
            wait_time *= self.time_multiplier
            if wait_time > self.max_wait_time:
                wait_time = self.max_wait_time
            return self.make_request(url, wait_time, expected_http_return)

    def get_block(self, block_hash):
        """
        @param block_hash: The hash of the block to get
        @type block_hash: String
        @return: The block from the API
        @rtype: Block
        """
        res = self.make_request('block/' + block_hash)
        block = Block(res.text)
        return block

    def get_block_hash(self, height):
        """
        @param height: The height of the block to get
        @type height: Int
        @return: The hash of the block
        @rtype: String
        """
        res = self.make_request('block-index/' + str(height))
        parsed = json.loads(res.text)
        return parsed["blockHash"]

    def get_raw_block(self, block_hash):
        """
        @param block_hash: The hash of the block to get
        @type block_hash: Int
        @return: The raw block
        @rtype: String
        """
        res = self.make_request('rawblock/' + block_hash)
        parsed = json.loads(res.text)
        return parsed["rawblock"]

    def get_block_summaries(self, max_number, date):
        """
        Returns the summaries of the blocks for the given day
        @param max_number: The maximum number of blocks to get
        @type max_number: Integer
        @param date: The date we are interested in
        @type date: String [YYYY-MM-DD]
        @return: A list of light blocks
        @rtype: [Block]
        """
        res = self.make_request('blocks?limit=' + str(max_number) + '&blockDate=' + date)
        list_res = []
        parsed = json.loads(res.text)
        for light_json_block in parsed["blocks"]:
            tmp = Block()
            tmp.parse_summary(light_json_block)
            list_res.append(tmp)
        return list_res, parsed["length"], BlockSummaryPagination(parsed["pagination"])

    def get_transaction(self, transaction_hash):
        """
        @param transaction_hash: The hash of the transaction to get
        @type transaction_hash: String
        @return: The transaction from the API
        @rtype: Transaction
        """
        res = self.make_request('tx/' + transaction_hash)
        tx = Transaction(res.text)
        return tx

    def get_raw_transaction(self, transaction_hash):
        """
        @param transaction_hash: The hash of the transaction to get
        @type transaction_hash: String
        @return: The raw transaction
        @rtype: String
        """
        res = self.make_request('rawtx/' + transaction_hash)
        parsed = json.loads(res.text)
        return parsed["rawtx"]

    def get_address(self, address, no_transactions=False, transaction_from=None, transaction_to=None):
        """
        @param address: The address we want to get from the service
        @param no_transactions: If we don't want to load the transactions for this address. False by default
        @param no_transactions: Boolean
        @param transaction_from: Load the transactions hash from transaction number. Not needed by default
        @param transaction_from: int
        @param transaction_to: Load the transactions hash until transaction number. Not needed by default
        @param transaction_to: int
        @return: The formated details about the address
        @rtype: Address
        """
        request_string = "addr/" + address + "?"
        if no_transactions and (transaction_from is not None or transaction_to is not None):
            raise ParamException("You can't ask no transaction and give a range for it")
        if no_transactions:
            request_string += 'noTxList=1'
        if transaction_from is not None:
            request_string += 'from=' + str(transaction_from) + '&'
        if transaction_to is not None:
            request_string += 'to=' + str(transaction_to)
        res = self.make_request(request_string)
        result = Address(res.text)
        return result

    def get_address_balance(self, address, in_satoshis=False):
        """
        @param address: The address we wish to get details from
        @type address: String
        @param in_satoshis: If we want to get the result in Satoshis, False by default
        @type in_satoshis: Boolean
        @return: The actual balance of the address
        @rtype: Float if we returns Bitcoins, else Int
        """
        res = self.make_request('addr/' + address + '/balance')
        if in_satoshis:
            return int(res.text)
        return satoshi_to_bitcoin(res.text)

    def get_address_total_received(self, address, in_satoshis=False):
        """
        @param address: The address we wish to get details from
        @type address: String
        @param in_satoshis: If we want to get the result in Satoshis, False by default
        @type in_satoshis: Boolean
        @return: Returns the total sum of money received by this address
        @rtype: Float if we returns Bitcoins, else Int
        """
        res = self.make_request('addr/' + address + '/totalReceived')
        if in_satoshis:
            return int(res.text)
        return satoshi_to_bitcoin(res.text)

    def get_address_total_sent(self, address, in_satoshis=False):
        """
        @param address: The address we wish to get details from
        @type address: String
        @param in_satoshis: If we want to get the result in Satoshis, False by default
        @type in_satoshis: Boolean
        @return: Returns the total sum of money sent by this address
        @rtype: Float if we returns Bitcoins, else Int
        """
        res = self.make_request('addr/' + address + '/totalSent')
        if in_satoshis:
            return int(res.text)
        return satoshi_to_bitcoin(res.text)

    def get_address_unconfirmed_balance(self, address, in_satoshis=False):
        """
        @param address: The address we wish to get details from
        @type address: String
        @param in_satoshis: If we want to get the result in Satoshis, False by default
        @type in_satoshis: Boolean
        @return: Returns the total unconfirmed balance for the address
        @rtype: Float if we returns Bitcoins, else Int
        """
        res = self.make_request('addr/' + address + '/unconfirmedBalance')
        if in_satoshis:
            return int(res.text)
        return satoshi_to_bitcoin(res.text)

    def get_unsent_outputs(self, address):
        """
        @param address: The address to get the details for
        @return: The unspent outputs for the address
        @rtype: [UnspentOutput]
        """
        res = self.make_request('addr/' + address + '/utxo')
        parsed = json.loads(res.text)
        unspent_list = []
        for unspent_output in parsed:
            unspent_list.append(UnspentOutput(unspent_output))
        return unspent_list

    def get_unsent_output_for_many(self, addresses):
        """
        @param addresses: The addresses to get the details for
        @type addresses: [String]
        @return: The unspent outputs for the addresses
        @rtype: [UnspentOutput]
        """
        formated_addresses = ','.join(addresses)
        res = self.make_request('addrs/' + formated_addresses + '/utxo')
        parsed = json.loads(res.text)
        unspent_list = []
        for unspent_output in parsed:
            unspent_list.append(UnspentOutput(unspent_output))
        return unspent_list

    def get_transaction_for_addresses(self, addresses, transactions_from=None, transactions_to=None):
        """
        @param addresses: The addresses we wish to get transactions from
        @param transactions_from: If we don't want to load the transactions for this address. False by default
        @type transactions_from: nullable int
        @param transactions_to: Load the transactions hash until transaction number. Not needed by default
        @type transactions_to: nullable int
        @return: A maximum of 50 transactions, the numbers of transactions, transactions from and to
        @rtype: [Transaction], int, int, int
        """
        formated_addresses = ','.join(addresses)
        request_string = 'addrs/' + formated_addresses + '/txs?'
        if transactions_from is not None:
            request_string += 'from=' + str(transactions_from) + '&'
        if transactions_to is not None:
            request_string += 'to=' + str(transactions_to)
        res = self.make_request(request_string)
        parsed = json.loads(res.text)
        transactions_list = []
        for transaction in parsed["items"]:
            transactions_list.append(Transaction(transaction, True))
        return transactions_list, parsed["totalItems"], parsed["from"], parsed["to"]

    def get_all_transactions_for_address(self, address, tx_from=0, tx_to=50):
        """
        Allows to get all the transactions for an address using the get_transaction_for_address method.
        @param address: The address to get the transactions from
        @type address: String
        @param tx_from: Used in the recursion
        @param tx_to: Used in the recursion
        @return: The transactions for the address
        @rtype: [Transaction]
        """
        transactions, total, tx_from, tx_to = self.get_transaction_for_addresses([address], tx_from, tx_to)
        if tx_to >= total:
            return transactions
        return transactions + self.get_all_transactions_for_address(address, tx_from + 50, tx_to + 50)
