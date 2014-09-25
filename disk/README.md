# Crappy scripts to mount disk image (such as ISOs) using udisks2

Simple scripts which use the dbus udisks2 API to mount disk images
without begin root. Similar to pmout but for disk images.

Usage (CLI):

    cd $(mount-diskimage foobar.iso)

Usage (GUI):

    open-diskimage foobar.iso
