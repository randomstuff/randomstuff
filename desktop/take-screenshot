#!/bin/sh
# Just take a screenshot.
# Designed to be bound to "Prind Screen"

set -e
dir=$(xdg-user-dir PICTURES) || dir="$HOME"
scrot "$dir/screenshot_$(date -u +%Y-%m-%dT%H:%M:%SZ).png"
notify-send -a take-screenshot -i video-display -t 2000 "Screenshot"
