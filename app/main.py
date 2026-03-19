from fastapi import FastAPI, Response, status, HTTPException, Depends
# from typing import Any, List
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from sqlalchemy.orm import Session

# from app.setting import settings
from app import schemas
from app import models
from app.database import engine, get_db
from app.utils import row_to_dict

models.Base.metadata.create_all(bind=engine)
# This will create the tables in the database based on the models defined in the models.py file.

app = FastAPI()

# MAX_RETRIES = 5
# RETRY_DELAY = 2
# trial_count = 0
# while True :
#     try :
#         conn = psycopg2.connect(
#             host = settings.DB_HOST,
#             database = settings.DB_NAME,
#             user = settings.DB_USER,
#             password = settings.DB_PASSWORD,
#             cursor_factory = RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful.")
#         break
#     except Exception as e:
#         print("Database connection failed.")
#         print("Error:", e)
#         time.sleep(RETRY_DELAY)
#     trial_count += 1
#     if trial_count >= MAX_RETRIES:
#         raise RuntimeError(f"Failed to connect to the database after {MAX_RETRIES} attempts.")

"""
Always keeps the API endpoints as plural, for example, /posts instead of /post.
This is a good practice to follow when designing RESTful APIs.
"""

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

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Hello World"
    }

@app.get("/posts", response_model = list[schemas.PostResponse]) # response_model is used to specify the model of the response, it will automatically convert the response to the specified model and return it in the response body.
def get_posts(db: Session = Depends(get_db)):
    
    # global cursor
    
    # cursor.execute(
    #     """
    #     SELECT
    #         *
    #     FROM
    #         posts
    #     """
    # )
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    print(posts)
    print(type(posts))
    print(row_to_dict(posts[0]))
    return posts

@app.get("/posts/{id}", response_model = schemas.PostResponse) # id feild is a path parameter, it is required and it is of type int.
# def get_post(id: int, response: Response) : # If we don't specify the type of id, it will be treated as a string and we won't be able to find the post with the given id.
def get_post(id: int, db: Session = Depends(get_db)) :
    
    # global cursor
    
    # print(id)
    # cursor.execute(
    #     """
    #     SELECT
    #         *
    #     FROM
    #         posts
    #     WHERE
    #         id = %s
    #     """, (str(id),) # We need to pass the id as a tuple in the second argument of the execute method, and we need to convert it to string.
    # )
    # post = cursor.fetchone()
    # print(post)
    
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
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse) # status code 201 means that the resource has been created successfully.
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # From payload, we need only 2 fields, title as a string and content as a string.
    
    # global cursor, conn
    
    # print(post)
    # print(post.model_dump())
    # cursor.execute(
    #     # We use the notation %s to prevent SQL injection attacks,
    #     # and we pass the values as a tuple in the second argument of the execute method.
    #     """
    #     INSERT INTO
    #         posts
    #         (title, content, published)
    #     VALUES
    #         (%s, %s, %s)
    #     RETURNING
    #         *
    #     """, (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit() # We need to commit the transaction to save the changes in the database.
    
    # This is inefficient if there are a large number of fields in the model,
    # and we need to update all the fields in the model,
    # then we need to write all the fields in the code, which is not a good practice.
    # new_post = models.Post(
    #     title = post.title,
    #     content = post.content,
    #     published = post.published
    # )
    
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

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT) # status code 204 means that the resource has been deleted successfully and there is no content to return in the response body.
def delete_post(id: int, db: Session = Depends(get_db)):
    # find the index in the array that has required ID, then remove that index from the array and return the response.
    
    # global cursor, conn
    
    # cursor.execute(
    #     """
    #     DELETE FROM
    #         posts
    #     WHERE
    #         id = %s
    #     RETURNING
    #         *
    #     """, (str(id),)
    # )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
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

@app.put("/posts/{id}", response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # global cursor, conn

    # cursor.execute(
    #     """
    #     UPDATE
    #         posts
    #     SET
    #         title = %s,
    #         content = %s,
    #         published = %s
    #     WHERE
    #         id = %s
    #     RETURNING
    #         *
    #     """, (post.title, post.content, post.published, str(id))
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


"""
FastAPI comes with a built-in interactive API documentation interface, which is automatically generated based on the API endpoints and the request/response models defined in the code.
This interface allows developers to easily test the API endpoints and see the expected request/response formats without needing to use external tools like Postman or cURL.
The interactive API documentation can be accessed by navigating to the /docs endpoint of the FastAPI application in a web browser.
For example, if the FastAPI application is running locally on port 8000, the interactive API documentation can be accessed at
    1. http://localhost:8000/docs (Swagger UI interface for API documentation and testing)
    2. http://localhost:8000/redoc (alternative documentation interface with a different layout and design)
"""

"""
To run the FastAPI application, we can use the command:
    1. fastapi dev
    2. fastapi dev --app app app/main.py
The first command will look for the FastAPI application in the current directory and run it,
while the second command allows us to specify the location of the FastAPI application if it is not in the current directory.
"""
