from fastapi import APIRouter, HTTPException
from repository.schemas import (
    SignUPRequest,
    SignUPResponse,
    VerifyOTPRequest,
    VerifyOTPPResponse,
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)
from repository.password import Password
import logging
from repository.signup import SignUP
import traceback
from pydantic import ValidationError
from repository.otp import OTP
from repository.login import Login
from repository.session import Session
from fastapi import Header
from repository.logout import Logout

logger = logging.getLogger(__name__)
router = APIRouter(tags=["auth"], prefix="/auth/v1")


@router.post("/signup", response_model=SignUPResponse)
async def signup(request: SignUPRequest):
    try:
        logger.info(request)
        signup = SignUP(request)
        resposne = await signup.start_signup_process()
        resposne = {
            "id": str(resposne.id),
            "name": resposne.name,
            "email": resposne.email,
            "service_name": resposne.service_name,
            "last_generated_otp_sent_at": str(resposne.last_generated_otp_sent_at),
            "message": "User created successfully Kindly check your email to verify your account",
        }
        return resposne

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


@router.post("/verify/otp", response_model=VerifyOTPPResponse)
async def verify_otp(request: VerifyOTPRequest):
    try:
        logger.info(request)
        otp = OTP()
        resposne = await otp.verify_otp(
            request.otp, request.user_id, request.service_name
        )
        resposne = {
            "id": str(resposne.id),
            "name": resposne.name,
            "email": resposne.email,
            "service_name": resposne.service_name,
            "message": "OTP verified successfully",
        }
        return resposne

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


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        logger.info(request)
        login = Login(request)
        resposne: LoginResponse = await login.start_login_process()
        resposne = {
            "id": resposne.id,
            "name": resposne.name,
            "service_name": resposne.service_name,
            "token": resposne.token,
            "message": "User logged in successfully",
            "expires_at": resposne.expires_at,
        }
        return resposne

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


@router.post("/logout", response_model=LogoutResponse)
async def logout(authorization: str = Header(...)):
    try:
        # decode token, mark as inactive in DB
        if not authorization:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        logger.info(authorization)
        await Logout(authorization).start_logout_process()
    except Exception as e:
        traceback.print_exc()
        logger.exception(str(e))
        raise HTTPException(status_code=400, detail={"message": str(e), "details": []})
    return LogoutResponse(message="Successfully logged out")


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(request: ResetPasswordRequest):
    # logic to verify token, reset password
    try:
        await Password(
            request.email, request.service_name
        ).start_reset_password_process(request.new_password)
        return {
            "message": "Password successfully updated kindly check your email for further instructions."
        }

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


# @router.get("/session/{token}", response_model=LoginResponse)
# async def login(token: str):
#     try:
#         logger.info(id)
#         session = Session()
#         resposne = await session.get_session_by_token(token)
#         if not resposne:
#             raise Exception("Session not found")
#         if Session.check_if_session_is_expired(resposne.expires_at):
#             raise Exception("Session expired, Kindly login again")
#         resposne = {
#             "token_id": resposne.id,
#             "name": resposne.user.name,
#             "service_name": resposne.user.service_name,
#             "message": "Session found successfully",
#             "expires_at": resposne.expires_at,
#         }
#         return resposne

#     except ValidationError as e:
#         traceback.print_exc()
#         raise HTTPException(
#             status_code=401,
#             detail={
#                 "message": "Validation Error",
#                 "details": e.errors(include_url=False, include_input=False),
#             },
#         )
#     except Exception as e:
#         traceback.print_exc()
#         logger.exception(str(e))
#         raise HTTPException(status_code=400, detail={"message": str(e), "details": []})
