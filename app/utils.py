from sqlalchemy.inspection import inspect
from typing import Any

def row_to_dict(row: Any) -> dict[str, Any]:
    return {
        c.key: getattr(row, c.key)
        for c in inspect(row).mapper.column_attrs
    }