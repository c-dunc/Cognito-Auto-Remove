import boto3
    

class ses_handler:

    def generate_email_body(user_list):
        body_text = f'''
        <html>
        <head></head>
        <body>
            <h1>Hello,</h1>
            <p>The following users have been removed from the Cognito User Pool:</p>
            <ul>
        '''
        for user in user_list:
            body_text += f'<li>{user}</li>\n'
            
        body_text += '''
            </ul>
            <p>This action was automated by </p><a href="https://github.com/c-dunc/Cognito-Auto-Remove">cognito unverified removal</a>
        </body>
        </html>
        '''
        return body_text

    def send_email(recipient_email, sender_email, aws_region, subject, body_text):
        print(f"New email ready: \n{recipient_email}")
        client = boto3.client('ses', region_name=aws_region)

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                            recipient_email,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': body_text,
                            },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': subject,
                    },
                },
                Source=sender_email,
)

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:", response['MessageId'])