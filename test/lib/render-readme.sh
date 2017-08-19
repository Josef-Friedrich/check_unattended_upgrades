#! /bin/sh

export PROJECT_NAME="$(basename "$(pwd)")"
export USAGE="$(./$PROJECT_NAME --help)"
export SHORT_DESCRIPTION="$(./$PROJECT_NAME --short-description)"

chmod a+x README.md.template.sh
./README.md.template.sh > README.md
