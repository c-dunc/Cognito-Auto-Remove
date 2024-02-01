import logging
import os
import boto3
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Constants
INVAL_STATUS = {"UNCONFIRMED", "RESET_REQUIRED", "FORCE_CHANGE_PASSWORD"}

# Initialize boto3 client outside of functions
client = boto3.client("cognito-idp")

# User pool ID from environment variable
user_pool_id = os.environ.get("user_pool_id")

def remove_user(username: str, user_pool_id: str):
    """
    Remove a user from the Cognito user pool.
    
    Args:
        username (str): The username of the user to be removed.
        user_pool_id (str): The ID of the Cognito user pool.
    
    Returns:
        dict: A dictionary containing a success message or an error message.
    """
    try:
        client.admin_delete_user(UserPoolId=user_pool_id, Username=username)
        return {"message": f"Removed user {username} successfully."}
    except ClientError as e:
        logger.error(f"Failed to remove user {username}: {e}")
        return {"error": f"Failed to remove user {username}: {e}"}

def confirm_unverified_status(user_data: str, user_pool_id: str):
    """
    Check if a user has an invalid status in the Cognito user pool.
    
    Args:
        username (str): The username of the user to be checked.
        user_pool_id (str): The ID of the Cognito user pool.
    
    Returns:
        bool: True if the user has an invalid status, False otherwise.
        dict: A dictionary containing an error message if the user status is not found.
    """
    try:
        response = client.list_users(UserPoolId=user_pool_id, Filter=f'username="{username}"')
        users = user_data.get("Users", [])
        user_status = next((user_info["UserStatus"] for user_info in users if "UserStatus" in user_info), None)

        if user_status in INVAL_STATUS:
            return True
        else:
            return False
    except ClientError as e:
        logger.error(f"Failed to retrieve user status for {username}: {e}")
        return {"error": f"Failed to retrieve user status for {username}: {e}"}

def check_aged_account(username: str, user_pool_id: str):
    pass

def lambda_handler(event: dict, context):
    """
    Lambda handler function.
    
    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The runtime information passed to the Lambda function.
    
    Returns:
        dict: A dictionary containing a success message or an error message.
    """
    username = event.get("username")
    if not username:
        logger.error("Username not provided")
        return {"error": "Username not provided"}
    else:
        user_data = client.list_users(UserPoolId=user_pool_id, Filter=f'username="{username}"')

    if not user_pool_id:
        logger.error("User pool ID not found")
        return {"error": f"User pool ID not found: {user_pool_id}"}

    if confirm_unverified_status(user_data, user_pool_id):
        logger.info(f"User {username} has invalid status. Checking age...")
        if check_aged_account == True:
            logger.info(f"User {username} is aged. Removing...")
        else:
            return {"error": f"User is invalid but not aged: {account_creation_date}/{aged_removal_interval}d"}
        
        return remove_user(username, user_pool_id)
    else:
        return {"error": f"User is valid and cannot be removed: {username}"}
