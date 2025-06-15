#!/usr/bin/python3
#
# Examples usage
#   host="$(list-ssh-hosts | fzf -e --smart-case)" && ssh "$host"

from os.path import expanduser, exists
import re
from glob import glob

INCLUDE_RE = re.compile("^\\s*include +", flags=re.I)
HOST_RE = re.compile("^\\s*host +", flags=re.I)

IGNORED_HOSTS = set([".host", "machine/.host"])

to_process_files = [
    "/etc/ssh/ssh_config",
    expanduser("~/.ssh/config"),
]

processed_files = set()
hosts = set()

while to_process_files:
    config_file = to_process_files.pop(0)
    if config_file in processed_files:
        continue
    processed_files.add(config_file)

    if not exists(config_file):
        continue

    with open(config_file, "rt") as f:

        for line in f:
            match = INCLUDE_RE.match(line)
            if match:
                found_include = line[match.end(0) :].strip()
                found_include = expanduser(found_include)
                for include in glob(found_include):
                    if include not in processed_files:
                        to_process_files.append(include)
                continue
            match = HOST_RE.match(line)
            if match:
                found_hosts = line[match.end(0) :].strip()
                for host in re.split(r"\s+", found_hosts):
                    if host and "*" not in host and host not in IGNORED_HOSTS:
                        hosts.add(host)
                continue

known_host_file = expanduser("~/.ssh/known_hosts")
if exists(known_host_file):
    with open(known_host_file, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            host = line.split(" ")[0].strip().split(",")[0]
            if host and host not in IGNORED_HOSTS:
                hosts.add(host)

for host in sorted(hosts):
    print(host)
