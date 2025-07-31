from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    goal: str
    cooking_time: int
    ingredients: str


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    goal: Optional[str]
    cooking_time: Optional[int]
    ingredients: Optional[str]


class RecipeResponse(RecipeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True