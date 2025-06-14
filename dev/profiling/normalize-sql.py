#!/usr/bin/python3

from typing import List, Optional
from collections.abc import Iterable
import sys
import sqlparse
from sqlparse.sql import Statement, Token
import sqlparse.tokens
import click


def find_end_of_list(tokens: List[Token], start: int) -> Optional[int]:
    n_tokens = len(tokens)
    j = start + 1
    while j < n_tokens:
        token = tokens[j]
        if token.ttype is sqlparse.tokens.Punctuation and token.value == ")":
            return j
        if (
            token.ttype is sqlparse.tokens.Token.Name.Placeholder
            or token.ttype in sqlparse.tokens.Literal
            or token.ttype is sqlparse.tokens.Whitespace
            or (token.ttype is sqlparse.tokens.Token.Punctuation and token.value == ",")
        ):
            j += 1
        else:
            return None


def anonymize_statement(
    statement: Statement, parameterize_lists: bool, parameterize: bool
) -> Statement:
    tokens = list(statement.flatten())

    i = 0
    n_tokens = len(tokens)

    result_tokens = []

    while i < n_tokens:
        token = tokens[i]

        if parameterize and token.ttype in sqlparse.tokens.Literal:
            result_tokens.append(
                sqlparse.sql.Token(sqlparse.tokens.Token.Name.Placeholder, "?")
            )
            i += 1
            continue

        if (
            parameterize_lists
            and token.ttype is sqlparse.tokens.Punctuation
            and token.value == "("
        ):
            end = find_end_of_list(tokens, i)
            if end is not None:
                result_tokens.append(
                    sqlparse.sql.Token(sqlparse.tokens.Token.Name.Placeholder, "?")
                )
                i = end + 1
                continue

        result_tokens.append(token)
        i += 1
    return Statement(result_tokens)


def anonymize_statements(
    statements: Iterable[Statement], parameterize_lists: bool, parameterize: bool
) -> List[Statement]:
    return [
        anonymize_statement(
            s, parameterize_lists=parameterize_lists, parameterize=parameterize
        )
        for s in statements
    ]


# TODO, add support for sqlparse.parsestream?
@click.command
@click.option(
    "--parameterize/--no-parameterize",
    default=False,
    help="Parameterize literals (replace them with ?)",
)
@click.option(
    "--parameterize-lists/--no-parameterize-lists",
    default=False,
    help="Parameterize list of literals i.e replace list of literals with ?",
)
def main(parameterize_lists: bool, parameterize: bool):
    """
    Normalize (newline-terminated) SQL requests read from stdin
    """
    for line in sys.stdin:
        statements = anonymize_statements(
            sqlparse.parse(line.strip()),
            parameterize_lists=parameterize_lists,
            parameterize=parameterize,
        )
        # TODO, optimize this
        res = "; ".join(
            sqlparse.format(
                s.value,
                keyword_case="upper",
                identifier_case="lower",
                strip_comments=True,
                use_space_around_operators=True,
                strip_whitespace=True,
                compact=True,
            )
            for s in statements
        )
        sys.stdout.write(res + "\n")


if __name__ == "__main__":
    main()
