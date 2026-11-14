# -*- coding: utf-8 -*-
from __future__ import division

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
        try, except, panic
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
    TOKEN_ID_TRY = 43
    TOKEN_ID_EXCEPT = 44
    TOKEN_ID_PANIC = 45
    TOKEN_ID_GO = 46
    TOKEN_ID_SEND = 47
    TOKEN_ID_RECEIVE = 48
    TOKEN_ID_IMPORT = 49
    TOKEN_ID_FROM = 50
    TOKEN_ID_TRUE = 51
    TOKEN_ID_FALSE = 52
    TOKEN_ID_NULL = 53

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

    TOKEN_ID_VARIABLE_NAME = 54
    TOKEN_ID_CONST_STRING = 55
    TOKEN_ID_CONST_NUMBER = 56

    TOKEN_ID_TO_NAME = {
        TOKEN_ID_VARIABLE_NAME: "variable name",
        TOKEN_ID_CONST_STRING: "const string",
        TOKEN_ID_CONST_NUMBER: "const number",
    }


class Token(object):
    """
    Token 是代码中的最小语法单元，它包含了 Token ID 以及它对应的负载信息。
    并且出于调试的目的，它还保存了这个 Token 在源代码的位置以及对应的行号
    """

    token_id = 0  # type: int
    token_payload = ""  # type: str
    code_begin_ptr = 0  # type: int
    code_end_ptr = 0  # type: int
    code_row_num = 1  # type: int

    def __init__(
        self,
        token_id,
        token_payload="",
        code_begin_ptr=0,
        code_end_ptr=0,
        code_row_num=1,
    ):  # type: (int, str, int, int, int) -> None
        """初始化一个新的 Token

        Args:
            token_id (int):
                该 Token 的 ID
            token_payload (str, optional):
                该 Token 的负载。
                默认值为空字符串
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
        prefix = "Token(id={}, name={}".format(
            self.token_id, json.dumps(self.token_name(), ensure_ascii=False)
        )
        if len(self.token_payload) > 0:
            prefix += ", payload={}".format(
                json.dumps(self.token_payload, ensure_ascii=False)
            )
        return prefix + ", code_begin_ptr={}, code_end_ptr={}, code_row_num={})".format(
            self.code_begin_ptr, self.code_end_ptr, self.code_row_num
        )
