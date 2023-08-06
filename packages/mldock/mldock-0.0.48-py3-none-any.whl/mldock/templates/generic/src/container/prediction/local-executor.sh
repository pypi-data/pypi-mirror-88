#!/usr/bin/env bash

function startup (){
    python src/container/prediction/startup.py --env='dev'
}

startup

exec "$@"

wait

echo "Complete!"