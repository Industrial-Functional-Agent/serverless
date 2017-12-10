import json

from aws_clients import LambdaClient, IamClient, CloudWatchEventsClient

# We assume that you have followed the instructions in
# http://boto3.readthedocs.io/en/latest/guide/configuration.html to 
# configure your AWS credentials. If for some reason this does not work 
# for you, passing aws_access_key_id and aws_secret_access_key directly 
# as named arguments should work.
lambda_client = LambdaClient()
iam_client = IamClient()
event_client = CloudWatchEventsClient()


def create_function(**environment_variables):
    role = iam_client.get_or_create_role()
    lambda_client.create_function(
        role=role,
        **environment_variables
    )


def update_function():
    lambda_client.update_function_code()


def invoke_function():
    lambda_client.invoke()


def delete_all_resources():
    lambda_client.delete_function()
    iam_client.delete_role()


if __name__ == "__main__":
    with open('slack_config.json', 'r') as f:
        slack_config = json.load(f)
        try:
            create_function(
                SLACK_CHANNEL=slack_config['slack-channel'],
                SLACK_TOKEN=slack_config['slack-token'],
            )
        except:
            update_function()

        function_config = lambda_client.get_function_configuration()
        event_client.create_rule(rate=2)
        event_client.put_targets(function_config)
        lambda_client.add_permission(function_config)

    # invoke_function()
