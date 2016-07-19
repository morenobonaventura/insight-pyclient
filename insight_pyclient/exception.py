# -*- coding:Utf-8 -*
"""
@author: Thibault de Balthasar
@contact: contact (at) thibaultdebalt [.] fr
@license: GNU GENERAL PUBLIC LICENSE Version 3
"""


class InsightPyClientException(Exception):
    """
    This exception will never be thrown in the first place. It is done in purpose that the other custom exceptions \
    inherit from it so, it will be easier later to deal with the module exceptions.

    @ivar message: The message of the exception
    @type message: String
    """

    def __init__(self, message):
        super(Exception, self).__init__(message)


class APIException(InsightPyClientException):
    """
    This Exception will be thrown in case of error within the API calls.

    @ivar message: The message of the exception
    @type message: String
    @ivar code: The code of the exception
    @type code: Integer
    @ivar ret: The return code of the request
    @type ret: String
    @ivar url: The url the program is trying to reach when the request failed
    @type url: String
    """

    def __init__(self, message, code, ret, url):
        super(InsightPyClientException, self).__init__(message)
        self.code = code
        self.ret = ret
        self.message = message
        self.url = url

    def __str__(self):
        return self.message + " HTTPCode " + str(
            self.code) + ' while trying to access ' + self.url + '.'


class ParamException(InsightPyClientException):
    """
    This exception will be raised if the arguments given to a function or method are wrong.

    @ivar message: The message of the exception
    @type message: String
    """

    def __init__(self, message):
        super(InsightPyClientException, self).__init__(message)
        self.message = message
