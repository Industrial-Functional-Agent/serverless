import decimal
import json

import boto3


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

response = table.update_item(
    Key={
        "year": year,
        "title": title
    },
    UpdateExpression="set info.rating = info.rating + :val",
    ExpressionAttributeValues={
        ":val": decimal.Decimal(1)
    },
    ReturnValues="UPDATED_NEW"  # return only the updated attributes
)

print("UpdateItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))
