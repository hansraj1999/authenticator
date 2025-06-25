import random
from datetime import datetime
from db import db_manager
from models import User


class OTP:

    @staticmethod
    def genearte_otp():
        return random.randint(1000, 9999)

    async def verify_otp(self, input_otp, user_id):
        async for session in db_manager.get_session():
            user = await session.get(User, user_id)
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
                user.is_email_verified = True
                await session.commit()
                await session.refresh(user)
                return user
            else:
                raise Exception("Invalid OTP")

    def is_otp_expired(self, last_generated_otp_sent_at):
        return (datetime.utcnow() - last_generated_otp_sent_at).total_seconds() > 3600
