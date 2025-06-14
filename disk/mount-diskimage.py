#!/usr/bin/python 

# Mount an image (ISO) using udisks2.
# Usage: open-image foobar.iso
# Dependencies: python, python-dbus, udisks2

import dbus
import os
import sys

fd = os.open(sys.argv[1], os.O_RDONLY)
bus = dbus.SystemBus()
manager = bus.get_object("org.freedesktop.UDisks2",
                        "/org/freedesktop/UDisks2/Manager")
loop = dbus.Interface(manager, "org.freedesktop.UDisks2.Manager").LoopSetup(fd, {})
loop = bus.get_object("org.freedesktop.UDisks2", loop)
path = dbus.Interface(loop, "org.freedesktop.UDisks2.Filesystem").Mount({})
dbus.Interface(loop, "org.freedesktop.UDisks2.Loop").SetAutoclear(True, {})
sys.stdout.write(path)
sys.exit(0)
