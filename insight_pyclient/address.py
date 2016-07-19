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
