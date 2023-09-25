from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

router = APIRouter(prefix="/posts", tags=['Posts'])

# region POSTS GET


@router.get("/", response_model=List[schemas.PostOut])
async def posts(db: Session = Depends(get_db), user=Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """
    API posts route

    Returns:
        str: JSON with gathered posts from db

    Example: {{URL}}/posts?limit=10&skip=0&search=<text>
    """
    # URL example: {{URL}}/posts?limit=10&skip=0&search=<text>
    results = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(func.lower(models.Post.title).contains(func.lower(search))).limit(limit).offset(skip).all()

    return results


@router.get("/{id}", response_model=schemas.ResponsePost)
async def get_post(id: int, db: Session = Depends(get_db), user=Depends(oauth2.get_current_user)):
    """
    Get's an item by id

    Args:
        id (str): Item id

    Returns:
        str: the id of the Item (primary key)
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not found')

    # if post.author_id != user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    return post


@router.get("/latest/", response_model=schemas.ResponsePost)
async def get_latest(db: Session = Depends(get_db), user=Depends(oauth2.get_current_user)):
    """
    Returns last item added

    Returns:
        str: JSON representing the latest item added

    Comments: Added slash at the end to avoid route conflict with get_post
    """
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'no records found')

    # if post.author_id != user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="User does not own latest record")
    return post

# endregion

# region POSTS POST


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
async def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), user=Depends(oauth2.get_current_user)):
    """
    post con un JSON y diferentes parametros

    Args:
        post (Post): Un objeto de la clase Post con los campos requeridos en el post.

    Returns:
        str: el nuevo registro
    """
    new_post = models.Post(author_id=user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# endregion

# region POSTS DELETE


@router.delete("/{id}")
async def delete_post(id: str, db: Session = Depends(get_db), user=Depends(oauth2.get_current_user)):
    """
    delete an item

    Args:
        id (str): item id to delete

    Raises:
        HTTPException: HTTP_404_NOT_FOUND if the id doesn't exists

    Returns:
        HTTP status: HTTP_204_NO_CONTENT if item deleted
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        if post.author_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not found')
# endregion

# region POSTS PUT


@router.put("/{id}", response_model=schemas.ResponsePost)
async def update_post(id: str, updated_post: schemas.CreatePost, db: Session = Depends(get_db), user=Depends(oauth2.get_current_user)):
    """
    Updates a post given a post id

    Args:
        id (str): post id
        post (Post): post fields
    Raises:
        HTTPException: if not id found

    Returns:
        Response: fastapi.Response object with status code
    """
    post_query = db.query(models.Post).filter(models.Post.id == id).first()

    if post_query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} not found')

    if post_query.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # A different approach
    post_query.title = updated_post.title
    post_query.content = updated_post.content
    post_query.published = updated_post.published
    db.commit()
    db.refresh(post_query)
    return post_query
# endregion
