# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import requests
from block import Block, BlockSummaryPagination
from exception import APIException
import json


class InsightApi(object):
    """
    This class one instantiated allows to make requests to the given insight api instance.

    @ivar address: The address of the instance of the API. It must end with a slash. Example: http://local.lan/api/
    @type address: String
    """

    def __init__(self, address):
        self.address = address

    def make_request(self, url):
        """
        Allows to make get request to the API
        :param url: The
        :return:
        """
        r = requests.get(self.address + url)
        return r

    def get_block(self, block_hash):
        """
        :param block_hash: The hash of the block to get
        :type block_hash: String
        :return: The block from the API
        :rtype: Block
        """
        res = self.make_request('block/' + block_hash)
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        block = Block(res.text)
        return block

    def get_block_hash(self, height):
        """
        :param height: The height of the block to get
        :type height: Int
        :return: The hash of the block
        :rtype: String
        """
        res = self.make_request('block-index/' + str(height))
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        parsed = json.loads(res.text)
        return parsed["blockHash"]

    def get_raw_block(self, block_hash):
        """
        :param block_hash: The hash of the block to get
        :type block_hash: Int
        :return: The raw block
        :rtype: String
        """
        res = self.make_request('rawblock/' + block_hash)
        if res.status_code != 200:
            raise APIException("Wrong status code", res.status_code, res.text)
        parsed = json.loads(res.text)
        return parsed["rawblock"]

    def get_block_summaries(self, max_number, date):
        """
        Returns the summaries of the blocks for the given day
        :param max_number: The maximum number of blocks to get
        :type max_number: Integer
        :param date: The date we are interested in
        :type date: String [YYYY-MM-DD]
        :return: A list of light blocks
        :rtype: [Block]
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
