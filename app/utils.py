from sqlalchemy.inspection import inspect
from typing import Any
from passlib.context import CryptContext

def row_to_dict(row: Any) -> dict[str, Any]:
    return {
        c.key: getattr(row, c.key)
        for c in inspect(row).mapper.column_attrs
        if c not in ("password",) # we can exclude the password field from the response for security reasons.
    }


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash(password: str) -> str:
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)