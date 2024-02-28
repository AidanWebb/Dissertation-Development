import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timezone, timedelta
from processing.dynamodb import encode, decode
from classes.errors import OKException
from classes.status import Status

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_ID"),
                          aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY"),
                          region_name='eu-west-2')

chatRoom_table = dynamodb.Table('chatRoom')

def sendMessage(sender, receiver, message):
    timestamp=datetime.now().isoformat()
    chatRoom_table.put_item(Item={
        'sender': sender,
        'receiver': receiver,
        'message': message,
        'timestamp': timestamp
    })

def recieveMessages(sender, receiver):
    response = chatRoom_table.query(
        KeyConditionExpression=Key('sender').eq(sender) & Key('receiver').eq(receiver)
    )
    return response['Items']