##
## A criaçäo desse script foi parcialmente assistida
## por IA para facilitar o processo de migração
##

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Ingredient, Recipe, RecipeIngredient
from app.core.database import Base, DATABASE_URL

# SQLite database URL
SQLITE_DATABASE_URL = "sqlite:///recipes.db"

# Create engines for SQLite and PostgreSQL
sqlite_engine = create_engine(SQLITE_DATABASE_URL)
postgres_engine = create_engine(DATABASE_URL)

# Create session factories
SQLiteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)

def migrate_data():
    # Create tables in PostgreSQL if they don't exist
    Base.metadata.create_all(bind=postgres_engine)

    # Open sessions
    sqlite_session = SQLiteSession()
    postgres_session = PostgresSession()

    try:
        # Migrate Ingredients
        ingredients = sqlite_session.query(Ingredient).all()
        for ingredient in ingredients:
            # Check if the ingredient already exists in PostgreSQL
            existing = postgres_session.query(Ingredient).filter_by(id=ingredient.id).first()
            if not existing:
                postgres_session.add(Ingredient(
                    id=ingredient.id,
                    name=ingredient.name,
                    unit_of_measure=ingredient.unit_of_measure
                ))

        # Migrate Recipes
        recipes = sqlite_session.query(Recipe).all()
        for recipe in recipes:
            # Check if the recipe already exists in PostgreSQL
            existing = postgres_session.query(Recipe).filter_by(id=recipe.id).first()
            if not existing:
                new_recipe = Recipe(
                    id=recipe.id,
                    name=recipe.name,
                    preparation_method=recipe.preparation_method
                )
                postgres_session.add(new_recipe)

                # Migrate Recipe Ingredients
                for ri in recipe.ingredients:
                    existing_ri = postgres_session.query(RecipeIngredient).filter_by(
                        recipe_id=ri.recipe_id,
                        ingredient_id=ri.ingredient_id
                    ).first()
                    if not existing_ri:
                        postgres_session.add(RecipeIngredient(
                            recipe_id=ri.recipe_id,
                            ingredient_id=ri.ingredient_id,
                            quantity=ri.quantity
                        ))

        # Commit changes to PostgreSQL
        postgres_session.commit()
        print("Data migration completed successfully!")

    except Exception as e:
        postgres_session.rollback()
        print(f"Error during migration: {e}")

    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == "__main__":
    migrate_data()