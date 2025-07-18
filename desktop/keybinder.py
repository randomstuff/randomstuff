#!/usr/bin/python3

"""
Execute a program when a global keyboard shortcut is triggered.

Example:

    keybinder "<Control>m" pactl set-sink-mute @DEFAULT_SOURCE@ toggle
"""

import sys
import gi
import os
import signal

gi.require_version("Gtk", "3.0")
gi.require_version("Keybinder", "3.0")
from gi.repository import Keybinder
from gi.repository import Gtk


def callback(x):
    os.spawnvp(os.P_NOWAIT, sys.argv[2], sys.argv[2:])


signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.init()
Keybinder.init()
Keybinder.bind(sys.argv[1], callback)
Gtk.main()
