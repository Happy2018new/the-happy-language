# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text

import json


class TokenIDChar(object):
    """
    TokenIDChar 是单字符的 Token ID 枚举。
    下面列出了目前受支持的所有单字符。
    ```
        +   -   *   /   %
        <   >   =   !
        &   |   ^   ~   :

        (   )   [   ]   {   }
        .   ,

        \\n  ;
    ```
    """

    TOKEN_ID_ADD = 0
    TOKEN_ID_SUB = 1
    TOKEN_ID_MUL = 2
    TOKEN_ID_DIV = 3
    TOKEN_ID_MOD = 4
    TOKEN_ID_LESS = 5
    TOKEN_ID_GREATER = 6
    TOKEN_ID_EQUAL = 7
    TOKEN_ID_EXCLAMATION = 8
    TOKEN_ID_LOGIC_AND = 9
    TOKEN_ID_LOGIC_OR = 10
    TOKEN_ID_LOGIC_XOR = 11
    TOKEN_ID_LOGIC_NOT = 12
    TOKEN_ID_COLON = 13
    TOKEN_ID_LEFT_SMALL_BRACKET = 14
    TOKEN_ID_RIGHT_SMALL_BRACKET = 15
    TOKEN_ID_LEFT_MIDDLE_BRACKET = 16
    TOKEN_ID_RIGHT_MIDDLE_BRACKET = 17
    TOKEN_ID_LEFT_BIG_BRACKET = 18
    TOKEN_ID_RIGHT_BIG_BRACKET = 19
    TOKEN_ID_DOT = 20
    TOKEN_ID_COMMA = 21
    TOKEN_ID_NEWLINE = 22
    TOKEN_ID_SEMICOLON = 23

    CHAR_TO_TOKEN_ID = {
        "+": TOKEN_ID_ADD,
        "-": TOKEN_ID_SUB,
        "*": TOKEN_ID_MUL,
        "/": TOKEN_ID_DIV,
        "%": TOKEN_ID_MOD,
        "<": TOKEN_ID_LESS,
        ">": TOKEN_ID_GREATER,
        "=": TOKEN_ID_EQUAL,
        "!": TOKEN_ID_EXCLAMATION,
        "&": TOKEN_ID_LOGIC_AND,
        "|": TOKEN_ID_LOGIC_OR,
        "^": TOKEN_ID_LOGIC_XOR,
        "~": TOKEN_ID_LOGIC_NOT,
        ":": TOKEN_ID_COLON,
        "(": TOKEN_ID_LEFT_SMALL_BRACKET,
        ")": TOKEN_ID_RIGHT_SMALL_BRACKET,
        "[": TOKEN_ID_LEFT_MIDDLE_BRACKET,
        "]": TOKEN_ID_RIGHT_MIDDLE_BRACKET,
        "{": TOKEN_ID_LEFT_BIG_BRACKET,
        "}": TOKEN_ID_RIGHT_BIG_BRACKET,
        ".": TOKEN_ID_DOT,
        ",": TOKEN_ID_COMMA,
        "\n": TOKEN_ID_NEWLINE,
        ";": TOKEN_ID_SEMICOLON,
    }
    TOKEN_ID_TO_CHAR = {value: key for key, value in CHAR_TO_TOKEN_ID.items()}


class TokenIDKeyword(object):
    """
    TokenIDKeyword 是关键字的 Token ID 枚举。
    下面列出了目前受支持的所有关键字。
    ```
        not, in, and, or
        if, elif, fi, for, rof, fn, nf
        switch, select, case, end
        continue, break, leave, return
        defer, try, except, panic
        go, send, receive
        import, from
        True, False, Null
    ```
    """

    TOKEN_ID_NOT = 24
    TOKEN_ID_IN = 25
    TOKEN_ID_AND = 26
    TOKEN_ID_OR = 27
    TOKEN_ID_IF = 28
    TOKEN_ID_ELIF = 29
    TOKEN_ID_FI = 30
    TOKEN_ID_FOR = 31
    TOKEN_ID_ROF = 32
    TOKEN_ID_FN = 33
    TOKEN_ID_NF = 34
    TOKEN_ID_SWITCH = 35
    TOKEN_ID_SELECT = 36
    TOKEN_ID_CASE = 37
    TOKEN_ID_END = 38
    TOKEN_ID_CONTINUE = 39
    TOKEN_ID_BREAK = 40
    TOKEN_ID_LEAVE = 41
    TOKEN_ID_RETURN = 42
    TOKEN_ID_DEFER = 43
    TOKEN_ID_TRY = 44
    TOKEN_ID_EXCEPT = 45
    TOKEN_ID_PANIC = 46
    TOKEN_ID_GO = 47
    TOKEN_ID_SEND = 48
    TOKEN_ID_RECEIVE = 49
    TOKEN_ID_IMPORT = 50
    TOKEN_ID_FROM = 51
    TOKEN_ID_TRUE = 52
    TOKEN_ID_FALSE = 53
    TOKEN_ID_NULL = 54

    KEYWORD_TO_TOKEN_ID = {
        "not": TOKEN_ID_NOT,
        "in": TOKEN_ID_IN,
        "and": TOKEN_ID_AND,
        "or": TOKEN_ID_OR,
        "if": TOKEN_ID_IF,
        "elif": TOKEN_ID_ELIF,
        "fi": TOKEN_ID_FI,
        "for": TOKEN_ID_FOR,
        "rof": TOKEN_ID_ROF,
        "fn": TOKEN_ID_FN,
        "nf": TOKEN_ID_NF,
        "switch": TOKEN_ID_SWITCH,
        "select": TOKEN_ID_SELECT,
        "case": TOKEN_ID_CASE,
        "end": TOKEN_ID_END,
        "continue": TOKEN_ID_CONTINUE,
        "break": TOKEN_ID_BREAK,
        "leave": TOKEN_ID_LEAVE,
        "return": TOKEN_ID_RETURN,
        "defer": TOKEN_ID_DEFER,
        "try": TOKEN_ID_TRY,
        "except": TOKEN_ID_EXCEPT,
        "panic": TOKEN_ID_PANIC,
        "go": TOKEN_ID_GO,
        "send": TOKEN_ID_SEND,
        "receive": TOKEN_ID_RECEIVE,
        "import": TOKEN_ID_IMPORT,
        "from": TOKEN_ID_FROM,
        "True": TOKEN_ID_TRUE,
        "False": TOKEN_ID_FALSE,
        "Null": TOKEN_ID_NULL,
    }
    TOKEN_ID_TO_KEYWORD = {value: key for key, value in KEYWORD_TO_TOKEN_ID.items()}


class TokenIDLiteral(object):
    """
    TokenIDLiteral 是变量名和字面量的 Token ID 枚举
    """

    TOKEN_ID_VARIABLE_NAME = 55
    TOKEN_ID_CONST_STRING = 56
    TOKEN_ID_CONST_NUMBER = 57

    TOKEN_ID_TO_NAME = {
        TOKEN_ID_VARIABLE_NAME: "variable name",
        TOKEN_ID_CONST_STRING: "const string",
        TOKEN_ID_CONST_NUMBER: "const number",
    }


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
