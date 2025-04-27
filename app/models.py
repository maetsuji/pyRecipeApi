from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    unit_of_measure = Column(String, nullable=False)

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    preparation_method = Column(Text, nullable=False)
    ingredients = relationship(
        'RecipeIngredient',
        cascade='all, delete, delete-orphan'
    )

class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(Float, nullable=False)
    ingredient = relationship('Ingredient')