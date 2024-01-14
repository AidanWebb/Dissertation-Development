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


def add_user(email, password):
    user_info = {
        'email': email,
        'password': password
    }
    encode(user_info)
    user_table.put_item(Item=user_info)
    return user_info


def get_user(email):
    """
    Returns user object given a user ID/email.
    :param email: User email address.
    :return: user object.
    """
    try:
        response = user_table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        user = response['Items'][0]
        decode(user)
        return user
    except:
        raise OKException(Status.USER_NOT_FOUND)