# Mount disk image (such as ISOs) using udisks2

Simple scripts which use the dbus udisks2 API to mount disk images
without begin root.

Similar to pmount but for disk images.

Usage (CLI):

    cd "$(mount-diskimage foobar.iso)"

Usage (GUI):

    xdg-open "$(mount-diskimage foobar.iso)"

You can use any file manager instead (nautilG us, thunar, dolphin, pcmanfm, etc.).

Some file manager provide an option to unmount the disk:

* thunar;

* pcmanfm;

* older versions of nautilus (I can't find the option on the latest version).
