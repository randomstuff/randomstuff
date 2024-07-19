#!/usr/bin/python3

import subprocess
import json


def run_command(args):
    cmd = subprocess.run(args, capture_output=True)
    if cmd.returncode != 0:
        exit(cmd.returncode)
    return cmd.stdout.decode("UTF-8")


list = json.loads(run_command(["pactl", "-fjson", "list"]))
sinks_names = [sink["name"] for sink in list["sinks"]]
print(sinks_names)

default_sink = run_command(["pactl", "get-default-sink"]).strip()
try:
    default_sink_index = sinks_names.index(default_sink)
    print(default_sink_index)
    if default_sink_index + 1 < len(sinks_names):
        new_sink_name = sinks_names[default_sink_index + 1]
    else:
        new_sink_name = sinks_names[0]
except ValueError as e:
    new_sink_name = sinks_names[0]
run_command(["pactl", "set-default-sink", new_sink_name])
