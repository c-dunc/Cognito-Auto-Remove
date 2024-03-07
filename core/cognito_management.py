import logging
import datetime
import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

INVAL_STATUS = {"UNCONFIRMED", "RESET_REQUIRED", "FORCE_CHANGE_PASSWORD"}
user_pool_id = os.environ.get("user_pool_id")
aged_user_threshold = os.environ.get("aged_user_threshold")

client = boto3.client("cognito-idp")

class user_management: 

    def list_invalid_users(invalid_status, user_pool_id):
        invalid_users = []
        for status in invalid_status:
            response = client.list_users(UserPoolId=user_pool_id, Filter=f'cognito:user_status="{status}"')
            invalid_users.extend(response.get('Users', []))

        return invalid_users

    @staticmethod
    def remove_user(username: str, user_pool_id: str):
        logger.info(f"Removing user '{username}' from user pool '{user_pool_id}'...")
        try:
            client.admin_delete_user(UserPoolId=user_pool_id, Username=username)
            return {"message": f"Removed user {username} successfully."}
        except ClientError as e:
            return {"error": f"Failed to remove user '{username}': {e}"}
        
    @staticmethod
    def check_user_aged(username: str):
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
