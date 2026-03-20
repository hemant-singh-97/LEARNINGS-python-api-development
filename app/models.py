from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    # If the table name does not exist, SQLAlchemy will create it for us.
    # If it already exists, it will use the existing table, without altering it in any way.
    # So, if the table exists and the Type Constraints are changed, it will not throw an error, but it will not alter the table either.
    # Additionally, if some new columns are added to the model, it will not alter the table to add those columns,
    # and it will throw an error if we try to insert data into those new columns, because those columns do not exist in the table.
    
    # Incase we want to alter the table, we need to use Alembic, which is a database migration tool for SQLAlchemy.
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)