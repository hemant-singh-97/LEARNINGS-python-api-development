from fastapi import FastAPI, Response, status, HTTPException
# from fastapi import Body
from pydantic import BaseModel
from typing import Optional, Any

app = FastAPI()

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

my_posts: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the content of the first post.",
        "published": True,
        "rating": 5
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is the content of the second post.",
        "published": False,
        "rating": None
    }
]
global_id = 3

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def find_post(my_posts: list[dict[str, Any]], id: int) -> Optional[dict[str, Any]]:
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

def find_post_index(my_posts: list[dict[str, Any]], id: int) -> Optional[int]:
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Hello World"
    }

@app.get("/posts")
def get_posts() -> dict[str, list[dict[str, Any]]]:
    
    global my_posts
    
    print(my_posts)
    return {
        "data": my_posts
    }

@app.get("/posts/{id}") # id feild is a path parameter, it is required and it is of type int.
def get_post(id: int, response: Response) : # If we don't specify the type of id, it will be treated as a string and we won't be able to find the post with the given id.
    
    global my_posts
    
    print(id)
    post = find_post(my_posts, id)
    if not post:
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
    
    global global_id, my_posts
    
    print(post)
    print(post.model_dump())
    my_posts.append(
        {
            "id": global_id,
            **post.model_dump()
        }
    )
    global_id += 1
    return {
        "new_post": f"title: {post.title}, content: {post.content}, published: {post.published}, rating: {post.rating}"
    }

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT) # status code 204 means that the resource has been deleted successfully and there is no content to return in the response body.
def delete_post(id: int):
    # find the index in the array that has required ID, then remove that index from the array and return the response.
    
    global my_posts
    
    post_idx = find_post_index(my_posts, id)
    if post_idx is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found."
        )
    my_posts.pop(post_idx)
    return Response(
        status_code = status.HTTP_204_NO_CONTENT
    )
    # We can also return a custom response with the status code and the message,
    # but it is not recommended to return a message in the response body for a DELETE request with status code 204,
    # as it indicates that there is no content to return in the response body.