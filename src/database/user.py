import os
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone, timedelta
from processing.dynamodb import encode, decode
from classes.errors import OKException
from classes.status import Status

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_ID"),
                          aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY"),
                          region_name='eu-west-2')

user_table = dynamodb.Table('user')


def add_user(username, password):
    user_info = {
        'username': username,
        'password': password,
        'friends' : []
    }
    encode(user_info)
    user_table.put_item(Item=user_info)
    return user_info


def get_user(username):
    """
    Returns user object given a user ID/email.
    :param username: User email address.
    :return: user object.
    """
    try:
        response = user_table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        user = response['Items'][0]
        decode(user)
        return user
    except:
        raise OKException(Status.USER_NOT_FOUND)


def add_friend(username, friend):
    try:
        response = user_table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        user = response['Items'][0]
        decode(user)
        user['friends'].append(friend)
        encode(user)
        user_table.put_item(Item=user)
    except:
        raise OKException(Status.USER_NOT_FOUND)


def delete_friend(username, friend):
    try:
        response = user_table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        user = response['Items'][0]
        decode(user)

        if friend in user['friends']:
            user['friends'].remove(friend)
            encode(user)
            user_table.put_item(Item=user)
        else:
            raise OKException(Status.USER_NOT_FOUND)
    except Exception as e:
        print(f"Error deleting friend: {e}")
        raise OKException(Status.USER_NOT_FOUND)

def get_user_by_username(username):
    try:
        response = user_table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        user = response['Items'][0]
        decode(user)
        return user
    except:
        raise OKException(Status.USER_NOT_FOUND)
