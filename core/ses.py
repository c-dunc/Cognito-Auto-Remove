import json
import boto3

from botocore.exceptions import ClientError

with open('config.json') as config_file:
    config = json.load(config_file)

    sender_email = config.get("SENDER_EMAIL")
    aws_region = config.get("AWS_REGION")
    subject = config.get("SUBJECT")
    body_text = config.get("BODY_TEXT")

class ses_handler:
    def send_email(recipient_email):
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