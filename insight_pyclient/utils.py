# -*- coding:Utf-8 -*
"""
Will contain useful functions for the rest of the module

@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""


def satoshi_to_bitcoin(satoshis):
    """
    Converts the given value from Satoshi to Bitcoin
    @param satoshis: The amount to convert
    @param satoshis: int
    @return: The converted value
    @rtype: Float
    """
    return float(satoshis) / 100000000.0


def bitcoin_to_satoshi(bitcoins):
    """
    Converts the given value from Bitcoin to Satoshi
    @param bitcoins: The amount to convert
    @param bitcoins: int
    @return: The converted value
    @rtype: Intr
    """
    return int(bitcoins * 100000000)
