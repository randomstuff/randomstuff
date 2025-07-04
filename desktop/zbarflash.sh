#!/bin/sh
# Scan QR code from selection and send to clipboard.

set -e
result=$(maim -s | zbarimg - -q --raw)
printf "%s\n" "$result" | xclip -selection clipboard -i
notify-send -a "$0" -- "QR code scan" "$result"
