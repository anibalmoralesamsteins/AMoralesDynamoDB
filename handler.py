import json
import boto3
import requests
from datetime import date

# Get the service resource.
dynamodb = boto3.resource('dynamodb',
    aws_access_key_id= 'DEFAULT_ACCESS_KEY',
    aws_secret_access_key= 'DEFAULT_SECRET',
    endpoint_url="http://localhost:8000"
)

def listar(event, context):
    table = dynamodb.Table('dolar')
    response = table.scan()
    items = response['Items']
    print(items)
    return {"statusCode": 200, "body": str(items)}

def create(event, context):
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='dolar',
        KeySchema=[
            {
                'AttributeName': 'dolar',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'dolar',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.wait_until_exists()

    # Print out some data about the table.
    print(table.item_count)

def insert(event, context):

    today = str(date.today())
    print(today)

    valorUSD = str(requests.get(url = 'https://mindicador.cl/api/dolar').json()['serie'][0]['valor'])
    print(valorUSD)

    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table('dolar')

    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    table.put_item(
        Item={
                'dolar': today+' $'+valorUSD
            }
        )

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
