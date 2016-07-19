# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import requests
import json

from block import Block, BlockSummaryPagination
from transaction import Transaction
from exception import APIException, ParamException
from address import Address, UnspentOutput
import utils


class InsightApi(object):
    """
    This class once instantiated allows to make requests to the given insight api instance.

    @ivar address: The address of the instance of the API. It must end with a slash. Example: http://local.lan/api/
    @type address: String
    """

    def __init__(self, address):
        self.address = address

    def make_request(self, url):
        """
        Allows to make get request to the API
        @param url: The
        @return:
        """
        r = requests.get(self.address + url)
        return r

    def get_block(self, block_hash):
        """
        @param block_hash: The hash of the block to get
        @type block_hash: String
        @return: The block from the API
        @rtype: Block
        """
        res = self.make_request('block/' + block_hash)
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        parsed = json.loads(res.text)
        return parsed["rawtx"]

    def get_address(self, address, no_transactions=False, transaction_from=None, transaction_to=None):
        """
        @param address: The address we want to get from the service
        @ivar address: String
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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        if in_satoshis:
            return int(res.text)
        return utils.satoshi_to_bitcoin(res.text)

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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        if in_satoshis:
            return int(res.text)
        return utils.satoshi_to_bitcoin(res.text)

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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        if in_satoshis:
            return int(res.text)
        return utils.satoshi_to_bitcoin(res.text)

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
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        if in_satoshis:
            return int(res.text)
        return utils.satoshi_to_bitcoin(res.text)

    def get_unsent_outputs(self, address):
        """
        @param address: The address to get the details for
        @return: The unspent outputs for the address
        @rtype: [UnspentOutput]
        """
        res = self.make_request('addr/' + address + '/utxo')
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        parsed = json.loads(res.text)
        unspent_list = []
        for unspent_output in parsed:
            unspent_list.append(UnspentOutput(unspent_output))
        return unspent_list
