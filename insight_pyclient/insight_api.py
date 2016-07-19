# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import requests
from block import Block


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
        block = Block(res.text)
        return block
