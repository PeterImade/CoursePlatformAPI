from fastapi_mail import FastMail,  MessageSchema, MessageType, ConnectionConfig
from ..core.config import Config
from pathlib import Path

# get the parent directory
BASE_DIR = Path(__file__).resolve().parent


# create config for sending emails
mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates")
)

# create the object to send emails with the config
mail = FastMail(config=mail_config)


def create_message(recipients: list[str], subject: str, body: str) -> MessageSchema:
    message = MessageSchema(recipients=recipients, subject=subject, body=body, subtype=MessageType.html)
    return message


async def send_verification_otp_to_email(receiver_email, receiver_name, otp) -> None:
    subject = "Subject: Your One-Time Password (OTP) for Coursify"

    body = f"""
    <h3>Hello, {receiver_name}. We hope this message finds you well. As part of our ongoing commitment to ensuring the security of your account, we have generated a one-time password (OTP) for you to use with your Coursify account.

    Your OTP: {otp}

    Please use this OTP within the next 5 minutes to complete your authentication process. For security reasons, please do not share this OTP with anyone.

    If you did not request this OTP or have any concerns about the security of your account, please contact our support team immediately at  or visit our website for assistance.

    Thank you for choosing Coursify! </h3>"""


    message = create_message(recipients=[receiver_email], subject=subject, body=body)
    mail.send_message(message)

async def send_reset_password_otp_to_email(receiver_email, receiver_name, otp) -> None:
    subject = "Subject: Password Reset Request - Your OTP Code"

    body = f"""
    <h3>Dear, {receiver_name}. We received a request to reset your password. Please find your one-time password (OTP) below:

    Your OTP Code: {otp}
    This OTP is valid for 5 minutes. Please enter it on the password reset page to proceed.

    If you did not request a password reset, you can safely ignore this email. Your password will remain unchanged.

    If you have any questions or need further assistance, feel free to reach out to our support team.   
    Thank you,
    Coursify! </h3>"""


    message = create_message(recipients=[receiver_email], subject=subject, body=body)
    mail.send_message(message)
    

