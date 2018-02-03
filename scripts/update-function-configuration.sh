#!/usr/bin/env bash

aws --profile ifa lambda \
    update-function-configuration \
    --function-name JoongonaraToSlackFunction \
    --environment "{\"Variables\":{\"SLACK_CHANNEL\":\"${SLACK_CHANNEL}\",\"SLACK_TOKEN\":\"${SLACK_TOKEN}\"}}"