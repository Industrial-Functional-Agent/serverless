#!/usr/bin/env bash

ZIP_FILE_NAME="JoongonaraToSlack.zip"
FUNCTION_NAME="JoongonaraToSlackFunction"
EVENT_RULE_NAME="JoonggonaraToSlackEvent"
IAM_ROLE_NAME="lambda_basic_execution"

aws --profile ifa s3 \
    cp \
    ${ZIP_FILE_NAME} \
    s3://fakenerd

IAM_ROLE_ARN=$(aws --profile ifa iam \
    get-role \
    --role-name ${IAM_ROLE_NAME} \
    --query Role.Arn \
    | sed s/\"//g)

aws --profile ifa lambda \
    create-function \
    --function-name ${FUNCTION_NAME} \
    --runtime python3.6 \
    --role ${IAM_ROLE_ARN} \
    --handler main.handler \
    --code S3Bucket=fakenerd,S3Key=${ZIP_FILE_NAME} \
    --environment "{\"Variables\":{\"SLACK_CHANNEL\":\"${SLACK_CHANNEL}\",\"SLACK_TOKEN\":\"${SLACK_TOKEN}\"}}" \

aws --profile ifa events \
    put-rule \
    --cli-input-json "{\"Name\": \"$EVENT_RULE_NAME\", \"ScheduleExpression\": \"rate(2 minutes)\"}" \

FUNCTION_ARN=$(aws --profile ifa lambda \
    get-function-configuration \
    --function-name ${FUNCTION_NAME} \
    --query FunctionArn \
    | sed s/\"//g)

EVENT_RULE_ARN=$(aws --profile ifa events \
    describe-rule \
    --name ${EVENT_RULE_NAME} \
    --query Arn \
    | sed s/\"//g)

aws --profile ifa events \
    put-targets \
    --rule ${EVENT_RULE_NAME} \
    --targets "Id"="$FUNCTION_NAME","Arn"="$FUNCTION_ARN"

aws --profile ifa lambda \
    add-permission \
    --function-name ${FUNCTION_NAME} \
    --statement-id ${EVENT_RULE_NAME} \
    --action "lambda:InvokeFunction" \
    --principal events.amazonaws.com \
    --source-arn ${EVENT_RULE_ARN}
