import boto3
    

class ses_handler:

    def generate_email_body():  # todo
        body_text = "Working in progress!"
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