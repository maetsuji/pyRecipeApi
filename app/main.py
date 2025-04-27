from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base
from typing import List

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ingredient Endpoints
@app.post('/api/ingredients', response_model=schemas.IngredientRead, status_code=status.HTTP_201_CREATED)
def create_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    return crud.create_ingredient(db, ingredient)

@app.post('/api/ingredients/bulk', response_model=List[schemas.IngredientRead], status_code=status.HTTP_201_CREATED)
def create_ingredients_bulk(ingredients: schemas.IngredientCreateList, db: Session = Depends(get_db)):
    created_ingredients = []
    for ingredient_data in ingredients.ingredients:
        # Verifica se o ingrediente já existe
        existing_ingredient = db.query(models.Ingredient).filter(models.Ingredient.name == ingredient_data.name).first()
        if existing_ingredient:
            raise HTTPException(status_code=400, detail=f"Ingredient '{ingredient_data.name}' already exists.")
        # Cria o ingrediente
        created_ingredient = crud.create_ingredient(db, ingredient_data)
        created_ingredients.append(created_ingredient)
    return created_ingredients

@app.get('/api/ingredients', response_model=List[schemas.IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(models.Ingredient).all()

@app.put('/api/ingredients/{id}', response_model=schemas.IngredientRead)
def update_ingredient(id: int, ing: schemas.IngredientCreate, db: Session = Depends(get_db)):
    return crud.update_ingredient(db, id, ing)

@app.delete('/api/ingredients/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(id: int, db: Session = Depends(get_db)):
    crud.delete_ingredient(db, id)
    return None

# Recipe Endpoints
@app.post('/api/recipes', response_model=schemas.RecipeRead, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)

@app.post('/api/recipes/bulk', response_model=List[schemas.RecipeRead], status_code=status.HTTP_201_CREATED)
def create_recipes_bulk(recipes: schemas.RecipeCreateList, db: Session = Depends(get_db)):
    created_recipes = []
    for recipe_data in recipes.recipes:
        # Verifica se a receita já existe
        existing_recipe = db.query(models.Recipe).filter(models.Recipe.name == recipe_data.name).first()
        if existing_recipe:
            raise HTTPException(status_code=400, detail=f"Recipe '{recipe_data.name}' already exists.")
        # Cria a receita
        created_recipe = crud.create_recipe(db, recipe_data)
        created_recipes.append(created_recipe)
    return created_recipes

@app.get('/api/recipes', response_model=List[schemas.RecipeRead])
def list_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).all()

@app.get('/api/recipes/{id}', response_model=schemas.RecipeRead)
def get_recipe(id: int, db: Session = Depends(get_db)):
    return crud.get_recipe(db, id)

@app.put('/api/recipes/{id}', response_model=schemas.RecipeRead)
def update_recipe(id: int, recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.update_recipe(db, id, recipe)

@app.delete('/api/recipes/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(id: int, db: Session = Depends(get_db)):
    crud.delete_recipe(db, id)
    return None