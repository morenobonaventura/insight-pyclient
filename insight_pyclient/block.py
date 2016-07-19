# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import json
import datetime


class Block(object):
    """
    Will contain an instance of Block provided by the api.

    @ivar hash: The transaction hash
    @type hash: String
    @ivar size: The size of the block
    @type hash: String
    @ivar height: The height of the block
    @type height: Integer
    @ivar height: The height of the block
    @type height: Integer
    @ivar height: The version of the block
    @type height: Integer
    @ivar merkleroot: The merkleroot of the block
    @type merkleroot: String
    @ivar tx: The hashes of the transactions present in the block
    @type tx: [String]
    @ivar time: The time of mining
    @type time: datetime
    @ivar nonce: The nonce of the block
    @type nonce: Integer
    @ivar bits: The bits of the block
    @type bits: String
    @ivar difficulty: The difficulty of the block
    @type difficulty: Float
    @ivar chainWork: The chainwork of the block
    @type chainWork: String
    @ivar confirmations: The confirmations of the block
    @type confirmations: Integer
    @ivar previousBlockHash: The hash of the previous block
    @type previousBlockHash: String
    @ivar nextBlockHash: The hash of the next block
    @type nextBlockHash: String
    @ivar reward: The reward of the block
    @type reward: Float
    @ivar isMainChain: Is this block in the mainchain ?
    @type isMainChain: Boolean
    @ivar poolName: The name of the pool that succeed mining the block
    @type poolName: String
    @ivar poolUrl: The URL of the pool that succeed mining the block
    @type poolUrl: String
    @ivar txLength: The length of the transaction (only on the summary version)
    @type txLength: Integer
    @ivar partOfSummary: On some cases, only a short version of the block may be loaded from the API, will be true if \
    it is the case. If the class was instantiated empty, will be null.
    @type partOfSummary: nullable Boolean
    """

    def __init__(self, json_string):
        parsed = json.loads(json_string)
        self.hash = parsed["hash"]
        self.size = parsed["size"]
        self.height = parsed["height"]
        self.version = parsed["version"]
        self.tx = parsed["tx"]
        self.time = datetime.datetime.fromtimestamp(parsed['time'])
        self.nonce = parsed["nonce"]
        self.bits = parsed["bits"]
        self.difficulty = parsed["difficulty"]
        self.chainWork = parsed["chainwork"]
        self.confirmations = parsed["confirmations"]
        self.previousBlockHash = parsed["previousblockhash"]
        self.nextBlockHash = parsed["nextblockhash"]
        self.reward = parsed["reward"]
        self.isMainChain = parsed["isMainChain"]
        self.poolName = parsed["poolInfo"]["poolName"]
        self.poolUrl = parsed["poolInfo"]["url"]

        self.partOfSummary = False
        self.txLength = 0

    def __init__(self):
        self.hash = ""
        self.size = 0
        self.height = 0
        self.version = 0
        self.tx = []
        self.time = datetime.datetime(1000, 1, 1)
        self.nonce = 0
        self.bits = ""
        self.difficulty = 0
        self.chainWork = ""
        self.confirmations = 0
        self.previousBlockHash = ""
        self.nextBlockHash = ""
        self.reward = 0
        self.isMainChain = False
        self.poolName = ""
        self.poolUrl = ""
        self.partOfSummary = False
        self.txLength = 0

    def parse_summary(self, loaded_json):
        """
        Used with get_block_summaries to get a light version
        :param loaded_json: The part of the json return by the API that contains the block to parse
        :type loaded_json: Dictionnary parsed by json.loads
        """
        self.partOfSummary = True
        self.hash = loaded_json["hash"]
        self.size = loaded_json["size"]
        self.txLength = loaded_json["txlength"]
        self.time = datetime.datetime.fromtimestamp(loaded_json['time'])
        if "poolInfo" in loaded_json:
            if "poolName" in loaded_json["poolInfo"]:
                self.poolName = loaded_json["poolInfo"]["poolName"]
            if "url" in loaded_json["poolInfo"]:
                self.poolUrl = loaded_json["poolInfo"]["url"]


class BlockSummaryPagination(object):
    """
    Will be used to store the pagination result of the block summary.
    :type nextDate: datetime (nullable)
    :type prevDate: dateTime (nullable)
    :type currentTs: int
    :type currentDate: dateTime
    :type isToday: Boolean
    :type more: Boolean
    :type moreTs: int
    """

    def __init__(self, parsed_json):
        if "next" in parsed_json and parsed_json["next"] is not "":
            self.nextDate = datetime.datetime.strptime(parsed_json["next"], "%Y-%m-%d").strftime("%d-%m-%Y")
        else:
            self.nextDate = None
        if "prev" in parsed_json and parsed_json["prev"] is not "":
            self.prevDate = datetime.datetime.strptime(parsed_json["prev"], "%Y-%m-%d").strftime("%d-%m-%Y")
        else:
            self.prevDate = None
        self.currentTs = parsed_json["currentTs"]
        self.currentDate = datetime.datetime.strptime(parsed_json["current"], "%Y-%m-%d").strftime("%d-%m-%Y")
        self.isToday = parsed_json["isToday"]
        self.more = parsed_json["more"]
        self.moreTs = parsed_json["moreTs"]
