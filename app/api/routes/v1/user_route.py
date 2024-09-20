from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from app.api.models.user_model import User
from app.authentication.auth import UserUseCases
from app.authentication.depends import get_current_user
from app.authentication.depends import token_is_valid
from app.core.database.db import get_db
from app.core.security import request_limiter

user_route = APIRouter(prefix="/user", dependencies=[Depends(token_is_valid)])
limiter = request_limiter.get_limiter()


@user_route.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def register(request: Request, user: User, db_session=Depends(get_db)):
    uc = UserUseCases(db_session)
    uc.register(user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": "User created"}
    )


@user_route.get("/me", status_code=status.HTTP_200_OK)
@limiter.limit("60/minute")
def me(
    request: Request,
    user: User = Depends(get_current_user),
    authorization: str = Header(None),
):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "user": user.username,
            "is_admin": user.is_admin,
            "token": authorization,
        },
    )


@user_route.post("/disable", status_code=status.HTTP_200_OK)
@limiter.limit("60/minute")
def disable(
    request: Request, user: User = Depends(get_current_user), db_session=Depends(get_db)
):
    uc = UserUseCases(db_session)
    uc.disable(user.username)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "User disabled"}
    )
