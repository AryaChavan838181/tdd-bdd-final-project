"""Task 4: Product REST endpoints and admin UI."""
from flask import abort, jsonify, request, url_for, render_template
from service import app
from service.models import Product, Category
from service.common import status


def check_content_type(content_type):
    if request.mimetype != content_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
              description="Content-Type must be application/json")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify(message="OK"), status.HTTP_200_OK


@app.route("/products", methods=["POST"])
def create_products():
    """Create a Product using JSON, responding with 201 and Location."""
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    location_url = url_for("get_products", product_id=product.id, _external=True)
    return jsonify(product.serialize()), status.HTTP_201_CREATED, {"Location": location_url}


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Read a Product by ID"""
    app.logger.info("Request to Read a Product with id [%s]", product_id)
    product = Product.find(product_id)
    if product is None:
        abort(status.HTTP_404_NOT_FOUND, description="Product not found")
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Update an existing Product"""
    app.logger.info("Request to Update Product %s", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if product is None:
        abort(status.HTTP_404_NOT_FOUND, description="Product not found")
    product.deserialize(request.get_json())
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Delete a Product"""
    app.logger.info("Request to Delete Product %s", product_id)
    product = Product.find(product_id)
    if product is not None:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT



@app.route("/products", methods=["GET"])
def list_products():
    """List Products with optional filters"""
    app.logger.info("Request to List Products")
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        try:
            category_enum = Category[category.upper()]
        except KeyError:
            abort(status.HTTP_400_BAD_REQUEST, description="Invalid category")
        products = Product.find_by_category(category_enum)
    elif available is not None:
        if available.lower() not in ("true", "false"):
            abort(
                status.HTTP_400_BAD_REQUEST,
                description="Invalid availability value"
            )
        is_available = available.lower() == "true"
        products = Product.find_by_availability(is_available)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK
