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
    """
    Vote post functionality

    Args:
        vote (schemas.Vote): The vote
        db (Session, optional): db pgsql session. Defaults to Depends(get_db).
        user (_type_, optional): the vote user (get by request or from session in key). Defaults to Depends(oauth2.get_current_user).

    Raises:
        HTTPException: 404 if post to be meant to be voted does not exists

    Returns:
        str: a message confirming if vote or unvote have been registered on database.

    Comments: First time a user call vote on a post, the record and positive vote is recorded.
    The second time the same user vote the same post, the existing vote will be deleted from db as on any social media like works.
    This functionality does not work exactly as on course, originally it sends an extra parameter on the request specifying the direction
    (1 or 0) to add or delete a vote but personally I think it get the method more complicated unnecessarily.
    """

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

# endregion
