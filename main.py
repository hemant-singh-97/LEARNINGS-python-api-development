from fastapi import FastAPI
# from fastapi import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Always keeps the API endpoints as plural, for example, /posts instead of /post. This is a good practice to follow when designing RESTful APIs.

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Hello World"
    }

@app.get("/posts")
def get_posts() -> dict[str, list[dict[str, str | int]]]:
    return {
        "data": [
            {
                "title": "First Post",
                "content": "This is the content of the first post."
            },
            {
                "title": "Second Post",
                "content": "This is the content of the second post."
            }
        ]
    }

@app.post("/createposts")
def create_posts(post: Post):
    # From payload, we need onlt 2 fields, title as a string and content as a string.
    print(post)
    print(post.model_dump())
    return {
        "new_post": f"title: {post.title}, content: {post.content}, published: {post.published}, rating: {post.rating}"
    }

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