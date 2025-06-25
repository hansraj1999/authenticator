from fastapi import APIRouter, HTTPException
from repository.schemas import (
    GetAllSessionsRequest,
    GetAllSessionsResponse,
)
from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

import logging
import traceback
from pydantic import ValidationError
from repository.session import Session

logger = logging.getLogger(__name__)
router = APIRouter(tags=["session"], prefix="/auth/v1")


@router.get("/session", response_model=GetAllSessionsResponse)
async def get_paginated_sessions(request: Annotated[GetAllSessionsRequest, Depends()]):
    try:
        logger.info(request)
        session = Session()
        resposne = await session.get_sessions_paginated(
            request.page, request.page_size, request.is_active
        )
        print(resposne, "resposne")

        return {"sessions": resposne}

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
