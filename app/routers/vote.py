from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

router = APIRouter(prefix="/vote", tags=['vote'])

# region VOTES GET


@router.post("/", status_code=status.HTTP_200_OK)
async def vote(vote: schemas.Vote, db: Session = Depends(get_db), user=Depends(oauth2.get_current_user)):

    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {vote.post_id} does not exist')

    vote_record = db.query(models.Vote).filter(models.Vote.post_id ==
                                               vote.post_id, models.Vote.user_id == user.id).first()
    if not vote_record:
        new_vote = models.Vote(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message": f"User with id {user.id} has voted post {vote.post_id} successfully"}
    else:
        db.delete(vote_record)
        db.commit()
        return {"message": f"User with id {user.id} has removed vote from post {vote.post_id} successfully"}


@router.get("/", response_model=List[schemas.ResponsePost])
async def get_votes(db: Session = Depends(get_db), user=Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    pass
# endregion
