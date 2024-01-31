import logging
import boto3
import os

# Logging Init
logger = logging.getLogger()
logger.setLevel(logging.INFO)

INVAL_STATUS = {"UNCONFIRMED", "RESET_REQUIRED", "FORCE_CHANGE_PASSWORD"}

user_pool_id = os.environ.get('user_pool_id')

def lambda_handler(event, context):
    """
    Lambda handler function automatically used when Lambda is triggered.
    :param event: username k, v passed through to determine user to remove
    """ 

    username = event.get('username')

    if not username:
        logger.error("Username not provided")
        return {"error": "Username not provided"}

    if not user_pool_id:
        logger.error("User pool ID not found")
        return {"error": "User pool ID not found"}

    client = boto3.client("cognito-idp")
    logger.info(f"Attempting to delete user: {username}")
    
    try:
        response = client.list_users(UserPoolId=user_pool_id, Filter=f'username="{username}"')
        users = response.get('Users', [])
        user_status = next((user_info['UserStatus'] for user_info in users if 'UserStatus' in user_info), None)

        if user_status:
            if user_status in INVAL_STATUS: 
                logger.info("User status is invalid. Removing...")
                client.admin_delete_user(UserPoolId=user_pool_id, Username=username)
                return {"message": "User removed successfully."}
            else:
                output = f'User status is {user_status}, WILL NOT REMOVE.'
                logger.info(output)
                return {"message": output}
        else:
            output = f'User status not found for user: {username}.'
            logger.info(output)
            return {"message": output}

    except Exception as error:
        logger.error(f"Error in removing user: {username}, Error: {error}")
        return {"error": f"Error in removing user: {username}, Error: {error}"}
