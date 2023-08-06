import boto3

class SendSms:

    def send_sns(self, number, message, aws_id, aws_secret, aws_region):
        sns = boto3.client('sns',
            aws_access_key_id = aws_id,
            aws_secret_access_key = aws_secret,
            region_name = aws_region,
        )
        
        response = sns.publish(
            PhoneNumber=number,
            Message=message
        )
        
        return response
        
