import boto3
import json

from core.cognito_handler import UserManagement
from core.ses import ses_handler

client = boto3.client("cognito-idp")

with open('config.json') as config_file:
    config = json.load(config_file)

user_pool_id = config.get('user_pool_id')
invalid_status = config.get('invalid_status')
aged_threshold = config.get('aged_threshold')
sender_email = config.get("sender_email")
aws_region = config.get("aws_region")
subject = config.get("subject")
recipient = config.get("recipient")

def lambda_handler(event, context):
    """
    Lambda handler function automatically used when Lambda is triggered.
    :param event:
    """

    print(f"New event: \n{event}")
    
    try: 
        invalid_users = UserManagement.list_invalid_users(invalid_status, user_pool_id)
        UserManagement.list_invalid_users(invalid_status, user_pool_id)
    except Exception as e:
        return f"Error: {e}"
    
    try:
        for user in invalid_users:
            UserManagement.check_user_aged(user, user_pool_id, aged_threshold)
    except Exception as e:
        return f"Error: {e}"
    
    try: 
        body_text = ses_handler.generate_email_body(invalid_users)
        ses_handler.send_email(recipient, sender_email, aws_region, subject, body_text)
    except: 
        return f"Error: {e}"