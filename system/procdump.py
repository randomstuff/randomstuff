#!/usr/bin/python3

from sys import stdout
from typing import Tuple, List, Optional
import re
import dataclasses

import click


MAPS_RE = re.compile(
    """
    ^
    (?P<start>[0-9a-f]+)
    -
    (?P<stop>[0-9a-f]+)
    \s+
    (?P<flags>[-r][-w][-x][ps])
    \s+
    (?P<offset>[0-9a-f]+)
    \s+
    (?P<device>[0-9a-f]+:[0-9a-f]+) # Device
    \s+
    (?P<inode>[0-9]+)
    \s*
    (?P<pathname>.*)
    $
    """,
    re.VERBOSE,
)


@dataclasses.dataclass
class Vma:
    start: int
    stop: int
    read: bool
    write: bool
    execute: bool
    shared: bool
    device: Tuple[int, int]
    inode: int
    pathname: Optional[str]

    @property
    def perms(self):
        return f"{'r' if self.read else '-'}{'w' if self.write else '-'}{'x' if self.execute else '-'}{'s' if self.shared else 'p'}"

    def __str__(self) -> str:
        return f"{self.start:x}-{self.stop:x} {self.perms} {self.device[0]:x}:{self.device[1]:x} {self.inode} {self.pathname}"


def get_vmas(pid: int) -> List[Vma]:
    vmas: List[Vma] = []
    with open(f"/proc/{pid}/maps", "rt") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            match = MAPS_RE.match(line)
            if match is None:
                raise Exception(f"Could not parse maps line: {line}")
            device_id = match.group("device")
            device_id
            vma = Vma(
                int(match.group("start"), 16),
                int(match.group("stop"), 16),
                match.group("flags")[0] == "r",
                match.group("flags")[1] == "w",
                match.group("flags")[2] == "x",
                match.group("flags")[3] == "s",
                tuple(map(lambda x: int(x, 16), match.group("device").split(":"))),
                int(match.group("inode"), 10),
                match.group("pathname"),
            )
            vmas.append(vma)
    return vmas


BUFFLEN = 10 * 4096


def match_perms(requested_permissions: str, permissions: str):
    """
    Check if a given permis value matched with a specified filter
    """
    return all(
        requested_permission == "." or requested_permission == permission
        for requested_permission, permission in zip(requested_permissions, permissions)
    )


@click.command()
@click.option("-p", "--pid", "pid", type=int, required=True, help="Process to dump.")
@click.option(
    "-P",
    "--perms",
    "perms",
    type=str,
    default="rw..",
    help="Requested VMA permissions (eg. rwxs, ...p, etc.)",
)
def main(pid: int, perms: str):
    """
    Dump a process memory to stdout.

    It works without stopping the process, without ptrace.
    It needs Linux >= 3.2.

    It might be useful eg. piped to the 'strings' command.
    """
    if len(perms) != 4:
        raise Exception("Invalid perms filter")

    vmas = get_vmas(pid)
    with open(f"/proc/{pid}/mem", "rb") as file:
        for vma in vmas:
            import sys

            sys.stderr.write(str(vma) + "\n")
            # Check VMS permissions againt requested ones:
            if not match_perms(perms, vma.perms):
                continue
            file.seek(vma.start)
            count = vma.stop - vma.start
            while count > 0:
                buffer = file.read(min(BUFFLEN, count))
                count = count - len(buffer)
                stdout.buffer.write(buffer)
        stdout.buffer.flush()


if __name__ == "__main__":
    main()
