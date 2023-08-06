#!/usr/bin/env python
# -*- coding:utf-8 -*-

class _RestSqlExceptionBase(Exception):
    """
    RestSQL库所有异常的基类。
    """

    def __init__(self, code, message, *args):
        self.code = code
        self.message = message.format(args)


class RunningException(_RestSqlExceptionBase):
    """
    运行时异常
    """
    pass


class UserConfigException(_RestSqlExceptionBase):
    """
    配置错误；提示用户问题。
    """
    pass


class JsonFormatException(UserConfigException):
    """
    json格式异常；提示用户问题。
    """
    pass


class ProgramConfigException(_RestSqlExceptionBase):
    """
    程序使用错误；也就是检查异常，请程序员检查程序。
    """
    pass
