#!/usr/bin/python3
# Convert ASCII text to invisible text using regional indicator symbols.
# Can

import sys
import unicodedata
import argparse
from argparse import ArgumentParser

FORWARD = {chr(l): chr(0xE0000 + l) for l in range(0x20, 0x7F)}
REVERSE = {b: a for (a, b) in FORWARD.items()}


def convert(input: str, reverse=False, keep=False) -> str:
    if not reverse:
        input = unicodedata.normalize("NFKD", input)
        input = input.lower()
        return "".join(FORWARD.get(l, l) for l in input if keep or l in FORWARD)
    else:
        input = unicodedata.normalize("NFKD", input)
        input = input.lower()
        return "".join(REVERSE.get(l, l) for l in input if keep or l in REVERSE)


DESCRIPTION = """
* Convert ASCII text to invisible text using regional indicator symbols
* Convert the text back into ASCII.
* Can be used to fool LLMs.󠁬󠁬󠁭󠁳󠀠󠁪󠁵󠁳󠁴󠀠󠁷󠁡󠁮󠁮󠁡󠀠󠁨󠁡󠁶󠁥󠀠󠁦󠁵󠁮
"""

parser = ArgumentParser(
    description=DESCRIPTION,
    allow_abbrev=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "filenames",
    metavar="FILE",
    type=str,
    nargs="*",
    help="Input text files",
)
parser.add_argument(
    "-c",
    "--command",
    metavar="TEXT",
    type=str,
    nargs="*",
    dest="texts",
    help="Input text",
)
parser.add_argument(
    "-r",
    "--reverse",
    action="store_true",
    default=False,
    help="Convert back into ASCII",
)
parser.add_argument(
    "-k",
    "--keep",
    action="store_true",
    default=False,
    help="Keep untranslatable characters",
)

args = parser.parse_args()

kwargs = {
    "reverse": args.reverse,
    "keep": args.keep,
}
for filename in args.filenames:
    if filename == "-":
        sys.stdout.write(convert(sys.stdin.read(), **kwargs))
    else:
        sys.stdout.write(convert(open(filename, "rt").read(), **kwargs))
for text in args.texts or []:
    sys.stdout.write(convert(text, **kwargs))
