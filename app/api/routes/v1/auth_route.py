from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.api.models.user_model import User
from app.authentication.auth import UserUseCases
from app.authentication.depends import get_current_user
from app.core.config import settings
from app.core.database.db import get_db
from app.core.database.tables.token_table import TokenTable
from app.core.security import request_limiter

auth_route = APIRouter(prefix="/auth")
limiter = request_limiter.get_limiter()


@auth_route.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("60/minute")
def login(
    request: Request,
    user_form: OAuth2PasswordRequestForm = Depends(),
    db_session=Depends(get_db),
):
    try:
        uc = UserUseCases(db_session)
        user = User(username=user_form.username, password=user_form.password)
        auth_data = uc.user_login(user)
        existing_token = (
            db_session.query(TokenTable).filter_by(user_id=auth_data["user_id"]).first()
        )
        if existing_token:
            db_session.delete(existing_token)
        db_session.add(
            TokenTable(user_id=auth_data["user_id"], token=auth_data["access_token"])
        )
        db_session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=auth_data)
    except HTTPException as e:
        settings.logger.error(f"Login failed with error: {e.detail}")
        raise e


@auth_route.get("/logout", status_code=status.HTTP_200_OK)
@limiter.limit("60/minute")
def logout(
    request: Request, user: User = Depends(get_current_user), db_session=Depends(get_db)
):
    try:
        uc = UserUseCases(db_session)
        uc.user_logout(user)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Logged out"}
        )
    except HTTPException as e:
        settings.logger.error(f"Logout failed with error: {e.detail}")
        raise e


@auth_route.put("/change-password", status_code=status.HTTP_200_OK)
@limiter.limit("60/minute")
def change_password(
    request: Request,
    old_password: str,
    new_password: str,
    user: User = Depends(get_current_user),
    db_session=Depends(get_db),
):
    uc = UserUseCases(db_session)
    uc.change_password(user.username, old_password, new_password)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Password changed"}
    )
