from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.utils import hash

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Hash The password before saving it to the database
    hashed_password = hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} not found."
        )
    return user