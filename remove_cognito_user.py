import logging
import boto3
import os

# GLOBAL VARIABLES
#################################################### 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

INVAL_STATUS = {"UNCONFIRMED", "RESET_REQUIRED", "FORCE_CHANGE_PASSWORD"}

user_pool_id = os.environ.get("user_pool_id") # cognito user pool id to access
aged_removal_interval = os.environ.get("aged_removal_interval") #  how many days old the account is before removal

global client
client = boto3.client("cognito-idp")

#################################################### 


def remove_user(username: str, user_pool_id=user_pool_id):
    try:
        client.admin_delete_user(UserPoolId=user_pool_id, Username=username)
        return {"message": f"Removed user {username} successfully."}
    except:
        return {"error": f"Unable to remove user {username}."}


def aged_account(username: str):
    logger.info(f"Checking if user {username} created in last 30 days.")

def confirm_unverified_status(username: str):

    response = client.list_users(UserPoolId=user_pool_id, Filter=f'username="{username}"')
    users = response.get("Users", [])
    user_status = next((user_info["UserStatus"] for user_info in users if "UserStatus" in user_info), None)

    if user_status:
        if user_status in INVAL_STATUS: 
            return True
        else:
            return False
    else: 
        return {"message": "User status not found for user: {username}."}

def lambda_handler(event: str, context):

    username = event.get("username")

    if not username:
        logger.error("Username not provided")
        return {"error": "Username not provided"}

    if not user_pool_id:
        logger.error("User pool ID not found")
        return {"error": "User pool ID not found"}


    if confirm_unverified_status(username) == True:
        logger.info(f"User {username} has invalid status. Removing user.")