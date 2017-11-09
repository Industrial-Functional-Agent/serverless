import decimal
import json

import boto3
from botocore.exceptions import ClientError


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(0)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(0)

dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2", endpoint_url="http://localhost:8000")

table = dynamodb.Table("Movies")

title = "The Big New Movie"
year = 2015

try:
    response = table.get_item(
        Key={
            "year": year,
            "title": title
        }
    )
except ClientError as e:
    print(e.response["Error"]["Message"])
else:
    item = response["Item"]
    print("GetItem succeeded:")
    print(json.dumps(item, indent=4, cls=DecimalEncoder))
