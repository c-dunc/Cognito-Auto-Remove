import logging
import datetime
import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TODO 
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
    
def check_aged_account(username: str):
    logger.info(f"Checking age of user '{username}'... must be at least {aged_user_threshold} days")
    try:
        response = client.admin_get_user(UserPoolId=user_pool_id, Username=username)
        creation_date_time = response['UserCreateDate'] # "2024-02-01 23:13:26.127000+00:00"
        creation_date = str(creation_date_time)[:10] # "2024-02-01" YYYY-MM-DD
        current_date = datetime.today().strftime('%Y-%m-%d')
        logger.info(f"current_date: {current_date}, creation_date: {creation_date}")
    
    except ClientError as e:
        logger.error(f"Error occurred while confirming unverified status for user '{username}': {e}")
        return {"error": f"Error occurred while confirming unverified status for user '{username}': {e}"}

def lambda_handler(event: dict, context):
    username = event.get("username")
    if not username:
        return {"error": "Username not provided"}

    if not user_pool_id:
        return {"error": "User pool ID not found"}

    if not confirm_unverified_status(username):
        return {"error": "User is verfied. Cannot remove user."}

    if check_aged_account(username):
        logger.info(f"Removing user '{username}' from user pool '{user_pool_id}'...")
        # remove_user(username)
    else:
        return {"error": f"User is less than {aged_user_threshold}d old."}