import logging
import boto3
import os

# Logging Init
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

user_pool_id = os.environ.get('user_pool_id')

def lambda_handler(event, context):
    """
    Lambda handler function automatically used when Lambda is triggered.
    """ 

    logger.info(f"New event: \n{event}")
    
    username = event['username']

    if not user_pool_id:
        logger.error("User pool ID not found")
        return {"error": "User pool ID not found"}

    client = boto3.client("cognito-idp")
    logger.info(f"Attempting to delete {username}")
    try: 
        response = client.admin_delete_user(UserPoold=user_pool_id,Username=username)
        output = f"Removed {username}"
        return output
    except Exception as e:
        output = f"Error in removing {username}\n{e}"
        return output