from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return "Hello World, welcome to my project"

products = [
    Product(id=1, name="Product 1", description="Description 1", price=10.99, quantity=10),
    Product(id=2, name="Product 2", description="Description 2", price=19.99, quantity=20),
    Product(id=3, name="Product 3", description="Description 3", price=29.99, quantity=30)
]

@app.get("/products")
def get_products():
    return products

@app.get("/products/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product):
    for prod in products:
        if prod.id == id:
            prod.name = product.name
            prod.description = product.description
            prod.price = product.price
            prod.quantity = product.quantity
            return product

@app.delete("/products/{id}")
def delete_product(id: int):
    for prod in products:
        if prod.id == id:
            products.remove(prod)
            return prod