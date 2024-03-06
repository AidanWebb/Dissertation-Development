import os
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_ID"),
                          aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY"),
                          region_name='eu-west-2')
chatRoom_table = dynamodb.Table('chatRoom')


def create_chat_session_id(sender, receiver):
    """Create a consistent chat session ID by alphabetically sorting user IDs."""
    return '_'.join(sorted([sender, receiver]))


def sendMessage(room, sender, message):
    timestamp = datetime.now().isoformat()
    chatRoom_table.put_item(Item={
        'chatSessionId': room,  # Use chatSessionId as the primary key
        'timestamp': timestamp,  # Sort key
        'sender': sender,
        'message': message
    })



def receiveMessages(chatSessionId):
    response = chatRoom_table.query(
        KeyConditionExpression=Key('chatSessionId').eq(chatSessionId),
        ScanIndexForward=True  # Ensure messages are returned in ascending order by timestamp
    )
    return response['Items']
