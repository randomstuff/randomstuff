#!/bin/bash
# Poor man's (Java) Profiler ~ Deluxe edition
#  http://poormansprofiler.org/
#  http://dom.as/tag/gdb/
# The deluxe addition have some kind-of argument handling.

set -e

sleeptime="0.1"
nsamples=""
process=""
mode="gdb"

while [ $# != 0 ]; do
    case "$1" in
        -n)
            # Limit the number of samples to take:
            nsamples="$2"
            shift 2
            ;;
        -s)
            # Waiting time between samples (in secondes):
            sleeptime="$2"
            shift 2
            ;;
        --generic)
            # Use GDB for sampling:
            mode=generic
            shift
            ;;
        --gdb)
            # Use GDB for sampling:
            mode=gdb
            shift
            ;;
        --jcmd)
            # Use jcmd for sampling (Java processes):
            mode=jcmd
            shift
            ;;
        --jstack)
            # Use jstack for sampling (Java processes):
            mode=jstack
            shift
            ;;
        --elfutils)
            # Use elfutils for sampling:
            mode=elfutils
            elfutils_stack="$(which eu-stack || which stack)"
            shift
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "Unexpected argument" >&2
            exit 1
            ;;
        *)
            process="$1"
            shift
            ;;
    esac
done

sample_gdb() {
    gdb -ex "set pagination 0" -ex "thread apply all bt" -batch -p "$process" "$@" 2> /dev/null
}
sample_elfutils() {
    "$elfutils_stack" -p "$process" "$@"
}
sample_jstack() {
    jstack "$process" "$@"
}
sample_jcmd() {
    jcmd "$process" Thread.print "$@"
}
sample_generic() {
    "$@"
}

if [ "$nsamples" == "" ]; then
    while true; do
        "sample_$mode" "$@"
        sleep "$sleeptime"
    done
else
    sample=$((0))
    while [ "$sample" -lt "$nsamples" ]; do
        "sample_$mode" "$@"
        sleep "$sleeptime"
        sample=$(($sample + 1))
    done
fi
