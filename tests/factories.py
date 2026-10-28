"""Test data factory for the product catalogue."""

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import Product, Category

class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""
        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=[
        "Hat", "Shoes", "Big Mac", "Sheets", "Hammer", "Laptop"
    ])
    description = factory.Faker("text")
    price = FuzzyDecimal(0.5, 2000.0, 2)
    available = FuzzyChoice(choices=[True, False])
    category = FuzzyChoice(choices=[
        Category.UNKNOWN,
        Category.CLOTHS,
        Category.FOOD,
        Category.HOUSEWARES,
        Category.AUTOMOTIVE,
        Category.TOOLS
    ])
