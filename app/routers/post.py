from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func

from app import schemas, models, oauth2
from app.database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

"""
CRUD Operations:
1. Create: POST /posts (app.post("/posts"))
2. Read: GET /posts (app.get("/posts"))
3. Update: PUT /posts/{id} (app.put("/posts/{id}")) OR PATCH /posts/{id} (app.patch("/posts/{id}"))
The difference in PUT and PATCH is that PUT is used to update the entire resource, while PATCH is used to update only a part of the resource.
For example, if we have a post with title and content, and we want to update only the title, we can use PATCH /posts/{id} with the new title in the request body.
If we want to update both the title and content, we can use PUT /posts/{id} with the new title and content in the request body.
4. Delete: DELETE /posts/{id} (app.delete("/posts/{id}"))
"""

@router.get("/", response_model = list[schemas.PostWithVotes])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts_with_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts_with_votes

@router.get("/{id}", response_model = schemas.PostWithVotes)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    return post


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    new_post =  models.Post(
        owner_id=current_user.id,
        **post.model_dump()

    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to perform requested action."
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(
        status_code = status.HTTP_204_NO_CONTENT
    )

@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id: int, request_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to perform requested action."
        )

    post_query.update(request_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()