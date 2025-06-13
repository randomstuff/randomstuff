#!/usr/bin/python3

import click
from json import dumps


@click.command()
@click.argument('input', type=click.File('rt'), default="-")
def main(input):
    """
    Convert input LTSV (Labeled Tab-separated Values) into JSON lines
    """
    for line in input:
        line = line.rstrip('\n')
        data = {}
        for token in line.split("\t"):
            i = token.index(":")
            if i == -1:
                continue
            key = token[:i]
            value = token[i+1:]
            data[key] = value
        print(dumps(data))


if __name__ == "__main__":
    main()
