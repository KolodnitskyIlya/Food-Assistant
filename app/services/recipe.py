from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate


class RecipeService:
    @staticmethod
    async def create_recipe(db: AsyncSession, recipe_create: RecipeCreate, user_id: int) -> Recipe:
        recipe = Recipe(**recipe_create.dict(), user_id=user_id)
        db.add(recipe)
        await db.commit()
        await db.refresh(recipe)
        return recipe

    @staticmethod
    async def get_user_recipes(db: AsyncSession, user_id: int) -> List[Recipe]:
        result = await db.execute(select(Recipe).where(Recipe.user_id == user_id))
        return result.scalars().all()