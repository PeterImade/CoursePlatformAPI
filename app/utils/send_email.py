import smtplib
from ..core.config import Config 
from ..core.logger import get_logger
logger = get_logger(__name__)



async def send_verification_otp_to_email(receiver_email, receiver_name, otp) -> None:
    subject = "Subject: Your One-Time Password (OTP) for Coursify"

    body = f"""<h3> Hello, {receiver_name}. We hope this message finds you well. As part of our ongoing commitment to ensuring the security of your account, we have generated a one-time password (OTP) for you to use with your Coursify account.

    Your OTP: {otp}

    Please use this OTP within the next 5 minutes to complete your authentication process. For security reasons, please do not share this OTP with anyone.

    If you did not request this OTP or have any concerns about the security of your account, please contact our support team immediately at  or visit our website for assistance.

    Thank you for choosing Coursify! </h3>"""

    message = f"Subject: {subject}\n\n{body}" 

    with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
        server.starttls()
        logger.info(f"login to mailtrap service.........") 
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        logger.info(f"logged in successfully.........") 
        logger.info("sending email..........") 
        server.sendmail(Config.MAIL_FROM, receiver_email, message)
        logger.info(f"Email sent successfully..........")


async def send_reset_password_otp_to_email(receiver_email, receiver_name, otp) -> None:
    subject = "Subject: Password Reset Request - Your OTP Code"

    body = f"""<h3>Dear, {receiver_name}. We received a request to reset your password. Please find your one-time password (OTP) below:

    Your OTP Code: {otp}
    This OTP is valid for 5 minutes. Please enter it on the password reset page to proceed.

    If you did not request a password reset, you can safely ignore this email. Your password will remain unchanged.

    If you have any questions or need further assistance, feel free to reach out to our support team.   
    Thank you,
    Coursify! </h3>"""
    
    
    message = f"Subject: {subject}\n\n{body}" 
    with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
        server.starttls()
        logger.info(f"login to mailtrap service.........") 
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        logger.info(f"logged in successfully.........") 
        logger.info("sending email..........") 
        server.sendmail(Config.MAIL_FROM, receiver_email, message)
        logger.info(f"Email sent successfully..........")
    

