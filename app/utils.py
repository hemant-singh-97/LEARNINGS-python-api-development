from sqlalchemy.inspection import inspect
from typing import Any
from passlib.context import CryptContext

def row_to_dict(row: Any) -> dict[str, Any]:
    return {
        c.key: getattr(row, c.key)
        for c in inspect(row).mapper.column_attrs
    }


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash(password: str) -> str:
    return pwd_context.hash(password)