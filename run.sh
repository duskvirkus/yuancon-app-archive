!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CAPTURE_DIR=$(realpath $SCRIPT_DIR/../capture/)
TIMESTAMPPED_CAPTURE=$CAPTURE_DIR/$(date +"%Y-%m-%dT%H:%M:%S")

echo Saving to $TIMESTAMPPED_CAPTURE

if [[ $2 -eq 'clean' ]]; then
    rm -rf $CAPTURE_DIR/*
fi

mkdir $TIMESTAMPPED_CAPTURE

# credit https://gist.github.com/crittermike/fe02c59fed1aeebd0a9697cf7e9f5c0c
cd $TIMESTAMPPED_CAPTURE && wget \
    --recursive \
    --page-requisites \
    --adjust-extension \
    --span-hosts \
    --convert-links \
    --restrict-file-names=windows \
    --domains yuancon.app \
    --no-parent \
    https://yuancon.app/