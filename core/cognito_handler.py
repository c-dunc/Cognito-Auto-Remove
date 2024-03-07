import datetime
import boto3
from botocore.exceptions import ClientError

client = boto3.client("cognito-idp")

class UserManagement:
    @staticmethod
    def list_invalid_users(invalid_status, user_pool_id, session):
        invalid_users = []
        client = session.client("cognito-idp")
        paginator = client.get_paginator('list_users')
        for status in invalid_status:
            response_iterator = paginator.paginate(UserPoolId=user_pool_id, Filter=f'cognito:user_status="{status}"')
            for response in response_iterator:
                invalid_users.extend(response.get('Users', []))

        return invalid_users

    @staticmethod
    def remove_user(username: str, user_pool_id: str, session):
        print(f"Removing user '{username}' from user pool '{user_pool_id}'...")
        try:
            with session.client("cognito-idp") as client:
                client.admin_delete_user(UserPoolId=user_pool_id, Username=username)
            return {"message": f"Removed user {username} successfully."}
        except ClientError as e:
            return {"error": f"Failed to remove user '{username}': {e}"}

    @staticmethod
    def get_user_age():
            response = client.admin_get_user(UserPoolId=user_pool_id, Username=username)
            creation_date_time = response['UserCreateDate']
            creation_date = creation_date_time.date()        
            return creation_date
    
    @staticmethod
    def check_user_aged(username: str, user_pool_id: str, aged_user_threshold: int, session):
        print(f"Checking age of user '{username}'... must be at least {aged_user_threshold} days")
        try:
            creation_date = UserManagement.get_user_age(username, user_pool_id, session)
            current_date = datetime.date.today()
            age = (current_date - creation_date).days
            print(f"current_date: {current_date}, creation_date: {creation_date}, age: {age}")

        except ClientError as e:
            print(f"Error occurred while confirming unverified status for user '{username}': {e}")
            return {"error": f"Error occurred while confirming unverified status for user '{username}': {e}"}
