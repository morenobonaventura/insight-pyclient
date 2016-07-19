# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""

import json


class Address(object):
    """
    Will be used to store the detail of an address obtained from the web service

    @type address: String
    @type balance: Float
    @type balanceSat: Double
    @type totalReceived: Float
    @type totalReceivedSat: Double
    @type totalSent: Float
    @type totalSentSat: Double
    @type totalReceivedSat: Double
    @type unconfirmedBalance: Float
    @type unconfirmedBalanceSat: Double
    @type unconfirmedTxAppearances: Int
    @type txAppearances: int
    @type transactions: [String]
    """

    def __init__(self, string_json):
        parsed = json.loads(string_json)
        self.address = parsed["addrStr"]
        self.balance = parsed["balance"]
        self.balanceSat = parsed["balanceSat"]
        self.totalReceived = parsed["totalReceived"]
        self.totalReceivedSat = parsed["totalReceivedSat"]
        self.totalSent = parsed["totalSent"]
        self.totalSentSat = parsed["totalSentSat"]
        self.unconfirmedBalance = parsed["unconfirmedBalance"]
        self.unconfirmedBalanceSat = parsed["unconfirmedBalanceSat"]
        self.unconfirmedTxAppearances = parsed["unconfirmedTxApperances"]
        self.txAppearances = parsed["txApperances"]
        self.transactions = parsed["transactions"]


class UnspentOutput(object):
    """
    Will be used to store the unsent outputs of some address
    @type address: String
    @type txid: String
    @type vout: Int
    @type scriptPubKey: String
    @type amount: Float
    @type satoshis: Int
    @type confirmations: Int
    @type ts: Int
    """

    def __init__(self, parsed_json):
        self.address = parsed_json['address']
        self.txid = parsed_json['txid']
        self.vout = parsed_json['vout']
        self.scriptPubKey = parsed_json['scriptPubKey']
        self.amount = parsed_json['amount']
        self.satoshis = parsed_json['satoshis']
        self.confirmations = parsed_json['confirmations']
        self.ts = parsed_json['ts']
