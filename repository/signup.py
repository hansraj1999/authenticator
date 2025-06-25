from repository.schemas import SignUPRequest
from encryption import get_encrypted_password, validate_password
from db import db_manager
from datetime import datetime
from models import User
import uuid
import logging
from communications.email import send_email
from communications.templates import OTP_EMAIL_BODY, OTP_EMAIL_SUBJECT
from repository.otp import OTP
from repository.user import User

logger = logging.getLogger(__name__)


class SignUP:
    def __init__(self, request: SignUPRequest):
        self.request = request

    async def start_signup_process(self):

        hashed_pass = get_encrypted_password(self.request.password)
        print(
            "onfmonfaonfanofa",
            validate_password(self.request.password, hashed_pass),
        )
        self.request.password = hashed_pass
        otp = OTP.genearte_otp()
        logger.info(
            f"otp: {otp} for user: {self.request.email} and password: {self.request.password} "
        )
        user = await User.create_user(
            name=self.request.name,
            email=self.request.email,
            password_hash=self.request.password,
            is_email_verified=False,
            service_name=self.request.service_name,
            last_generated_otp=str(otp),
        )

        await send_email(
            user.email,
            OTP_EMAIL_SUBJECT,
            html_body=(
                OTP_EMAIL_BODY.replace("{", "{{")
                .replace("}", "}}")
                .replace("{{user_name}}", user.name)
                .replace("{{otp_code}}", str(otp))
            ),
        )
        logger.info(f"email sent to: {user.email}")
        return user
