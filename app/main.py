from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from app.setting import settings

app = FastAPI()

MAX_RETRIES = 5
RETRY_DELAY = 2
trial_count = 0
while True :
    try :
        conn = psycopg2.connect(
            host = settings.DB_HOST,
            database = settings.DB_NAME,
            user = settings.DB_USER,
            password = settings.DB_PASSWORD,
            cursor_factory = RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as e:
        print("Database connection failed.")
        print("Error:", e)
        time.sleep(RETRY_DELAY)
    trial_count += 1
    if trial_count >= MAX_RETRIES:
        raise RuntimeError(f"Failed to connect to the database after {MAX_RETRIES} attempts.")

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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Hello World"
    }

@app.get("/posts")
def get_posts() -> dict[str, list[dict[str, Any]]]:
    
    global cursor
    
    cursor.execute(
        """
        SELECT
            *
        FROM
            posts
        """
    )
    posts = cursor.fetchall()
    print(posts)
    return {
        "data": posts
    }

@app.get("/posts/{id}") # id feild is a path parameter, it is required and it is of type int.
def get_post(id: int, response: Response) : # If we don't specify the type of id, it will be treated as a string and we won't be able to find the post with the given id.
    
    global cursor
    
    print(id)
    cursor.execute(
        """
        SELECT
            *
        FROM
            posts
        WHERE
            id = %s
        """, (str(id),) # We need to pass the id as a tuple in the second argument of the execute method, and we need to convert it to string.
    )
    post = cursor.fetchone()
    print(post)

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
    return {
        "post_details": post
    }

# fast-api will alway send status code 200 for successful requests, but we can change it to 201 for POST requests to indicate that a new resource has been created successfully.
@app.post("/posts", status_code = status.HTTP_201_CREATED) # status code 201 means that the resource has been created successfully.
def create_posts(post: Post):
    # From payload, we need only 2 fields, title as a string and content as a string.
    
    global cursor, conn
    
    print(post)
    print(post.model_dump())
    cursor.execute(
        # We use the notation %s to prevent SQL injection attacks,
        # and we pass the values as a tuple in the second argument of the execute method.
        """
        INSERT INTO
            posts
            (title, content, published)
        VALUES
            (%s, %s, %s)
        RETURNING
            *
        """, (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit() # We need to commit the transaction to save the changes in the database.
    return {
        "new_post": new_post
    }

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT) # status code 204 means that the resource has been deleted successfully and there is no content to return in the response body.
def delete_post(id: int):
    # find the index in the array that has required ID, then remove that index from the array and return the response.
    
    global cursor, conn
    
    cursor.execute(
        """
        DELETE FROM
            posts
        WHERE
            id = %s
        RETURNING
            *
        """, (str(id),)
    )
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    return Response(
        status_code = status.HTTP_204_NO_CONTENT
    )
    # We can also return a custom response with the status code and the message,
    # but it is not recommended to return a message in the response body for a DELETE request with status code 204,
    # as it indicates that there is no content to return in the response body.

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    global cursor, conn

    cursor.execute(
        """
        UPDATE
            posts
        SET
            title = %s,
            content = %s,
            published = %s
        WHERE
            id = %s
        RETURNING
            *
        """, (post.title, post.content, post.published, str(id))
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    return {
        "updated_post": updated_post
    }


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
