import argparse
import json

from aws_manager.aws_clients import LambdaClient, IamClient, CloudWatchEventsClient


lambda_client = LambdaClient()
iam_client = IamClient()
event_client = CloudWatchEventsClient()


def get_slack_config():
    f = open('slack_config.json', mode='r')
    return json.load(f)


def create_function(**environment_variables):
    try:
        role = iam_client.get_or_create_role()
        lambda_client.create_function(
            role=role,
            **environment_variables
        )
        lambda_client.add_permission()
    except:
        # FIXME: If there is function already, do we need to handle it?
        update_function(**environment_variables)


def update_function(**environment_variables):
    lambda_client.update_function_code()
    lambda_client.update_function_configuration(**environment_variables)


def delete_function():
    lambda_client.delete_function()


def enable_event():
    function_config = lambda_client.get_function_configuration()
    try:
        event_client.create_rule(rate=2)
        event_client.put_targets(function_config)
    except Exception as e:
        print(e)


def disable_event():
    event_client.disable_rule()


def delete_event():
    try:
        event_client.remove_targets(lambda_client.function_name)
    except Exception as e:
        print(e)
    event_client.delete_rule()


def main():
    parser = argparse.ArgumentParser(description='Manage AWS')
    parser.add_argument('--action', type=str, choices=['lambda', 'event'],
                        help='select aws action')
    parser.add_argument('--method', type=str, default='create',
                        choices=['create', 'update', 'delete'],
                        help='handle lambda function')
    parser.add_argument('--event', type=str, default='enable',
                        choices=['enable', 'disable', 'delete'],
                        help='handle cloud watch event')
    args = parser.parse_args()
    slack_config = get_slack_config()

    if args.action == 'lambda':
        if args.method == 'create':
            create_function(
                SLACK_CHANNEL=slack_config['slack-channel'],
                SLACK_TOKEN=slack_config['slack-token']
            )
        elif args.method == 'update':
            update_function(
                SLACK_CHANNEL=slack_config['slack-channel'],
                SLACK_TOKEN=slack_config['slack-token']
            )
        elif args.method == 'delete':
            delete_function()
    elif args.action == 'event':
        if args.event == 'enable':
            enable_event()
        elif args.event == 'disable':
            disable_event()
        elif args.event == 'delete':
            delete_event()


if __name__ == '__main__':
    main()
