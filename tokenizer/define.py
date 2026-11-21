# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text

from .const import TokenIDChar, TokenIDKeyword, TokenIDLiteral
from ..utilities.string import StringConverter
from ..utilities.reader import ListReader


class Token(object):
    """
    Token 是代码中的最小语法单元，它包含了 Token ID 以及它对应的负载信息。
    并且出于调试的目的，它还保存了这个 Token 在源代码的位置以及对应的行号
    """

    token_id = 0  # type: int
    token_payload = StringConverter.EMPTY_TEXT  # type: Text
    code_begin_ptr = 0  # type: int
    code_end_ptr = 0  # type: int
    code_row_num = 1  # type: int

    def __init__(
        self,
        token_id,
        token_payload=StringConverter.EMPTY_TEXT,
        code_begin_ptr=0,
        code_end_ptr=0,
        code_row_num=1,
    ):  # type: (int, Text, int, int, int) -> None
        """初始化一个新的 Token

        Args:
            token_id (int):
                该 Token 的 ID
            token_payload (Text, optional):
                该 Token 的负载信息。
                负载应是文本的标准形。
                默认值为空文本的标准形
            code_begin_ptr (int, optional):
                该 Token 在源代码中的起始位置。
                默认值为 0
            code_end_ptr (int, optional):
                该 Token 在源代码中的结束位置。
                默认值为 0
            code_row_num (int, optional):
                该 Token 在源代码中对应的行号。
                默认值为 1
        """
        self.token_id = token_id
        self.token_payload = token_payload
        self.code_begin_ptr = code_begin_ptr
        self.code_end_ptr = code_end_ptr
        self.code_row_num = code_row_num

    def token_name(self):  # type: () -> str
        """
        token_name 返回该 Token 的名称。
        该函数的存在仅仅是为了调试的目的，
        用于方便查看该 Token 对应的名称

        Returns:
            str:
                该 Token 的调试名称。
                如果无效，则返回 "unknown"
        """
        if self.token_id in TokenIDChar.TOKEN_ID_TO_CHAR:
            return TokenIDChar.TOKEN_ID_TO_CHAR[self.token_id]
        elif self.token_id in TokenIDKeyword.TOKEN_ID_TO_KEYWORD:
            return TokenIDKeyword.TOKEN_ID_TO_KEYWORD[self.token_id]
        elif self.token_id in TokenIDLiteral.TOKEN_ID_TO_NAME:
            return TokenIDLiteral.TOKEN_ID_TO_NAME[self.token_id]
        else:
            return "unknown"

    def __repr__(self):  # type: () -> str
        """返回该 Token 的字符串表示

        Returns:
            str: 该 Token 的字符串表示
        """
        prefix = "Token(token_id={}, token_name={}".format(
            self.token_id, StringConverter.str_json_dumps(self.token_name())
        )
        if len(self.token_payload) > 0:
            prefix += ", token_payload={}".format(
                StringConverter.str_json_dumps(self.token_payload)
            )
        return prefix + ", code_begin_ptr={}, code_end_ptr={}, code_row_num={})".format(
            self.code_begin_ptr, self.code_end_ptr, self.code_row_num
        )


class TokenReader(ListReader):
    """TokenReader 是 Token 的流式阅读器"""

    def __init__(self, buf, ptr=0):  # type: (list[Token], int) -> None
        """初始化一个新的 Token 流式阅读器

        Args:
            buf (list[Token]):
                用于初始化阅读器的 Token 列表
            ptr (int, optional):
                阅读器的初始指针位置，
                默认值为 0
        """
        ListReader.__init__(self, buf, ptr)

    def buffer(self):  # type: () -> list[Token]
        """buffer 返回该阅读器的底层流

        Returns:
            list[Token]: 该阅读器的底层流
        """
        return ListReader.buffer(self)

    def pointer(self):  # type: () -> int
        """
        pointer 返回该阅读器的当前指针位置

        Returns:
            int: 该阅读器的当前指针位置
        """
        return ListReader.pointer(self)

    def set_pointer(self, ptr):  # type: (int) -> TokenReader
        """
        set_pointer 设置该阅读器的当前指针位置。
        即便提供的指针超出范围，它也可以正常工作

        Args:
            ptr (int): 阅读器的新指针位置

        Returns:
            TokenReader: 返回阅读器本身
        """
        ListReader.set_pointer(self, ptr)
        return self

    def read(self):  # type: () -> Token | None
        """
        read 试图从底层流中读取一个 Token。
        如果底层流已被提前耗尽，则返回 None

        Returns:
            Token | None:
                从底层流中读取到的 Token。
                如果流已耗尽，则返回 None
        """
        return ListReader.read(self)

    def must_read(self):  # type: () -> Token
        """
        must_read 试图从底层流读取一个 Token 并希望保证这一点。
        这意味着如果该函数没有抛出错误，则它保证返回一个 Token

        Raises:
            Exception:
                如果底层流被提前耗尽，
                则将会抛出对应的错误

        Returns:
            Token: 从底层流中读取到的 Token
        """
        return ListReader.must_read(self)

    def unread(self):  # type: () -> TokenReader
        """
        unread 无副作用地撤销对底层流的一个 Token 的读取。
        即便试图在底层流的开头撤销读取，也不会产生任何错误

        Returns:
            TokenReader: 返回阅读器本身
        """
        ListReader.unread(self)
        return self

    def must_unread(self):  # type: () -> TokenReader
        """
        must_unread 撤销对底层流的一个 Token 的读取，并希望保证这一点。
        这意味着如果没有抛出错误，则它保证阅读器指针恰好向前移动一个元素

        Raises:
            Exception:
                如果撤销后指针的位置超出流的可达范围，
                则将会抛出对应的错误

        Returns:
            TokenReader: 返回阅读器本身
        """
        ListReader.must_unread(self)
        return self
