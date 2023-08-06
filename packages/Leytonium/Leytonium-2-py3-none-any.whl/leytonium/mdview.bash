set -e

path=$(mktemp)

function cleanup {
    rm -fv $path
}

trap cleanup EXIT

pandoc -T "$(basename "${@: -1}")" --toc "$@" >$path

firefox $path

while true; do sleep 1; done
