from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.exceptions import ResponseValidationError


router = APIRouter(prefix='/users', tags=['Users'])

# region USERS POST


# , response_model=schemas.UserResponse)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """
    Creates a new user

    Args:
        db (Session, optional): postgres db session. Defaults to Depends(get_db).
    """

    user_exists = db.query(models.User).filter(
        models.User.email == user.email).first()
    if user_exists is None:
        new_user = models.User(**user.model_dump())
        new_user.password = utils.hash_password(user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with email {user.email} already exists')


@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db), user=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not found')
    return user


# endregion
