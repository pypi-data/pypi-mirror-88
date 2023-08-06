set -e

sudo apt-get update

sudo apt-get --with-new-pkgs upgrade

sudo apt-get autoremove

touchpath=~/var/last-upgrade

mkdir -p "$(dirname "$touchpath")"

touch "$touchpath"
