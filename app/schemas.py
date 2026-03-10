from pydantic import BaseModel
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str


class DocumentCreate(BaseModel):
    category_id: int
    title: str
    content: str


class SearchRequest(BaseModel):
    category_id: int
    query: str


class SearchLogCreate(BaseModel):
    query: str
    category_id: int
    result: int


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class DocumentUpdate(BaseModel):
    category_id: int
    title: str
    content: str


class UserCreate(BaseModel):
    user_id: str
    user_name: str
    user_role: int


class UserLogin(BaseModel):
    user_id: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ApiKeyResponse(BaseModel):
    api_key: str