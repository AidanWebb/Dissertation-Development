import os
import boto3
import base64
import logging
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone, timedelta
from processing.dynamodb import encode, decode
from classes.errors import OKException
from classes.status import Status
from processing.crypto import rsa_keypair
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_ID"),
                          aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY"),
                          region_name='eu-west-2')

user_table = dynamodb.Table('user')


def add_user(username, password):

    private_key_serialized, public_key_serialized = rsa_keypair()

    user_info = {
        'username': username,
        'password': password,
        'public_key': public_key_serialized.decode('utf-8'),
        'private_key': private_key_serialized.decode('utf-8'),
        'friends': []
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


def add_friend(username, friend_username):
    user = get_user(username)
    friend = get_user(friend_username)


    if friend_username not in user['friends']:
        user['friends'].append(friend_username)
        encode(user)
        user_table.put_item(Item=user)

    if username not in friend['friends']:
        # Add user to friend's friend list
        friend['friends'].append(username)
        encode(friend)
        user_table.put_item(Item=friend)


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



def fetch_public_key(username):
    try:
        logging.info(f"Attempting to fetch public key for username: {username}")
        response = user_table.query(
            KeyConditionExpression=Key('username').eq(username),
            ProjectionExpression='public_key'
        )
        if response['Items']:
            public_key = response['Items'][0]['public_key']
            logging.info(f"Successfully fetched public key for {username}")
            return public_key
        else:
            logging.warning(f"No public key found for {username}")
            return None
    except Exception as e:
        logging.error(f"Error fetching public key for {username}: {e}", exc_info=True)
        return None

def fetch_private_key(username):
    try:
        logging.info(f"Attempting to fetch private key for username: {username}")
        response = user_table.query(
            KeyConditionExpression=Key('username').eq(username),
            ProjectionExpression='private_key'
        )
        if response['Items']:
            private_key = response['Items'][0]['private_key']
            logging.info(f"Successfully fetched private key for {username}")
            return private_key
        else:
            logging.warning(f"No private key found for {username}")
            return None
    except Exception as e:
        logging.error(f"Error fetching private key for {username}: {e}", exc_info=True)
        return None

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


def get_public_key(username):
    try:
        user = fetch_public_key(username)
        print(f"User object retrieved for '{username}': {user}")
        return user.get('public_key')
    except Exception as e:
        print(f"Error retrieving public key for {username}: {e}")
        return None
