from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

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
                "id": 1,
                "title": "First Post",
                "content": "This is the content of the first post."
            },
            {
                "id": 2,
                "title": "Second Post",
                "content": "This is the content of the second post."
            }
        ]
    }

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {
        "new_post": f"title: {payload['title']}, content: {payload['content']}"
    }