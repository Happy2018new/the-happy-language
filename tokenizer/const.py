# -*- coding: utf-8 -*-
from __future__ import division


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
