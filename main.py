import logging
import boto3
import json
import os
# logging Init
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

INVAL_STATUS = ["UNCONFIRMED"]
INVAL_USERS = {}

sending_email = os.environ['SENDING_EMAIL']
receiving_email = os.environ['RECEIVING_EMAIL']
aws_account_name = os.environ['AWS_ACCOUNT_NAME']
aws_account_id = os.environ['AWS_ACCOUNT_ID']
aws_region = os.environ['AWS_REGION']
user_pool_id = os.environ['user_pool_id']

def lambda_handler(event: str, context: str):
    """
    lambda_handler automatically used when Lambda is triggered

    :param event: event data sent from Eventbridge
    """ 
    logger.info(f"new event: \n{event}")
    client = boto3.client("cognito-idp")
    for status in INVAL_STATUS:
        INVAL_USERS.append(client.list_users(UserPoolId=user_pool_id,Filter=f'cognito:user_status="{status}"'))
