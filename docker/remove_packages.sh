#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get purge -y --auto-remove "$@"
rm -rf /var/lib/apt/lists /var/cache/apt/archives
