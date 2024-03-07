import logging
import boto3
import json

from core.cognito_management import user_management

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

client = boto3.client("cognito-idp")

with open('config.json') as config_file:
    config = json.load(config_file)

user_pool_id = config.get('user_pool_id')
invalid_status = config.get('invalid_status')

def lambda_handler(event, context):
    """
    Lambda handler function automatically used when Lambda is triggered.
    :param event:
    """

    if not user_pool_id:
        logger.error("Set userpool ID in config.json")
        return
    logger.info(f"New event: \n{event}")

    try: 
        invalid_users = user_management.list_invalid_users()
        for user in invalid_users:
            aged = user_management.check_user_aged(invalid_users)
            if aged:
                try:
                    user_management.remove_user(user['Username'])
                except:
                    logger.error(f"Unable to remove user '{user['Username']}'")
            else:
                logger.error(f"User '{user}' is not aged enough to be removed.")
                return
    except: 
        pass