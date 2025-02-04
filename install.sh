#!/bin/bash
set -e

# Argument parsing
SHORT=r,d:,p:,s:,h
LONG=remove,dest-dir:,prefix-dir:,no-sudo,no-pip-install,help
VALID_ARGS=$(getopt -a --options $SHORT --longoptions $LONG -- "$@")
if [[ $? -ne 0 ]]; then
    exit 1;
fi

PREFIX_DIR="/usr"
DEST_DIR=""
SHOULD_REMOVE=false
NO_SUDO=false
NO_PIP_INSTALL=false

eval set -- "$VALID_ARGS"
while true; do
  case "$1" in
    '--remove' | '-r')
        SHOULD_REMOVE=true
        ;;
    '--prefix-dir' | '-p')
        PREFIX_DIR=$2
        shift
        ;;
    '--dest-dir' | '-d')
        DEST_DIR=$2
        shift
        ;;
    '--no-sudo')
        NO_SUDO=true
        ;;
    '--no-pip-install')
        NO_PIP_INSTALL=true
        ;;
    '--help' | '-h')
        echo "Usage: $0 [--remove,-r] [--dest-dir,-d <installation destination directory (defaults to $DEST_DIR)>] [--prefix-dir,-p <installation prefix directory (defaults to $PREFIX_DIR)>] [--no-sudo] [--no-pip-install]" 1>&2
        exit 0
        ;;
    --)
        break
        ;;
  esac
  shift
done

# Root check
if [ "$EUID" -ne 0 ] && [ "$NO_SUDO" = false ]
  then echo "This program requires root permissions or use the '--no-sudo' option"
  exit 1
fi

function build() {
    echo "building package"
    rm -rf "dist/" 2> "/dev/null" || true
    python -m build -s
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2> "/dev/null" || true
}

function uninstall() {
    if [ "$NO_PIP_INSTALL" = false ]; then
        echo "uninstalling python package"
        python -m pip uninstall -y fw-fanctrl 2> "/dev/null" || true
    fi
}

function install() {
    build

    if [ "$NO_PIP_INSTALL" = false ]; then
        echo "installing python package"
        python -m pip install --prefix="$DEST_DIR$PREFIX_DIR" dist/*.tar.gz
        which python
        rm -rf "dist/" 2> "/dev/null" || true
    fi
}

if [ "$SHOULD_REMOVE" = true ]; then
    uninstall
else
    install
fi
exit 0
