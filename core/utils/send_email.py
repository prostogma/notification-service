import aiosmtplib
from email.message import EmailMessage


async def send_email(recipient: str, subject: str, body: str):
    email = "no_reply@example.com"
    
    message = EmailMessage()
    message["From"] = email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    
    await aiosmtplib.send(
        message,
        sender=email,
        recipients=[recipient],
        hostname="maildev",
        port=1025
    )