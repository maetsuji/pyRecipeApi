from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import models
from .. import schemas

# ----- Ingredient CRUD -----

def get_ingredient(db: Session, id: int):
    return db.query(models.Ingredient).get(id)

def create_ingredient(db: Session, ing: schemas.IngredientCreate):
    if db.query(models.Ingredient).filter(models.Ingredient.name == ing.name).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Ingredient already exists')
    db_ing = models.Ingredient(**ing.dict())
    db.add(db_ing)
    db.commit()
    db.refresh(db_ing)
    return db_ing

def update_ingredient(db: Session, id: int, ing: schemas.IngredientCreate):
    db_ing = get_ingredient(db, id)
    if not db_ing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Ingredient not found')
    db_ing.name = ing.name
    db_ing.unit_of_measure = ing.unit_of_measure
    db.commit()
    return db_ing

def delete_ingredient(db: Session, id: int):
    db_ing = get_ingredient(db, id)
    if not db_ing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Ingredient not found')
    db.delete(db_ing)
    db.commit()
    return None

# ----- Recipe CRUD -----

def get_recipe(db: Session, id: int):
    return db.query(models.Recipe).get(id)

def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    if db.query(models.Recipe).filter(models.Recipe.name == recipe.name).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Recipe name already exists')
    if not recipe.ingredients:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Recipe must have ingredients')

    db_recipe = models.Recipe(
        name=recipe.name,
        preparation_method=recipe.preparation_method
    )
    for ri in recipe.ingredients:
        if not get_ingredient(db, ri.ingredient_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f'Ingredient {ri.ingredient_id} not found')
        assoc = models.RecipeIngredient(
            ingredient_id=ri.ingredient_id,
            quantity=ri.quantity
        )
        db_recipe.ingredients.append(assoc)

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def update_recipe(db: Session, id: int, recipe: schemas.RecipeCreate):
    db_recipe = get_recipe(db, id)
    if not db_recipe:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Recipe not found')
    db_recipe.name = recipe.name
    db_recipe.preparation_method = recipe.preparation_method
    # remove ingredients and re-add
    db_recipe.ingredients.clear()
    for ri in recipe.ingredients:
        if not get_ingredient(db, ri.ingredient_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f'Ingredient {ri.ingredient_id} not found')
        assoc = models.RecipeIngredient(
            ingredient_id=ri.ingredient_id,
            quantity=ri.quantity
        )
        db_recipe.ingredients.append(assoc)
    db.commit()
    return db_recipe

def delete_recipe(db: Session, id: int):
    db_recipe = get_recipe(db, id)
    if not db_recipe:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Recipe not found')
    db.delete(db_recipe)
    db.commit()
    return None