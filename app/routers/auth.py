from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, utils, oauth2, schemas


router = APIRouter(prefix='/login', tags=['Auth'])


@router.post('/', response_model=schemas.Token)
async def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)) -> dict[str, str]:
    """
    User login API route

    Args:
        user_creds (OAuth2PasswordRequestForm, optional): OAuth2 dependency class. Defaults to Depends().
        db (Session, optional): DB Session. Defaults to Depends(database.get_db).

    Raises:
        HTTPException: email not found
        HTTPException: wrong password

    Returns:
        str: dict in JSON with access token and token type
    """
    user = db.query(models.User).filter(
        models.User.email == user_creds.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(
        data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
