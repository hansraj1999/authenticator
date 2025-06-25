from repository.schemas import LoginRequest, LoginResponse
from repository.user import User
from repository.session import Session
from encryption import validate_password
from datetime import datetime, timedelta


class Login:
    def __init__(self, request: LoginRequest) -> LoginResponse:
        self.request = request

    async def create_session(self, user_id):
        if self.request.remember_me:
            expires_at = None
        else:
            expires_at = datetime.utcnow() + timedelta(days=30)
        return await Session.create_session(user_id, expires_at)

    async def start_login_process(self):

        user = await User.get_user_by_email(self.request.email)
        if user is None:
            raise Exception("User not found")

        if validate_password(self.request.password, user.password_hash):
            raise Exception("Invalid password")
        _session = await Session.get_session_by_user_id(user.id)
        if not _session:
            _session = await Session.upsert_session(user.id)
        elif Session.check_if_session_is_expired(_session.expires_at):
            _session = await Session.upsert_session(user.id)

        response = LoginResponse(
            id=user.id,
            name=user.name,
            service_name=user.service_name,
            token=_session.session_id,
            message="User logged in successfully",
            expires_at=_session.expires_at,
        )

        return response
