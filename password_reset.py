import os
import boto3

def lambda_handler(event, context):
    """
    Lambda handler function automatically used when Lambda is triggered.
    :param event: username and new password passed through to be changed. 
                  used against test users for verification
    """ 
    
    username = event['username']
    new_password = event['password']
    user_pool_id = os.environ.get('user_pool_id')

    cognito_client = boto3.client('cognito-idp')
    
    try:
        
        cognito_client.admin_set_user_password(UserPoolId=user_pool_id,Username=username,Password=new_password,Permanent=True)
        return {
            'statusCode': 200,
            'body': 'Password reset successfully.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error resetting password: ' + str(e)
        }
