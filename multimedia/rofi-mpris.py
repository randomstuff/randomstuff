#!/usr/bin/python3

"""
MPRIS mode for rofi
"""

import dbus
import sys
import os


PATH = "/org/mpris/MediaPlayer2"
ROOT_IFACE = "org.mpris.MediaPlayer2"
PLAYER_IFACE = "org.mpris.MediaPlayer2.Player"
TRACKLIST_IFACE = "org.mpris.MediaPlayer2.TrackList"
PROP_IFACE = "org.freedesktop.DBus.Properties"


bus = dbus.SessionBus()


def get_mpris_names():
    result = []
    for bus_name in bus.list_names():
        if bus_name.startswith("org.mpris.MediaPlayer2."):
            try:
                get_tracks(bus_name)
            except:
                continue
            name = get_object(bus_name, PROP_IFACE).Get(ROOT_IFACE, "Identity")
            result.append((bus_name, name))
    return result


def guess_mpris_name():
    return max(
        (name for (name, _) in get_mpris_names()),
        key=lambda name: len(get_tracks(name)),
    )


def get_object(bus_name, interface):
    object = bus.get_object(bus_name, PATH)
    return dbus.Interface(object, interface)


def get_tracks(bus_name):
    tracks = get_object(bus_name, PROP_IFACE).Get(TRACKLIST_IFACE, "Tracks")
    return get_object(bus_name, TRACKLIST_IFACE).GetTracksMetadata(tracks)


if os.environ.get("ROFI_RETV") is not None:

    # TODO, add player selector
    bus_name = guess_mpris_name()

    # User selection:
    if len(sys.argv) > 1:
        track_id = os.environ["ROFI_INFO"]
        get_object(bus_name, TRACKLIST_IFACE).GoTo(track_id)

    # Generate tracks menu:
    else:

        tracks = get_tracks(bus_name)

        print("\0prompt\x1fTrack\n")

        try:
            current_track_id = (
                get_object(bus_name, PROP_IFACE)
                .Get(PLAYER_IFACE, "Metadata")
                .get("mpris:trackid")
            )
            for i, track in enumerate(tracks):
                if track["mpris:trackid"] == current_track_id:
                    print("\0active\x1f" + str(i) + "\n")
                    break
        except:
            pass

        for track in tracks:
            track_id = track["mpris:trackid"]
            track_url = track.get("xesam:url")
            track_title = track.get("xesam:title") or track_url
            print(track_title + "\0info\x1f" + track_id + "\n")

# Direct execution outside of rofi:
else:
    argv0 = sys.argv[0]
    os.execvp("rofi", ["rofi", "-show", "mpris", "-modes", "mpris:" + argv0])
    os.exit(255)
