import json

import boto3
from botocore.exceptions import ClientError


class AWSClient:
    def __init__(self, client_name, *args, **kwargs):
        self.session = boto3.Session(profile_name='ifa')
        self._client = self.session.client(client_name, *args, **kwargs)


class IamClient(AWSClient):
    def __init__(self, *args, **kwargs):
        super().__init__('iam', *args, **kwargs)
        self._role_name = 'lambda_basic_execution'
        self._role_policy_document_name = 'role_policy_document.json'

    @property
    def role_name(self):
        return self._role_name

    @property
    def role_policy_document_name(self):
        return self._role_policy_document_name

    def _get_role_policy_document(self):
        with open(self.role_policy_document_name, 'r') as f:
            role_policy_document_json = f.read()
            return json.loads(role_policy_document_json)

    def create_role(self):
        return self._client.create_role(
            RoleName=self.role_name,
            AssumeRolePolicyDocument=json.dumps(self._get_role_policy_document()),
        )

    def get_role(self):
        return self._client.get_role(
            RoleName=self.role_name
        )

    def delete_role(self):
        return self._client.delete_role(
            RoleName=self.role_name
        )

    def get_or_create_role(self):
        try:
            return self.get_role()
        except ClientError:
            return self.create_role()


class LambdaClient(AWSClient):
    def __init__(self, *args, **kwargs):
        super().__init__('lambda', *args, **kwargs)
        self._function_name = 'JoongoToSlack'
        self._function_code_zip_file_name = 'JoongoToSlack.zip'

    @property
    def function_name(self):
        return self._function_name

    @property
    def function_code_zip_file_name(self):
        return self._function_code_zip_file_name

    def invoke(self):
        return self._client.invoke(
            FunctionName=self.function_name,
            InvocationType='Event',
        )

    def _get_zipped_function_code(self):
        with open(self.function_code_zip_file_name, 'rb') as f:
            code = f.read()
            return code

    def update_function_code(self):
        return self._client.update_function_code(
            FunctionName=self.function_name,
            ZipFile=self._get_zipped_function_code(),
        )

    def create_function(self, role, **env_variables):
        return self._client.create_function(
            FunctionName=self.function_name,
            Runtime='python3.6',
            Role=role['Role']['Arn'],
            Handler='main.handler',
            Code=dict(
                ZipFile=self._get_zipped_function_code(),
            ),
            Description='Sends crawled text to Slack',
            Timeout=60,
            MemorySize=512,
            Environment=dict(
                Variables=env_variables,
            ),
        )

    def update_function_configuration(self, **env_variables):
        return self._client.update_function_configuration(
            FunctionName=self.function_name,
            Environment=dict(
                Variables=env_variables,
            ),
        )

    def delete_function(self):
        return self._client.delete_function(
            FunctionName=self.function_name,
        )

    def get_function(self):
        return self._client.get_function(
            FunctionName=self.function_name,
        )

    def get_function_configuration(self):
        return self._client.get_function_configuration(
            FunctionName=self.function_name,
        )

    def add_permission(self):
        return self._client.add_permission(
            FunctionName=self.function_name,
            StatementId='AnyUniqueString',
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            # SourceArn='string',
        )


class CloudWatchEventsClient(AWSClient):
    def __init__(self, *args, **kwargs):
        super().__init__('events', *args, **kwargs)
        self.rule_name = 'JoongoToSlack'

    def create_rule(self, rate, role=None):
        return self._client.put_rule(
            Name=self.rule_name,
            ScheduleExpression='rate({} minutes)'.format(rate),
            State='ENABLED',
            # RoleArn=role['Role']['Arn'],
        )

    def enable_rule(self):
        return self._client.enable_rule(
            Name=self.rule_name,
        )

    def disable_rule(self):
        return self._client.disable_rule(
            Name=self.rule_name,
        )

    def delete_rule(self):
        return self._client.delete_rule(
            Name=self.rule_name,
        )

    def put_targets(self, function_config):
        return self._client.put_targets(
            Rule=self.rule_name,
            Targets=[
                {
                    'Id': function_config['FunctionName'],
                    'Arn': function_config['FunctionArn'],
                    # 'RoleArn': function_config['Role']['Arn'],
                },
            ]
        )

    def remove_targets(self, function_name):
        return self._client.remove_targets(
            Rule=self.rule_name,
            Ids=[
                function_name,
            ]
        )
