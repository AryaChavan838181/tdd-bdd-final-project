"""Product model, persistence, and filtering."""
from decimal import Decimal, InvalidOperation
from enum import Enum
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SAEnum


db = SQLAlchemy()


class Category(Enum):
    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable=False, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(SAEnum(Category), nullable=False, default=Category.UNKNOWN)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price) if self.price is not None else None,
            "available": self.available,
            "category": self.category.name if self.category else None,
        }

    def deserialize(self, data):
        if not isinstance(data, dict):
            abort(400, description="Expected a JSON object")
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            abort(400, description="Product name is required")
        self.name = name.strip()
        self.description = str(data.get("description") or "")
        try:
            price = Decimal(str(data.get("price")))
            if not price.is_finite() or price < 0:
                raise ValueError("Invalid price")
        except (InvalidOperation, ValueError, TypeError):
            abort(400, description="Invalid price")
        self.price = price
        available = data.get("available", True)
        if not isinstance(available, bool):
            abort(400, description="available must be a boolean")
        self.available = available
        raw_category = data.get("category", "UNKNOWN")
        try:
            self.category = raw_category if isinstance(raw_category, Category) else Category[str(raw_category).upper()]
        except KeyError:
            abort(400, description="Invalid category")
        return self

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        return cls.query.order_by(cls.id).all()

    @classmethod
    def find(cls, product_id):
        return db.session.get(cls, product_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available):
        return cls.query.filter(cls.available.is_(available))

    @staticmethod
    def init_db(app):
        init_db(app)


def init_db(app):
    with app.app_context():
        db.create_all()
