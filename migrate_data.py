from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Ingredient, Recipe, RecipeIngredient
from app.core.database import Base, DATABASE_URL

# SQLite database URL
SQLITE_DATABASE_URL = "sqlite:///recipes.db"

# Create engines for SQLite and MySQL
sqlite_engine = create_engine(SQLITE_DATABASE_URL)
mysql_engine = create_engine(DATABASE_URL)

# Create session factories
SQLiteSession = sessionmaker(bind=sqlite_engine)
MySQLSession = sessionmaker(bind=mysql_engine)

def migrate_data():
    # Create tables in MySQL if they don't exist
    Base.metadata.create_all(bind=mysql_engine)

    # Open sessions
    sqlite_session = SQLiteSession()
    mysql_session = MySQLSession()

    try:
        # Migrate Ingredients
        ingredients = sqlite_session.query(Ingredient).all()
        for ingredient in ingredients:
            # Check if the ingredient already exists in MySQL
            existing = mysql_session.query(Ingredient).filter_by(id=ingredient.id).first()
            if not existing:
                mysql_session.add(Ingredient(
                    id=ingredient.id,
                    name=ingredient.name,
                    unit_of_measure=ingredient.unit_of_measure
                ))

        # Migrate Recipes
        recipes = sqlite_session.query(Recipe).all()
        for recipe in recipes:
            # Check if the recipe already exists in MySQL
            existing = mysql_session.query(Recipe).filter_by(id=recipe.id).first()
            if not existing:
                new_recipe = Recipe(
                    id=recipe.id,
                    name=recipe.name,
                    preparation_method=recipe.preparation_method
                )
                mysql_session.add(new_recipe)

                # Migrate Recipe Ingredients
                for ri in recipe.ingredients:
                    existing_ri = mysql_session.query(RecipeIngredient).filter_by(
                        recipe_id=ri.recipe_id,
                        ingredient_id=ri.ingredient_id
                    ).first()
                    if not existing_ri:
                        mysql_session.add(RecipeIngredient(
                            recipe_id=ri.recipe_id,
                            ingredient_id=ri.ingredient_id,
                            quantity=ri.quantity
                        ))

        # Commit changes to MySQL
        mysql_session.commit()
        print("Data migration completed successfully!")

    except Exception as e:
        mysql_session.rollback()
        print(f"Error during migration: {e}")

    finally:
        sqlite_session.close()
        mysql_session.close()

if __name__ == "__main__":
    migrate_data()