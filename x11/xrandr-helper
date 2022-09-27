#!/bin/sh
# Helper for xrandr.
# randr-helper toggle ~ toggle active video output device / screen

set -e

screen=0

display_help() {
    echo "$0 ~ xrandr helper"
    echo "USAGE:"
    echo "  $0 help ~ show help"
    echo "  $0 toggle ~ toggle display output"
    # TODO, mirror mode
}

toggle_output() {
    outputs=$(xrandr --screen $screen | grep '^[-A-Z0-9]* ' | grep -o '^[-A-Z0-9]*' || true)
    connected_outputs=$(xrandr --screen $screen | grep '^[-A-Z0-9]* connected' | grep -o '^[-A-Z0-9]*' || true)
    disconnected_outputs=$(xrandr --screen $screen | grep '^[-A-Z0-9]* disconnected' | grep -o '^[-A-Z0-9]*' || true)
    enabled_outputs=$(xrandr --screen $screen | grep '^[-A-Z0-9]* connected' | grep -F '+' | grep -o '^[-A-Z0-9]*' || true)
    disabled_outputs=$(xrandr --screen $screen | grep '^[-A-Z0-9]* connected' | grep -v -F '+' | grep -o '^[-A-Z0-9]*' || true)

    target_output=""
    found=false
    for output in $connected_outputs; do
        if test -z "$target_output"; then
            target_output="$output"
        fi
        case $output in
            $enabled_outputs)
                found=true
            ;;
            $disabled_outputs)
                if $found; then
                    target_output="$output"
                    break
                fi
            ;;
        esac
    done

    for output in $disconnected_outputs; do
        xrandr --screen $screen --output "$output" --off
    done
    for output in $connected_outputs; do
        if test "$output" != "$target_output"; then
            xrandr --screen $screen --output "$output" --off
        fi
    done
    xrandr --screen $screen --output "$target_output" --auto
    xrandr --screen $screen --output "$target_output" --primary
}

if test $# = 0; then
    display_help
fi
command="$1"
shift
case "$command" in
    toggle)
        toggle_output "$@"
    ;;
    help | --help)
        display_help "$@"
    ;;
    *)
        printf "Invalid command" >&2
        exit 1
    ;;
esac
