import random
from datetime import datetime
from db import db_manager
from repository.user import User


class OTP:

    @staticmethod
    def genearte_otp():
        return random.randint(1000, 9999)

    async def verify_otp(self, input_otp, user_id, service_name="shorturl"):
        async for session in db_manager.get_session():
            user = await User.get_user_by_id(user_id, service_name)
            if not user:
                raise Exception("User not found")
            if user.is_email_verified:
                raise Exception("User is already verified")
            last_generated_otp = user.last_generated_otp
            if not last_generated_otp or self.is_otp_expired(
                user.last_generated_otp_sent_at
            ):
                raise Exception("OTP is expired Kindly regenerate")
            if input_otp == last_generated_otp:
                await User.update_is_email_verified(user_id, service_name)
            else:
                raise Exception("Invalid OTP")
            return user

    def is_otp_expired(self, last_generated_otp_sent_at):
        return (datetime.utcnow() - last_generated_otp_sent_at).total_seconds() > 3600
