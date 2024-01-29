import logging
import boto3
import os

# Logging Init
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

INVAL_STATUS = ["UNCONFIRMED", "RESET_REQUIRED", "FORCE_CHANGE_PASSWORD"]
invalid_users = []

def lambda_handler(event, context):
    """
    Lambda handler function automatically used when Lambda is triggered.
    """
    logger.info(f"New event: \n{event}")
    user_pool_id = os.environ.get('user_pool_id')
    if not user_pool_id:
        logger.error("User pool ID not found in environment variables.")
        return {"error": "User pool ID not found"}

    client = boto3.client("cognito-idp")
    for status in INVAL_STATUS:
        response = client.list_users(UserPoolId=user_pool_id, Filter=f'cognito:user_status="{status}"')
        invalid_users.extend(response.get('Users', []))
      
    return invalid_users
