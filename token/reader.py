# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any

import json
from .define import Token

ESCAPE_CHAR_MAPPING = {
    "t": "\t",
    "r": "\r",
    "n": "\n",
    "\\": "\\",
    "'": "'",
    '"': '"',
}


class StringReader(object):
    """StringReader 是字符串的流式阅读器"""

    _buf = ""  # type: str
    _ptr = 0  # type: int
    _row = 1  # type: int

    def __init__(self, buf, ptr=0):  # type: (str, int) -> None
        """
        初始化一个新的字符串流式阅读器

        Args:
            buf (str):
                用于初始化阅读器的字符串
            ptr (int, optional):
                阅读器的初始指针位置，
                默认值为 0
        """
        self._buf = buf
        self._ptr = 0
        self._row = 1
        self.set_pointer(ptr)

    def buffer(self):  # type: () -> str
        """
        buffer 返回该阅读器的底层流

        Returns:
            str: 该阅读器的底层流
        """
        return self._buf

    def pointer(self):  # type: () -> int
        """
        pointer 返回该阅读器的当前指针位置

        Returns:
            int: 该阅读器的当前指针位置
        """
        return self._ptr

    def row(self):  # type: () -> int
        """
        row 返回该阅读器当前指针所在的行号

        Returns:
            int: 该阅读器的当前指针所在的行号
        """
        return self._row

    def set_pointer(self, ptr):  # type: (int) -> StringReader
        """
        set_pointer 设置该阅读器的当前指针位置。
        即便提供的指针超出范围，它也可以正常工作

        Args:
            ptr (int): 阅读器的新指针位置

        Returns:
            StringReader: 返回阅读器本身
        """
        self._ptr = min(max(ptr, 0), len(self._buf))
        self._row = 1

        for i in range(self._ptr):
            if self._buf[i] == "\n":
                self._row += 1

        return self

    def read(self):  # type: () -> str
        """
        read 试图从底层流中读取一个字符。
        即便底层流已耗尽，也不会产生错误

        Returns:
            str: 从底层流中读取到的字符串
        """
        if self._ptr >= len(self._buf):
            return ""

        result = self._buf[self._ptr]
        if result == "\n":
            self._row += 1
        self._ptr += 1

        return result

    def must_read(self):  # type: () -> str
        """
        must_read 从底层流读取一个字符，并希望保证这一点。
        这意味着如果没有错误，则它保证返回一个非空的字符串

        Raises:
            Exception:
                如果底层流被提前耗尽，
                则将会抛出对应的错误

        Returns:
            str: 从底层流中读取到的单个字符
        """
        char = self.read()
        if char == "":
            raise Exception("must_read: Unexpected EOF")
        return char

    def unread(self):  # type: () -> StringReader
        """
        unread 无副作用地撤销对底层流的一个字符的读取。
        即便试图在流的开头撤销读取，也不会产生任何错误

        Returns:
            StringReader: 返回阅读器本身
        """
        ptr = self._ptr - 1
        if ptr < 0:
            return self

        if self._buf[ptr] == "\n":
            self._row -= 1
        self._ptr = ptr

        return self

    def must_unread(self):  # type: () -> StringReader
        """
        must_unread 撤销对底层流的一个字符的读取，并希望保证这一点。
        这意味着如果没有错误，则它保证阅读器指针恰好向前移动一个字符

        Raises:
            Exception:
                如果撤销后指针的位置超出流的可达范围，
                则将会抛出对应的错误

        Returns:
            StringReader: 返回阅读器本身
        """
        if self._ptr - 1 < 0:
            raise Exception("must_unread: Unexpected EOF")
        return self.unread()

    def jump_space(self):  # type: () -> StringReader
        """
        jump_space 不断地阅读并跳过期间遇到的所有空白字符，
        因此，它会在遇到第一个非空白字符前停止阅读并返回值。
        即便底层流在空白字符处终止，该函数也不会产生任何错误

        Returns:
            StringReader: 返回阅读器本身
        """
        while True:
            char = self.read()
            if char == " " or char == "\t" or char == "\r":
                continue
            if char != "":
                self.unread()
            return self

    def parse_string(self):  # type: () -> str
        """
        parse_string 试图从底层流中解析一个由单引号包围的字符串。
        它假定调用者已经从底层流中读取了这个字符串最开头的单引号

        Raises:
            Exception:
                如果字符串未被正确关闭，
                或字符串中包含了换行符，
                或存在不受支持的转义符，
                则将会抛出对应的错误

        Returns:
            str: 解析得到的字符串
        """
        result = ""
        while True:
            char = self.must_read()

            if char == "'":
                return result
            if char == "\n":
                raise Exception(
                    "parse_string: A string cannot contain a newline character"
                )
            if char != "\\":
                result += char
                continue

            sub = self.must_read()
            if sub not in ESCAPE_CHAR_MAPPING:
                raise Exception(
                    "parse_string: Escape character {} is not supported".format(
                        json.dumps("\\" + sub, ensure_ascii=False)
                    )
                )
            result += ESCAPE_CHAR_MAPPING[sub]


class ListReader(object):
    """ListReader 是列表的流式阅读器"""

    _buf = []  # type: list[Any]
    _ptr = 0  # type: int

    def __init__(self, buf, ptr=0):  # type: (list[Any], int) -> None
        """
        初始化一个新的流式列表阅读器

        Args:
            buf (list[Any]):
                用于初始化阅读器的列表，这将作为阅读器的底层流。
                调用者有义务确保给出的列表中的元素不包含 None
            ptr (int, optional):
                阅读器的初始指针位置，
                默认值为 0
        """
        self._buf, self._ptr = buf, 0
        self.set_pointer(ptr)

    def buffer(self):  # type: () -> list[Any]
        """buffer 返回该阅读器的底层流

        Returns:
            list[Any]: 该阅读器的底层流
        """
        return self._buf

    def pointer(self):  # type: () -> int
        """
        pointer 返回该阅读器的当前指针位置

        Returns:
            int: 该阅读器的当前指针位置
        """
        return self._ptr

    def set_pointer(self, ptr):  # type: (int) -> ListReader
        """
        set_pointer 设置该阅读器的当前指针位置。
        即便提供的指针超出范围，它也可以正常工作

        Args:
            ptr (int): 阅读器的新指针位置

        Returns:
            ListReader: 返回阅读器本身
        """
        self._ptr = max(ptr, 0)
        self._ptr = min(self._ptr, len(self._buf))
        return self

    def read(self):  # type: () -> Any | None
        """
        read 试图从底层流中读取一个元素。
        如果底层流提前耗尽，则返回 None

        Returns:
            Any | None:
                从底层流中读取到的元素。
                如果流耗尽，则返回 None
        """
        if self._ptr >= len(self._buf):
            return None
        self._ptr += 1
        return self._buf[self._ptr - 1]

    def must_read(self):  # type: () -> Any
        """
        must_read 试图从底层流读取一个元素，并希望保证这一点。
        这意味着如果没有错误，则它保证返回一个不是 None 的元素。

        Raises:
            Exception:
                如果底层流被提前耗尽，
                则将会抛出对应的错误

        Returns:
            Any: 从底层流中读取到的元素
        """
        element = self.read()
        if element is None:
            raise Exception("must_read: Unexpected EOF")
        return element

    def unread(self):  # type: () -> ListReader
        """
        unread 无副作用地撤销对底层流的一个元素的读取。
        即便试图在流的开头撤销读取，也不会产生任何错误

        Returns:
            ListReader: 返回阅读器本身
        """
        self._ptr = max(self._ptr - 1, 0)
        return self

    def must_unread(self):  # type: () -> ListReader
        """
        must_unread 撤销对底层流的一个元素的读取，并希望保证这一点。
        这意味着如果没有错误，则它保证阅读器指针恰好向前移动一个元素

        Raises:
            Exception:
                如果撤销后指针的位置超出流的可达范围，
                则将会抛出对应的错误

        Returns:
            ListReader: 返回阅读器本身
        """
        if self._ptr - 1 < 0:
            raise Exception("must_unread: Unexpected EOF")
        return self.unread()


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
