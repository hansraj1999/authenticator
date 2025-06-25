from repository.session import Session

from models import Session as SessionModel
from db import db_manager
from models import Session as SessionModel


class Logout:
    def __init__(self, token: str):
        self.token = token

    async def start_logout_process(self):

        _session: SessionModel = await Session.get_session_by_token(
            self.token, is_active=True
        )
        if _session is None:
            raise Exception("No Active session found")

        result = await Session.invalidate_session(self.token)
        return False
