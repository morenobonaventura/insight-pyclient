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
