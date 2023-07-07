#!/usr/bin/env bash

set -eu

MODEL="base"
LANG="en"

script_dir="$(realpath "$(dirname "${0}")")"

if [ ! $(docker images | grep "whisper-${MODEL}" ) ]; then
    docker build -t whisper-${MODEL} --build-arg model=${MODEL} "${script_dir}"
fi

docker run --rm -it \
    --privileged -v /dev/bus/usb:/dev/bus/usb \
    --name whisper.cpp \
    whisper-${MODEL} \
    stream \
        --model /root/models/ggml-${MODEL}.bin \
        --language ${LANG} \
        --step 0 \
        -t 6 \
        --length 3000 \
        -vth 0.7 \
        -fth 155
