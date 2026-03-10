from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone, timedelta
from .database import Base

JST = timezone(timedelta(hours=9))

def now_jst():
    return datetime.now(JST)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), default=now_jst)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), default=now_jst)


class SearchLog(Base):
    __tablename__ = "search_logs"

    id = Column(Integer, primary_key=True)
    query = Column(Text)
    category_id = Column(Integer)
    result = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=now_jst)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    user_name = Column(String)
    user_role = Column(Integer)
    api_key = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)