# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""


class APIException(Exception):
    """
    This Exception will be thrown in case of error within the API calls.

    @ivar message: The message of the exception
    @type message: String
    @ivar code: The code of the exception
    @type code: Integer
    @ivar ret: The return code of the request
    @type ret: String
    """

    def __init__(self, message, code, ret):
        super(Exception, self).__init__(message)
        self.code = code
        self.ret = ret
        self.message = message
