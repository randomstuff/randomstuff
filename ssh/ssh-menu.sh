#!/bin/sh

set -e
host="$(list-ssh-hosts | fzf -e --smart-case)"
exec ssh "$host"
