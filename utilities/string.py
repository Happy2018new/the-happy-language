# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text

import json


class StringConverter(object):
    """
    StringConverter 提供了字符串的标准化工具（以及反向实现），
    它的主要目的是兼容 Python 2 和 Python 3 的字符串类型差异
    """

    EMPTY_TEXT = b"".decode(encoding="ascii")  # type: Text
    """
    EMPTY_TEXT 是空文本的标准形
    """
    TEXT_TYPE = type(EMPTY_TEXT)  # type: type[Text]
    """
    TEXT_TYPE 是文本标准形的类型
    """

    @staticmethod
    def to_text(string):  # type: (Text | bytes) -> Text
        """
        to_text 将给出的字符串化为文本的标准形。
        在 Python 2 中，将返回 unicode。
        在 Python 3 中，将返回 str

        Args:
            string (Text | bytes):
                欲化为文本标准形的字符串

        Returns:
            Text: 获得的文本标准形
        """
        if isinstance(string, type(StringConverter.EMPTY_TEXT)):
            return string
        elif isinstance(string, bytes):
            return string.decode(encoding="utf-8")
        else:
            raise Exception("Should never happened")

    @staticmethod
    def to_str(string):  # type: (Text | bytes) -> str
        """
        to_str 将给出的 string 还原为 str 类型

        Args:
            string (Text | bytes):
                给出的 string

        Returns:
            str: 还原结果
        """
        text = StringConverter.to_text(string)
        if isinstance(text, str):
            return text
        return text.encode(encoding="utf-8")

    @staticmethod
    def error_to_text(error):  # type: (BaseException | None) -> Text
        """
        error_to_text 将给出的异常转换为文本的标准形

        Args:
            error (BaseException | None):
                欲化为文本标准形的异常

        Returns:
            Text: 异常的文本标准形
        """
        # Entry point for Python 3
        if isinstance(StringConverter.EMPTY_TEXT, str):
            return str(error)

        # If this exception have non-native unicode method
        provider = getattr(type(error), "__unicode__", None)
        original = getattr(BaseException, "__unicode__", None)
        if provider is not None and provider is not original:
            return StringConverter.to_text(provider(error))

        # If this exception have non-native str method
        if not isinstance(error, BaseException):
            return StringConverter.to_text(error.__str__())
        if type(error).__str__ is not BaseException.__str__:
            return StringConverter.to_text(error.__str__())

        # Process each argument of the exception
        messages = []
        for i in error.args:
            if isinstance(i, (StringConverter.TEXT_TYPE, bytes)):
                messages.append(StringConverter.to_text(i))
            elif isinstance(i, BaseException):
                messages.append(StringConverter.error_to_text(i))
            else:
                messages.append(StringConverter.to_text(i.__str__()))

        # Construct the final message
        result = StringConverter.to_text(", ").join(messages)
        if len(messages) > 1:
            return StringConverter.to_text("({})").format(result)
        return result

    @staticmethod
    def error_to_str(error):  # type: (BaseException | None) -> str
        """
        error_to_str 将给出的异常转换为 str 类型

        Args:
            error (BaseException | None):
                欲转换为 str 的异常

        Returns:
            str:
                异常消息的字符串表示。
                确保结果的类型是 str
        """
        return StringConverter.to_str(StringConverter.error_to_text(error))

    @staticmethod
    def text_json_dumps(string):  # type: (Text | bytes) -> Text
        """
        text_json_dumps 将给出的字符串转换为 JSON 表示。
        text_json_dumps 确保返回的结果是一个文本的标准形

        Args:
            string (Text | bytes):
                给出的字符串

        Returns:
            Text:
                该字符串的 JSON 表示。
                确保结果是一个文本标准形
        """
        return json.dumps(StringConverter.to_text(string), ensure_ascii=False)

    @staticmethod
    def str_json_dumps(string):  # type: (Text | bytes) -> str
        """
        str_json_dumps 将给出的字符串转换为 JSON 表示。
        str_json_dumps 确保返回的结果一定是一个 str

        Args:
            string (Text | bytes):
                给出的字符串

        Returns:
            str:
                该字符串的 JSON 表示。
                确保结果的类型是 str
        """
        return StringConverter.to_str(StringConverter.text_json_dumps(string))
