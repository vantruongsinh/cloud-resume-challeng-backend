import json
import boto3
import botocore
from datetime import date


def lambda_handler(event, context):
    # TODO implement
    
    today = date.today()
    today_str = today.strftime("%A %d-%B-%Y")
    
    TABLE_NAME = "VisitorCount"
    REGION = 'us-east-1'
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    
    #today_str = 'Monday 30-January-2023'
    
    today_count = table.get_item(TableName=TABLE_NAME,Key={'Date':today_str})
    count = 0
    
    if today_count.get('Item',{}) == {}:
        with table.batch_writer() as batch:
            count = 1
            batch.put_item(Item={"Date": today_str, "VisitCount": 1})
    
    else:
        count = int(today_count.get('Item').get('VisitCount'))
        count = count + 1
        with table.batch_writer() as batch:
            batch.put_item(Item={"Date": today_str, "VisitCount": count})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'count':count})
    }
