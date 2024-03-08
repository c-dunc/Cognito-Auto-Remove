import datetime
import boto3


client = boto3.client("cognito-idp")

class UserManagement:
    @staticmethod
    def list_invalid_users(invalid_status, user_pool_id):
        invalid_usernames = []
        response = client.list_users(UserPoolId=user_pool_id, Filter=f'cognito:user_status="{invalid_status}"')
        for user in response.get('Users', []):
            invalid_usernames.append(user['Username'])
        
        return invalid_usernames

        

    @staticmethod
    def remove_user(username: str, user_pool_id: str):
        print(f"Removing user '{username}' from user pool '{user_pool_id}'...")
        try:
            client.admin_delete_user(UserPoolId=user_pool_id, 
            Username=username
)
            print("Removed user {username} successfully.")
        except Exception as e:
            print("Failed to remove {username}.")

    @staticmethod
    def get_user_age(user_pool_id, username):
            response = client.admin_get_user(UserPoolId=user_pool_id, 
            Username=username
)
            creation_date_time = response['UserCreateDate']
            creation_date = creation_date_time.date()        
            return creation_date
    
    @staticmethod
    def check_user_aged(username: str, user_pool_id: str, aged_user_threshold: int):
        print(f"Checking age of user '{username}'... must be at least {aged_user_threshold} days")
        try:
            creation_date = UserManagement.get_user_age(user_pool_id, 
            username
)
            current_date = datetime.date.today()
            age = (current_date - creation_date).days
            print(f"age: {age}, current_date: {current_date}, creation_date: {creation_date}")
            if int(age) >= int(aged_user_threshold):
                print(f"Removing {username}...")
                UserManagement.remove_user(username)

        except Exception as e:
            print(f"Error occurred while confirming unverified status for user '{username}': {e}")