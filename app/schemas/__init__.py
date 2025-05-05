from pydantic import BaseModel
from typing import List

# Ingredient
class IngredientCreate(BaseModel):
    name: str
    unit_of_measure: str

class IngredientRead(BaseModel):
    id: int
    name: str
    unit_of_measure: str

    class Config:
        orm_mode = True

# Novo esquema para uma lista de ingredientes
class IngredientCreateList(BaseModel):
    ingredients: List[IngredientCreate]

# RecipeIngredient
class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
    quantity: float

class RecipeIngredientRead(BaseModel):
    ingredient: IngredientRead
    quantity: float

    class Config:
        orm_mode = True

# Recipe
class RecipeCreate(BaseModel):
    name: str
    preparation_method: str
    ingredients: List[RecipeIngredientCreate]

class RecipeRead(BaseModel):
    id: int
    name: str
    preparation_method: str
    ingredients: List[RecipeIngredientRead]

    class Config:
        orm_mode = True

# Novo esquema para uma lista de receitas
class RecipeCreateList(BaseModel):
    recipes: List[RecipeCreate]