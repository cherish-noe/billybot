#!/bin/bash

repo_name="billy-bot"

build() {
    pushd docker

    rm -rf billy-bot
    mkdir billy-bot
    cp -R ../{.streamlit,chroma_storage,pages,utils,img} billy-bot
    cp ../{requirements.txt,app.py,.env} billy-bot

    docker build -t "$repo_name" --progress=plain .

    #popd
}

if [[ "$1" == "--build" ]]; then
    build
else
    echo "usage: ./docker_build --build"
fi
