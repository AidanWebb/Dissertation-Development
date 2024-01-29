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

chatRooms_table = dynamodb.Table('chatRooms')

def create_chatRoom(chatRoom_id, created_at, participants):
    """
    Creates a new chat room in the DynamoDB table.
    """
    chatRooms_table.put_item(
        Item={
        'chatRoom_id' : chatRoom_id,
        'created_at' : created_at,
        'participants' : participants
        }
    )
def addUser_to_chatRoom(chatRoom_id, user):
    """
    Adds a user to the specified chat room in the DynamoDB table.
    """
    chatRooms_table.update_item(
        Key={'chatRoom_id':chatRoom_id},
        UpdateExpressions = 'SET participants = list_append(participants, :user)',
        ExpressionsAttributeValues = {'user':[user]}
    )

def get_chatRoom(chatRoom_id):
    """
     Retrieves a chat room from the DynamoDB table by chat room ID.
    """
    response = chatRooms_table.get_item(
        Key={'chatRoom_id': chatRoom_id}
    )
    return response.get('Item')

def get_chatRoom_forUsers(user):
    """
    Retrieves chat rooms associated with the specified user from the DynamoDB table.
    """
    response = chatRooms_table.scan(
        FilterExpressions = Attr('participants').contains(user)
    )
    return response.get('Items',[])