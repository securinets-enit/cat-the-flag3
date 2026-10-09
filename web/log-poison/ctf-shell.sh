#!/bin/sh
set -eu
set -f

command_line="${1-}"
[ -n "$command_line" ] || exit 2

set -- $command_line
command_name="${1-}"
shift || true

case "$command_name" in
    cat|ls)
        exec "/bin/$command_name" "$@"
        ;;
    *)
        echo "command not allowed" >&2
        exit 126
        ;;
esac