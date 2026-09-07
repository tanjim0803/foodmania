from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.utils.user import decode_token
from app.database.session import SessionDep
from fastapi import HTTPException, status
from app.services.user import user_services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    db: SessionDep, token: Annotated[dict, Depends(oauth2_scheme)]
):
    token_decode = decode_token(token)

    user_id = token_decode.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = await user_services.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exists!"
        )

    return user
