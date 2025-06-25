from fastapi import APIRouter, HTTPException, Query, Depends
from repository.schemas import (
    GetAllUsersRequest,
    GetAllUsersResponse,
)
from typing import Annotated

import logging
import traceback
from pydantic import ValidationError
from repository.user import User

logger = logging.getLogger(__name__)
router = APIRouter(tags=["users"], prefix="/auth/v1")


@router.get("/users", response_model=GetAllUsersResponse)
async def get_all_users(request: Annotated[GetAllUsersRequest, Depends()]):
    try:
        logger.info(request)
        user = User()
        resposne = await user.get_all_users_paginated(request.page, request.page_size)

        return {"users": resposne}

    except ValidationError as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Validation Error",
                "details": e.errors(include_url=False, include_input=False),
            },
        )
    except Exception as e:
        traceback.print_exc()
        logger.exception(str(e))
        raise HTTPException(status_code=400, detail={"message": str(e), "details": []})
