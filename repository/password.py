from repository.schemas import LoginRequest, LoginResponse
from repository.user import User
from repository.session import Session
from encryption import validate_password
from datetime import datetime, timedelta
from encryption import get_encrypted_password, validate_password
from repository.otp import OTP
from communications.email import send_email
from communications.templates import OTP_EMAIL_BODY, OTP_EMAIL_SUBJECT
import logging

logger = logging.getLogger(__name__)


class Password:
    def __init__(self, email: str, service_name: str = "shorturl"):
        self.email = email
        self.service_name = service_name

    async def create_session(self, user_id):
        if self.request.remember_me:
            expires_at = None
        else:
            expires_at = datetime.utcnow() + timedelta(days=30)
        return await Session.create_session(user_id, expires_at)

    async def start_reset_password_process(self, new_password: str):

        user = await User.get_user_by_email(self.email)
        print("self.email", self.email)
        if user is None:
            raise Exception(f"User with email: {self.email} not found")
        otp = OTP.genearte_otp()
        res = await User.update_password(
            user.id,
            get_encrypted_password(new_password),
            otp,
            self.service_name,
        )
        # TODO: remove all active sessions await Logout(authorization).start_logout_process()
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
        return res
