#!/bin/sh
# OCR japanese text from selection and send to clipboard.

set -e

result=$(
maim -s |
mogrify -brightness-contrast 0,100 png:- |
tesseract -l jpn - - |
tr -d " "
)

printf "%s\n" "$result" | xclip -selection clipboard -i

notify-send -a "$0" -- "OCR result" "$result"
