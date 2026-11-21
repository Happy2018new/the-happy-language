# -*- coding: utf-8 -*-
from __future__ import division

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Text

import re
from .define import Token, TokenReader
from .const import TokenIDChar, TokenIDKeyword, TokenIDLiteral
from ..utilities.reader import StringReader
from ..utilities.string import StringConverter

ORD_ZERO = ord("0")
ORD_NINE = ord("9")


class ParseResult(object):
    token_reader = TokenReader([], 0)  # type: TokenReader
    last_begin_ptr = 0  # type: int
    last_end_ptr = 0  # type: int
    last_begin_row = 0  # type: int
    last_end_row = 0  # type: int
    parse_error = None  # type: Exception | None

    def __init__(
        self, reader, begin_ptr, end_ptr, begin_row, end_row, err
    ):  # type: (TokenReader, int, int, int, int, Exception | None) -> None
        self.token_reader = reader
        self.last_begin_ptr = begin_ptr
        self.last_end_ptr = end_ptr
        self.last_begin_row = begin_row
        self.last_end_row = end_row
        self.parse_error = err

    def reader(self):  # type: () -> TokenReader
        return self.token_reader

    def __repr__(self):  # type: () -> str
        return "ParseResult(parsed_tokens={}, last_begin_ptr={}, last_end_ptr={}, last_begin_row={}, last_end_row={}, parse_error={})".format(
            self.token_reader.buffer(),
            self.last_begin_ptr,
            self.last_end_ptr,
            self.last_begin_row,
            self.last_end_row,
            StringConverter.str_json_dumps(
                StringConverter.error_to_str(self.parse_error)
            ),
        )


class Tokenizer(object):
    STATIC_NAME_CHECKER = re.compile(
        (
            b"\\A[A-Za-z_\\u3400-\\u4dbf\\u4e00-\\u9fff]"
            b"[A-Za-z0-9_\\u3400-\\u4dbf\\u4e00-\\u9fff]*\\Z"
        ).decode(encoding="raw_unicode_escape")
    )

    @staticmethod
    def _validate_static_name(name):  # type: (Text) -> tuple[bool, str]
        if len(name) > 0 and ORD_ZERO <= ord(name[0]) <= ORD_NINE:
            message = "Variable or attribute name cannot start with a number"
            return False, message
        if Tokenizer.STATIC_NAME_CHECKER.match(name) is None:
            message = "Variable or attribute name can only contain letters, numbers and underscores"
            return False, message
        return True, ""

    @staticmethod
    def _parse_keyword_or_name(
        reader, prefix, begin, row
    ):  # type: (StringReader, Text, int, int) -> Token
        result = prefix

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

        if result not in TokenIDKeyword.KEYWORD_TO_TOKEN_ID:
            valid, message = Tokenizer._validate_static_name(result)
            if not valid:
                raise Exception(
                    "_parse_keyword_or_name: Invalid variable or attribute name {} ({})".format(
                        StringConverter.str_json_dumps(result), message
                    )
                )
            return Token(
                token_id=TokenIDLiteral.TOKEN_ID_STATIC_NAME,
                token_payload=result,
                code_begin_ptr=begin,
                code_end_ptr=reader.pointer(),
                code_row_num=row,
            )

        return Token(
            token_id=TokenIDKeyword.KEYWORD_TO_TOKEN_ID[result],
            code_begin_ptr=begin,
            code_end_ptr=reader.pointer(),
            code_row_num=row,
        )

    @staticmethod
    def _parse_int_or_float(
        reader, prefix, begin, row
    ):  # type: (StringReader, Text, int, int) -> Token
        result = prefix

        while True:
            char = reader.read()
            if char == "":
                break
            elif ORD_ZERO <= ord(char) <= ORD_NINE:
                result += char
            elif char == ".":
                result += char
            elif char in TokenIDChar.CHAR_TO_TOKEN_ID:
                reader.unread()
                break
            elif char in ["'", " ", "\t", "\r"]:
                reader.unread()
                break
            else:
                reader.unread()
                return Tokenizer._parse_keyword_or_name(reader, result, begin, row)

        try:
            _ = float(result)
        except Exception:
            raise Exception(
                "_parse_int_or_float: Invalid const number {}".format(
                    StringConverter.to_str(result)
                )
            )

        return Token(
            token_id=TokenIDLiteral.TOKEN_ID_CONST_NUMBER,
            token_payload=result,
            code_begin_ptr=begin,
            code_end_ptr=reader.pointer(),
            code_row_num=row,
        )

    @staticmethod
    def _parse_next_token(reader, row):  # type: (StringReader, int) -> Token | None
        char = reader.read()
        if char == "":
            return None

        if char == "'":
            begin = reader.pointer() - 1
            return Token(
                token_id=TokenIDLiteral.TOKEN_ID_CONST_STRING,
                token_payload=reader.parse_string(),
                code_begin_ptr=begin,
                code_end_ptr=reader.pointer(),
                code_row_num=row,
            )
        if char in TokenIDChar.CHAR_TO_TOKEN_ID:
            return Token(
                token_id=TokenIDChar.CHAR_TO_TOKEN_ID[char],
                code_begin_ptr=reader.pointer() - 1,
                code_end_ptr=reader.pointer(),
                code_row_num=row,
            )
        if ORD_ZERO <= ord(char) <= ORD_NINE:
            return Tokenizer._parse_int_or_float(
                reader, char, reader.pointer() - 1, row
            )

        return Tokenizer._parse_keyword_or_name(reader, char, reader.pointer() - 1, row)

    @staticmethod
    def parse_all_token(reader):  # type: (StringReader) -> ParseResult
        tokens = []  # type: list[Token]

        while True:
            ptr, row = reader.jump_space().pointer(), reader.row()
            try:
                token = Tokenizer._parse_next_token(reader, row)
                if token is None:
                    break
                tokens.append(token)
            except Exception as e:
                return ParseResult(
                    TokenReader(tokens), ptr, reader.pointer(), row, reader.row(), e
                )

        return ParseResult(
            TokenReader(tokens), ptr, reader.pointer(), row, reader.row(), None
        )
