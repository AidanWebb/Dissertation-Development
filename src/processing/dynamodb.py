import decimal
import os
import boto3

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_ID"),
                          aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY"),
                          region_name='eu-west-1')


def decode(obj):
    """
    Converts python dictionary containing Decimal types to dictionary of floats.
    :param obj: python dictionary containing Decimal.
    :return: python dictionary containing floats.
    """
    if isinstance(obj, decimal.Decimal):
        if obj == int(obj):
            return int(obj)
        return float(obj)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = decode(value)
    elif isinstance(obj, list):
        for value in obj:
            decode(value)
    return obj


def encode(obj):
    """
    Converts python dictionary containing float types to dictionary of Decimal.
    :param obj: python dictionary containing floats.
    :return: python dictionary containing Decimal.
    """
    if isinstance(obj, float):
        if obj == int(obj):
            return int(obj)
        return decimal.Decimal(str(obj))
    elif isinstance(obj, dict):
        for key, value in obj.copy().items():
            if value in ['']:
                del obj[key]
            else:
                obj[key] = encode(value)
    elif isinstance(obj, list):
        for value in obj.copy():
            if value in ['']:
                obj.remove(value)
            else:
                encode(value)
    return obj
