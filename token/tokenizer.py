# -*- coding: utf-8 -*-
from __future__ import division

import re
import json
from .reader import StringReader, TokenReader
from .define import TokenIDChar, TokenIDKeyword, TokenIDLiteral, Token

VAR_NAME_PATTERN = re.compile(
    (
        b"\\A[A-Za-z_\\u3400-\\u4dbf\\u4e00-\\u9fff][A-Za-z0-9_\\u3400-\\u4dbf\\u4e00-\\u9fff]*\\Z"
        b"[A-Za-z0-9_\\u3400-\\u4dbf\\u4e00-\\u9fff]*\\Z"
    ).decode("raw_unicode_escape")
)
ORD_ZERO = ord("0")
ORD_NINE = ord("9")


class ParseResult(object):
    token_reader = TokenReader([], 0)  # type: TokenReader
    last_begin_ptr = 0  # type: int
    last_end_ptr = 0  # type: int
    last_row_num = 0  # type: int
    parse_error = None  # type: Exception | None

    def __init__(
        self, reader, begin, end, row, err
    ):  # type: (TokenReader, int, int, int, Exception | None) -> None
        self.token_reader = reader
        self.last_begin_ptr = begin
        self.last_end_ptr = end
        self.last_row_num = row
        self.parse_error = err

    def __repr__(self):  # type: () -> str
        return "ParseResult(parsed_tokens={}, last_begin_ptr={}, last_end_ptr={}, last_row_num={}, parse_error={})".format(
            self.token_reader.buffer(),
            self.last_begin_ptr,
            self.last_end_ptr,
            self.last_row_num,
            self.parse_error,
        )


class Tokenizer(object):
    def __init__(self):  # type: () -> None
        pass

    def _validate_var_name(self, name):  # type: (str) -> tuple[bool, str]
        if VAR_NAME_PATTERN.match(name) is None:
            message = "Variable name can only contain letters, numbers, and underscores"
            return False, message
        return True, ""

    def _parse_int_or_float(
        self, reader, char, begin, row
    ):  # type: (StringReader, str, int, int) -> Token
        result = char

        while True:
            char = reader.read()
            if char == "":
                break
            elif ORD_ZERO <= ord(char) <= ORD_NINE:
                result += char
            elif char == ".":
                result += char
            else:
                reader.unread()
                break

        try:
            _ = float(result)
        except Exception:
            raise Exception(
                "_parse_int_or_float: Invalid const number {}".format(result)
            )

        return Token(
            token_id=TokenIDLiteral.TOKEN_ID_CONST_NUMBER,
            token_payload=result,
            code_begin_ptr=begin,
            code_end_ptr=reader.pointer(),
            code_row_num=row,
        )

    def _parse_keyword_or_var(
        self, reader, char, begin, row
    ):  # type: (StringReader, str, int, int) -> Token
        result = char

        while True:
            char = reader.read()
            if char == "":
                break
            elif char in TokenIDChar.CHAR_TO_TOKEN_ID:
                reader.unread()
                break
            elif char in ["'", " ", "\t", "\r"]:
                reader.unread()
                break
            else:
                result += char

        token = Token(
            token_id=TokenIDLiteral.TOKEN_ID_VARIABLE_NAME,
            token_payload=result,
            code_begin_ptr=begin,
            code_end_ptr=reader.pointer(),
            code_row_num=row,
        )
        if result in TokenIDKeyword.KEYWORD_TO_TOKEN_ID:
            token.token_id = TokenIDKeyword.KEYWORD_TO_TOKEN_ID[result]
            return token

        valid, message = self._validate_var_name(result)
        if not valid:
            raise Exception(
                "_parse_keyword_or_var: Invalid variable name {} ({})".format(
                    json.dumps(result, ensure_ascii=False), message
                )
            )
        return token

    def _parse_next_token(self, reader):  # type: (StringReader) -> Token | None
        row = reader.row()
        char = reader.jump_space().read()
        if char == "":
            return None

        if char in TokenIDChar.CHAR_TO_TOKEN_ID:
            return Token(
                token_id=TokenIDChar.CHAR_TO_TOKEN_ID[char],
                code_begin_ptr=reader.pointer() - 1,
                code_end_ptr=reader.pointer(),
                code_row_num=row,
            )
        if char == "'":
            begin = reader.pointer() - 1
            return Token(
                token_id=TokenIDLiteral.TOKEN_ID_CONST_STRING,
                token_payload=reader.parse_string(),
                code_begin_ptr=begin,
                code_end_ptr=reader.pointer(),
                code_row_num=row,
            )

        if ORD_ZERO <= ord(char) <= ORD_NINE:
            return self._parse_int_or_float(reader, char, reader.pointer() - 1, row)
        return self._parse_keyword_or_var(reader, char, reader.pointer() - 1, row)

    def parse_all_token(self, reader):  # type: (StringReader) -> ParseResult
        tokens = []  # type: list[Token]
        last_ptr = reader.pointer()  # type: int

        while True:
            try:
                token, last_ptr = self._parse_next_token(reader), reader.pointer()
                if token is None:
                    break
                tokens.append(token)
            except Exception as e:
                return ParseResult(
                    TokenReader(tokens), last_ptr, reader.pointer(), reader.row(), e
                )

        return ParseResult(
            TokenReader(tokens), last_ptr, reader.pointer(), reader.row(), None
        )
