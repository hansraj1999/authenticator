from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging
import os

smtp_client = None  # Global SMTP reference
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global smtp_client
    smtp_client = smtplib.SMTP_SSL("smtp.hostinger.com", 465)
    user_name = os.getenv("SMTP_USER_NAME")
    password = os.getenv("SMTP_PASSWORD")
    logger.info(f"SMTP_USER_NAME: {user_name}")
    logger.info(f"SMTP_PASSWORD: {password}")
    smtp_client.login(user_name, password)
    print("✅ SMTP connection established.")

    yield  # Everything after this line runs at shutdown

    if smtp_client:
        smtp_client.quit()
        print("🔒 SMTP connection closed.")


def get_smtp():
    if not smtp_client:
        raise RuntimeError("SMTP client not available")
    return smtp_client


async def send_email(to: str, subject: str, text_body: str = "", html_body: str = ""):
    try:
        smtp = get_smtp()
        sender_email = os.getenv("SMTP_USER_NAME")

        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to
        message["Subject"] = subject
        if text_body:
            message.attach(MIMEText(text_body, "plain"))
        if html_body:
            message.attach(MIMEText(html_body, "html"))

        # Send using persistent SMTP
        smtp.sendmail(sender_email, to, message.as_string())
    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.exception(str(e))
    return True
