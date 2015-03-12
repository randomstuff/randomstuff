#!/bin/sh

# Filter the content of the clipboard/selection through a UNIX filter.
# Examples:
#    gui_filter clipboard base64
#    gui_filter clipboard base64 -d
#    gui_filter clipboard cowsay

mode="$1"
shift

case "$mode" in
  primary | seconday | clipboard)
    xclip -out -selection "$mode" | command "$@" | xclip -in -selection "$mode"
    ;;
  selection)
    # This is an horrible hack.
    # It only works for C-c/C-v keybindings.
    sleep 0.1
    xdotool key control+c
    sleep 0.1
    xclip -out -selection clipboard | command "$@" | xclip -in -selection clipboard
    xdotool key control+v
    ;;
esac
