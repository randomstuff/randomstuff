#!/usr/bin/python3

"""
Execute a program when a global keyboard shortcut is triggered.

Example:

    keybinder "<Control>m" pactl set-sink-mute @DEFAULT_SOURCE@ toggle
"""

import gi
import signal
import argparse
import time
from typing import Optional
import datetime

gi.require_version("Gtk", "3.0")
gi.require_version("Keybinder", "3.0")
gi.require_version("Notify", "0.7")
from gi.repository import Keybinder, GLib, Gtk, Notify


class App:

    start_time: Optional[float]
    notification: Optional[Notify.Notification]

    def __init__(self):
        self.start_time = None
        self.notification = None

    def start_callback(self, key):
        if self.start_time is not None:
            return
        self.start_time = time.monotonic_ns()
        self.notify("Timer start")

    def stop_callback(self, key):
        if self.start_time is None:
            return
        duration = time.monotonic_ns() - self.start_time
        self.start_time = None
        duration_s = duration / 1e9
        d = datetime.timedelta(microseconds=duration / 1000)
        self.notify(f"Timer stop, duration = {d}")

    def start_stop_callback(self, key):
        if self.start_time is None:
            self.start_callback(key)
        else:
            self.stop_callback(key)

    def restart_callback(self, key):
        if self.start_time is None:
            self.start_callback(key)
            return
        new_time = time.monotonic_ns()
        duration = new_time - self.start_time
        self.start_time = new_time
        duration_s = duration / 1e9
        d = datetime.timedelta(microseconds=duration / 1000)
        message = f"Timer restart, duration = {d}"
        self.notify(message)

    def notify(self, message):
        print(message)
        if self.notification is not None:
            self.notification.close()
        self.notification = Notify.Notification.new(message, "", "dialog-information")
        self.notification.show()


epilog = """example:

  global-stopwatch.py --start F1 --stop F2 --restart F3 --startstop F4
  global-stopwatch.py --start '<Super>F11' --stop '<Super>F12'
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Desktop stopwatch based on global keybindings.",
        allow_abbrev=False,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--start", required=False, help="Start keybinding(s)")
    parser.add_argument("--stop", required=False, help="Stop keybinding(s)")
    parser.add_argument("--restart", required=False, help="Restart keybinding(s)")
    parser.add_argument("--startstop", required=False, help="Start/stop keybinding(s)")
    args = parser.parse_args()

    app = App()
    Notify.init("GlobalStopWatch")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.init()
    Keybinder.init()
    if args.start:
        for key in args.start.split(","):
            Keybinder.bind(key, app.start_callback)
    if args.stop:
        for key in args.stop.split(","):
            Keybinder.bind(key, app.stop_callback)
    if args.startstop:
        for key in args.startstop.split(","):
            Keybinder.bind(key, app.start_stop_callback)
    if args.restart:
        for key in args.restart.split(","):
            Keybinder.bind(key, app.restart_callback)
    Gtk.main()
