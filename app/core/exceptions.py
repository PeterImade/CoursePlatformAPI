from typing import Any, Callable

from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse


class CoursePlatformException(Exception):
    """This is the base class for all bookly errors"""
    pass

class InvalidToken(CoursePlatformException):
    """User has provided an invalid or expired token"""
    pass

class InvalidOTP(CoursePlatformException):
    """User has provided an invalid or expired otp"""
    pass

class RevokedToken(CoursePlatformException):
    """User has provided a token that has been revoked"""
    pass

class AccessTokenRequired(CoursePlatformException):
    """User has provided a refresh token when an access token is needed"""
    pass

class RefreshTokenRequired(CoursePlatformException):
    """User has provided an access token when a refresh token is needed"""
    pass

class UserAlreadyExists(CoursePlatformException):
    """User has provided an email for a user who exists during sign up."""
    pass

class InvalidCredentials(CoursePlatformException):
    """User has provided wrong email or password during log in."""
    pass

class InvalidRequest(CoursePlatformException):
    """User has provided wrong email or password during log in."""
    pass
class InvalidRequest(CoursePlatformException):
    """User has provided wrong email or password during log in."""
    pass

class InsufficientPermission(CoursePlatformException):
    """User does not have the necessary permissions to perform an action."""
    pass

class CourseNotFound(CoursePlatformException):
    """Course Not found"""
    pass

class EmailError(CoursePlatformException):
    """Email Not Sent"""
    pass

class UserNotFound(CoursePlatformException):
    """User Not found"""
    pass

class TooManyRequests(CoursePlatformException):
    """Too many requests"""
    pass


def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: CoursePlatformException):
        return JSONResponse(content=initial_detail, status_code=status_code)
    return exception_handler

def register_error_handlers(app: FastAPI):
    app.add_exception_handler(UserAlreadyExists, create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, initial_detail={
        "message": "User with email already exists",
        "error_code": "user_exists"
    }))

    app.add_exception_handler(CourseNotFound, create_exception_handler(status_code=status.HTTP_404_NOT_FOUND, initial_detail={
        "message": "Course not found",
        "error_code": "course_not_found"
    }))
    
    app.add_exception_handler(EmailError, create_exception_handler(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, initial_detail={
        "message": "Failed to send email due to server error.",
        "error_code": "email_not_sent"
    }))

    app.add_exception_handler(InvalidCredentials, create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST, initial_detail={
        "message": "Invalid Email or Password",
        "error_code": "invalid_email_or_password"
    }))
  
    app.add_exception_handler(InvalidRequest, create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST, initial_detail={
        "message": "Invalid Request",
        "error_code": "invalid_request"
    }))

    app.add_exception_handler(InvalidToken, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={
        "message": "Token is invalid Or expired",
        "resolution": "Please get new token",
        "error_code": "invalid_token"
    }))

    app.add_exception_handler(InvalidOTP, create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST, initial_detail={
        "message": "OTP is invalid Or expired",
        "resolution": "Please get new OTP",
        "error_code": "invalid_otp"
    }))

    app.add_exception_handler(RevokedToken, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={
        "message": "Token is invalid or has been revoked",
        "resolution": "Please get new token",
        "error_code": "token_revoked"
    }))

    app.add_exception_handler(AccessTokenRequired, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={
        "message": "Please provide a valid access token",
        "resolution": "Please get an access token",
        "error_code": "access_token_required"
    }))
    
    app.add_exception_handler(RefreshTokenRequired, create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, initial_detail={
        "message": "Please provide a valid refresh token",
        "resolution": "Please get a refresh token",
        "error_code": "refresh_token_required"
    }))
    
    app.add_exception_handler(InsufficientPermission, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={
        "message": "You do not have enough permissions to perform this action",
        "error_code": "insufficient_permissions"
    }))

    app.add_exception_handler(UserNotFound, create_exception_handler(status_code=status.HTTP_404_NOT_FOUND,initial_detail={
        "message": "User not found",
        "error_code": "user_not_found",
    }))
   
    app.add_exception_handler(TooManyRequests, create_exception_handler(status_code=status.HTTP_429_TOO_MANY_REQUESTS,initial_detail={
        "message": "You have exceeded the maximum number of OTP requests.",
        "resolution": "Please wait for a few minutes before trying again.",
        "error_code": "too_many_requests",
    }))



    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(content={
            "message": "Oops! Something went wrong",
            "error_code": "internal_server_error"
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)