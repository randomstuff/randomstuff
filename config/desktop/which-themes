#!/bin/sh
# Which themes are available in both GTK2 and GTK3?

cd /usr/share/themes

for a in * ; do
  if test -d $a/gtk-2.0 -a -d $a/gtk-3.0 ; then
    echo $a
  fi
done
