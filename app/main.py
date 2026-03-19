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

from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import post, user

# This will create the tables in the database based on the models defined in the models.py file.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routers
app.include_router(post.router)
app.include_router(user.router)

"""
Always keeps the API endpoints as plural, for example, /posts instead of /post.
This is a good practice to follow when designing RESTful APIs.
"""

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Hello World"
    }