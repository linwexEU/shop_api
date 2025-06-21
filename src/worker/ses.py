from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email.mime.text import MIMEText 
from email import encoders

import boto3 

from src.config import settings


# Configure AWS credentials
aws_credentials = {
    "aws_access_key_id": settings.AWS_ACCESS_KEY, 
    "aws_secret_access_key": settings.AWS_SECRET_KEY, 
    "region_name": settings.AWS_REGION
} 


class SESClient:
    def __init__(self):
        self.client = boto3.client("ses", **aws_credentials)

    def send_email_with_attachment(self, to: str, from_: str, subject: str, body: str, attachment: bytes, filename: str):
        # Mime structure 
        message = MIMEMultipart() 
        message["Subject"] = subject
        message["From"] = from_ 
        message["To"] = to 

        # Add body 
        message.attach(MIMEText(body, "plain")) 

        # Add file 
        part = MIMEBase("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        part.set_payload(attachment) 
        encoders.encode_base64(part) 
        part.add_header("Content-Disposition", f"attachment; filename={filename}")

        # Attach file 
        message.attach(part)
        
        # Send email
        response = self.client.send_raw_email(
            Source=from_, 
            Destinations=[to], 
            RawMessage={"Data": message.as_string()}
        )
        
        self.client.close() 
        return response
