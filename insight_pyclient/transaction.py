# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import json
import datetime


class TransactionInput(object):
    """
    Will contain the input of a transaction.
    :type txid: String
    :type vout: int
    :type scriptSigAsm: String
    :type scriptSigHex: String
    :type sequence: int
    :type n: int
    :type addr: string
    :type valueSat: int
    :type value: Float
    :type doubleSpentTxID: nullable (string ?)
    """

    def __init__(self, parsed_json):
        self.txid = parsed_json["txid"]
        self.vout = parsed_json["vout"]
        self.sequence = parsed_json["sequence"]
        self.n = parsed_json["n"]
        self.addr = parsed_json["addr"]
        self.valueSat = parsed_json["valueSat"]
        self.value = parsed_json["value"]
        self.doubleSpentTxID = parsed_json["doubleSpentTxID"]
        self.scriptSigAsm = parsed_json["scriptSig"]["asm"]
        self.scriptSigHex = parsed_json["scriptSig"]["hex"]


class TransactionOutput(object):
    """
    Will be used to store the outputs of a transaction.

    :type value: Float
    :type n: int
    :type spentTxId: String
    :type spentIndex: int
    :type spentHeight: int
    :type scriptPubKey: TransactionOutput.ScriptPublicKey
    """

    def __init__(self, parsed_json):
        self.value = parsed_json["value"]
        self.n = parsed_json["n"]
        self.spentTxId = parsed_json["spentTxId"]
        self.spentIndex = parsed_json["spentIndex"]
        self.spentHeight = parsed_json["spentHeight"]
        self.scriptPubKey = TransactionOutput.ScriptPublicKey(parsed_json["scriptPubKey"])

    class ScriptPublicKey(object):
        """
        To store the scriptPubKey
        :type hex: String
        :type asm: String
        :type addresses = [String]
        :type type: String
        """

        def __init__(self, parsed_json):
            self.hex = parsed_json["hex"]
            self.asm = parsed_json["asm"]
            self.addresses = parsed_json["addresses"]
            self.type = parsed_json["type"]


class Transaction(object):
    """
    Will be used to store the details of a transaction

    :type txid: String
    :type version: int
    :type lockTime: int
    :type blockHeight: int
    :type confirmations: int
    :type time: datetime
    :type valueOut: Float
    :type size: int
    :type valueIn: Float
    :type fees: Float
    :type inputs: [Input]
    :type outputs: [Output]
    """

    def __init__(self, string_json):
        parsed = json.loads(string_json)
        self.txid = parsed["txid"]
        self.version = parsed["version"]
        self.lockTime = parsed["locktime"]
        self.blockHeight = parsed["blockheight"]
        self.confirmations = parsed["confirmations"]
        self.time = datetime.datetime.fromtimestamp(parsed['time'])
        self.valueOut = parsed["valueOut"]
        self.size = parsed["size"]
        self.valueIn = parsed["valueIn"]
        self.fees = parsed["fees"]
        self.inputs = []
        self.outputs = []

        for item in parsed["vout"]:
            self.outputs.append(TransactionOutput(item))
        for item in parsed["vin"]:
            self.inputs.append(TransactionInput(item))
