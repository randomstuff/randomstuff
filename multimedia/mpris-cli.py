#!/usr/bin/python3

"""
MPRIS CLI client

This CLI tool can be used to control a MPRIS compatible
multimedia player such as VLC.

Available actions:

* list-applications/list-apps
* identity
* quit
* raise
* play-pause
* pause
* play
* stop
* previous/prev
* next
* open
* tracks, list available TRACKS (JSON lines)
* goto TRACK
"""

import sys
import json
import dbus
import argparse


MPRIS_PATH = "/org/mpris/MediaPlayer2"
MPRIS_IFACE = "org.mpris.MediaPlayer2"
PLAYER_IFACE = "org.mpris.MediaPlayer2.Player"
TRACKLIST_IFACE = "org.mpris.MediaPlayer2.TrackList"
PROP_IFACE = "org.freedesktop.DBus.Properties"

DBUS_NAME = "org.freedesktop.DBus"
DBUS_IFACE = "org.freedesktop.DBus"
DBUS_PATH = "/org/freedesktop/DBus"

parser = argparse.ArgumentParser(
    description=__doc__,
    allow_abbrev=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("-a", "--application", help="Application ID", default=None)
parser.add_argument("--object", help="Application object name", default=None)
parser.add_argument("action", help="Action", default="-")
parser.add_argument("args", nargs="*", default=[], help="Additional arguments")

args = parser.parse_args()
action = args.action


def get_object(bus_name, path, interface):
    if bus_name is None:
        raise Exception("Missing bus name")
    bus = dbus.SessionBus()
    object = bus.get_object(bus_name, MPRIS_PATH)
    return dbus.Interface(object, interface)


if action == "list-apps" or action == "list-applications":
    names = get_object(DBUS_NAME, DBUS_PATH, DBUS_IFACE).ListNames()
    for name in names:
        if name.startswith("org.mpris.MediaPlayer2."):
            print(name)
    exit(0)

if args.object is not None:
    bus_name = args.object
elif args.application is not None:
    bus_name = "org.mpris.MediaPlayer2." + args.application
else:
    bus_name = None

if action == "identity":
    print(get_object(bus_name, MPRIS_PATH, PROP_IFACE).Get(MPRIS_IFACE, "Identity"))
elif action == "quit":
    get_object(bus_name, MPRIS_PATH, MPRIS_IFACE).Quit()
elif action == "raise":
    get_object(bus_name, MPRIS_PATH, MPRIS_IFACE).Raise()
elif action == "play-pause":
    get_object(bus_name, MPRIS_PATH, PLAYER_IFACE).PlayPause()
elif action == "pause":
    get_object(bus_name, MPRIS_PATH, PLAYER_IFACE).Pause()
elif action == "play":
    get_object(bus_name, MPRIS_PATH, PLAYER_IFACE).Play()
elif action == "stop":
    get_object(bus_name, MPRIS_PATH, PLAYER_IFACE).Stop()
elif action == "previous" or action == "prev":
    get_object(bus_name, MPRIS_PATH, PLAYER_IFACE).Previous()
elif action == "next":
    get_object(bus_name, MPRIS_PATH, PLAYER_IFACE).Next()
elif action == "open":
    get_object(bus_name, MPRIS_PATH, PLAYER_IFACE).OpenUri(args.args[0])
elif action == "tracks":
    tracks = get_object(bus_name, MPRIS_PATH, PROP_IFACE).Get(TRACKLIST_IFACE, "Tracks")
    metadata = get_object(bus_name, MPRIS_PATH, TRACKLIST_IFACE).GetTracksMetadata(
        tracks
    )
    for value in metadata:
        print(json.dumps(value))
elif action == "goto":
    get_object(bus_name, MPRIS_PATH, TRACKLIST_IFACE).GoTo(args.args[0])
else:
    sys.stderr.write("Invalid command\n")
    exit(1)
