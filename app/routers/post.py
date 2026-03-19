from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas
from app import models
from app.database import get_db
from app.utils import row_to_dict

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

@router.get("/", response_model = list[schemas.PostResponse]) # response_model is used to specify the model of the response, it will automatically convert the response to the specified model and return it in the response body.
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    print(type(posts))
    print(row_to_dict(posts[0]))
    return posts

@router.get("/{id}", response_model = schemas.PostResponse) # id feild is a path parameter, it is required and it is of type int.
def get_post(id: int, db: Session = Depends(get_db)) :
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(row_to_dict(post))

    if post is None:
        # method 1: We can return a custom response with the status code and the error message.
        # response.status_code = status.HTTP_404_NOT_FOUND # We can set the status code of the response to 404 if the post is not found.
        # return {
        #     "error": f"Post with id {id} not found."
        # }
        
        # method 2: We can raise an HTTPException with the status code and the error message.
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    return post

# fast-api will alway send status code 200 for successful requests, but we can change it to 201 for POST requests to indicate that a new resource has been created successfully.
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse) # status code 201 means that the resource has been created successfully.
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post =  models.Post(
        **post.model_dump()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    print(type(new_post))
    print(row_to_dict(new_post))
    return new_post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT) # status code 204 means that the resource has been deleted successfully and there is no content to return in the response body.
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(
        status_code = status.HTTP_204_NO_CONTENT
    )
    # We can also return a custom response with the status code and the message,
    # but it is not recommended to return a message in the response body for a DELETE request with status code 204,
    # as it indicates that there is no content to return in the response body.

@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()