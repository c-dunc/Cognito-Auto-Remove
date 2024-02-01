import logging
import os
import boto3
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TODO 
# Fix issue with check_aged_account returning None
# Implement check_aged_account to check if user is older than 30 days


# Constants
INVAL_STATUS = {"UNCONFIRMED", "RESET_REQUIRED", "FORCE_CHANGE_PASSWORD"}
user_pool_id = os.environ.get("user_pool_id")
aged_user_threshold = os.environ.get("aged_user_threshold") # uses days e.g. 30 = 30 days

# Initialize boto3 client outside of functions
client = boto3.client("cognito-idp")

def remove_user(username: str, user_pool_id=user_pool_id):
    logger.info(f"Removing user '{username}' from user pool '{user_pool_id}'...")
    try:
        client.admin_delete_user(UserPoolId=user_pool_id, Username=username)
        return {"message": f"Removed user {username} successfully."}
        pass
    except ClientError as e:
        return {"error": f"Failed to remove user '{username}': {e}"}

def confirm_unverified_status(username: str):
    logger.info(f"Confirming user '{username}' is in unverified status...")
    try:
        response = client.admin_get_user(UserPoolId=user_pool_id, Username=username)
        user_status = response['UserStatus']
        if user_status in INVAL_STATUS:
            return True
        else:
            return False
        
    except ClientError as e:
        return {"error": f"Error occurred while confirming unverified status for user '{username}': {e}"}
    
def check_aged_account(user_data: list, username: str):
    logger.info(f"Checking age of user '{username}'... must be at least {aged_user_threshold} days")
    try:
        user_info = user_data[0]
        creation_date = user_info.get("UserCreateDate")
        if creation_date:
            return str(creation_date)
        else:
            logger.error(f"Creation date not found for user '{username}'")
            return None
    except Exception as e:
        logger.error(f"Error occurred while checking age for user '{username}': {e}")
        return None


def lambda_handler(event: dict, context):
    username = event.get("username")
    if not username:
        return {"error": "Username not provided"}

    if not user_pool_id:
        return {"error": "User pool ID not found"}

    if not confirm_unverified_status(username):
        return {"error": "User is verfied. Cannot remove user."}
    logger.info(f"User '{username}' is unverified.")

    # creation_date = check_aged_account(user_data, username)
    # if not creation_date:
    #     return {"error": f"Creation date not found for user '{username}'"}

    # remove_user(username)