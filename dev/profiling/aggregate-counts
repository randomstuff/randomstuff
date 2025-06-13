#!/usr/bin/python3

from typing import List
from collections.abc import Iterable
import sys
import click


@click.command
@click.option(
    "--normalize", type=click.Choice(["no", "one", "percent", "permille"]), default="no"
)
@click.option("--input-count/--no-input-count", type=bool, default=False)
# TODO, add support different output format
def main(normalize: str, input_count: bool):
    """Count the number of occurences of each input line.

    \b
    Given the following input
        a
        a
        b
        a
        c
        b
    it produces the following output:
        3   a
        2   b
        1   c

    With --input-count, it takes counts as input as well and sum them.

    \b
    Given the following input
        3.5   a
        2   b
        c   1
        3   a
        2   b
        c   1
    it produces the following output:
        6.5   a
        4   b
        2   c
    """
    counts = {}
    total = 0
    for line in sys.stdin:
        line = line.rstrip("\n").rstrip("\r")
        if input_count:
            i = line.index("\t")
            if i == -1:
                raise Exception("Missing count")
            raw_value = line[:i]
            if raw_value.endswith("%"):
                value = float(raw_value[:-1]) / 100
            elif raw_value.endswith("‰"):
                value = float(raw_value[:-1]) / 1000
            elif "." in raw_value:
                value = float(raw_value)
            else:
                value = int(raw_value)
            line = line[i + 1 :]
        else:
            value = 1
        counts[line] = counts.get(line, 0) + value
        total += value

    items = sorted(((count, key) for (key, count) in counts.items()), reverse=True)
    for count, key in items:
        if normalize == "no":
            value = str(count)
        elif normalize == "one":
            value = str(count / total)
        elif normalize == "percent":
            value = str(100 * count / total) + "%"
        elif normalize == "permil":
            value = str(1000 * count / total) + "‰"
        else:
            raise Exception("Unexpected value for 'normalize' parameter")
        print(f"{value}\t{key}")


if __name__ == "__main__":
    main()
