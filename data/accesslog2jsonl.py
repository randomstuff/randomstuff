#!/usr/bin/python3

from zoneinfo import ZoneInfo
import signal
from typing import List, Optional, Any, Callable
import re
import sys
from re import Pattern
from json import dumps
from datetime import datetime, date
from ipaddress import ip_address, IPv4Address, IPv6Address
from datetime import timezone
from argparse import ArgumentParser, RawDescriptionHelpFormatter, BooleanOptionalAction


def json_mapper(obj):
    if isinstance(obj, (datetime, date)):
        res = obj.isoformat()
        if obj.tzinfo is timezone.utc:
            res = res.replace("+00:00", "Z")
        return res
    if isinstance(obj, (IPv4Address, IPv6Address)):
        return str(obj)
    raise TypeError("No serialization for %s" % type(obj))


def parse_int(value: str) -> Optional[int]:
    if value == "-":
        return None
    return int(value)


def load_tz(tzname: str):
    if tzname == "UTC":
        return timezone.utc
    else:
        return ZoneInfo(tzname)


def parse_date(value: str, tz) -> datetime:
    return datetime.strptime(value, "%d/%b/%Y:%H:%M:%S %z").astimezone(tz)


class Field:
    name: str
    regex: str
    converter: Callable[[str], Any] | None

    def __init__(
        self, name: str, regex: str, converter: Callable[[str], Any] | None = None
    ) -> None:
        self.name = name
        self.regex = regex
        self.converter = converter


class Format:
    _tokens: List[Field | str]
    _fields: List[Field]
    _pattern = Pattern

    def __init__(self, tokens: List[Field | str]) -> None:
        self._tokens = tokens

        regex_string = (
            "^"
            + "".join(
                # TODO, difference between "literal" and "regex snippet"
                ("(" + token.regex + ")") if isinstance(token, Field) else token
                for token in tokens
            )
            + "$"
        )
        self._pattern = re.compile(regex_string)

        self._fields = [token for token in tokens if isinstance(token, Field)]

    def parse(self, data: str) -> Optional[dict]:
        match = self._pattern.match(data)
        if match is None:
            return None
        groups = match.groups()
        return {
            field.name: (
                field.converter(groups[i]) if field.converter is not None else groups[i]
            )
            for i, field in enumerate(self._fields)
        }


# NGINX defult combined format:
# log_format combined '$remote_addr - $remote_user [$time_local] '
#                    '"$request" $status $body_bytes_sent '
#                    '"$http_referer" "$http_user_agent"';

# Apache combined:
# LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined


def make_combined_format_parser(tz):
    return Format(
        [
            Field("remote_addr", "[^ ]+", converter=ip_address),
            " [^ ]+ ",
            Field("remote_user", "[^ ]+"),
            " \\[",
            Field("timestamp", "[^]]+", converter=lambda x: parse_date(x, tz)),
            '\\] "',
            Field("method", "[^ ]+"),
            " ",
            Field("path", '[^ "]+'),
            " ",
            Field("protocol", '[^ "]+'),
            '" ',
            Field("status", "[-0-9]+", converter=parse_int),
            " ",
            Field("body_bytes_sent", "[-0-9]+", converter=parse_int),
            ' "',
            Field("http_referer", '[^"]+'),
            '" "',
            Field("http_user_agent", '[^"]+'),
            '"',
        ]
    )


def main():

    parser = ArgumentParser(
        description="HTTP access log to JSON line",
        allow_abbrev=False,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("infiles", nargs="*", default=["-"])
    parser.add_argument(
        "--raw", default=False, action=BooleanOptionalAction, help="Include raw line"
    )
    parser.add_argument(
        "--debug", default=False, action=BooleanOptionalAction, help="Include raw line"
    )
    parser.add_argument("--tz", default="UTC", help="Timezone")
    args = parser.parse_args()
    debug = args.debug
    raw = args.raw
    infiles = args.infiles
    tz = load_tz(args.tz)

    parse = make_combined_format_parser(tz).parse

    # Correctly die on broken pipe:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    for infile in infiles:

        if infile == "-":
            input = sys.stdin
        else:
            input = open(infile, "rt")

        try:
            for line in input:
                line = line.rstrip("\n")
                data = parse(line)
                if data is None:
                    if debug:
                        sys.stderr.write(line + "\n")
                    continue
                if raw:
                    data["raw"] = line
                print(dumps(data, default=json_mapper))
        finally:
            if infile != "-":
                input.close()


if __name__ == "__main__":
    main()
