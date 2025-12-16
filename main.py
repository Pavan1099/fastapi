from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, get_db

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def greet():
    return "Hello World, welcome to my project"


@app.get("/products", response_model=List[models.Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.ProductDB).all()


@app.get("/products/{id}", response_model=models.Product)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(models.ProductDB).filter(models.ProductDB.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=models.Product)
def add_product(product: models.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{id}", response_model=models.Product)
def update_product(
    id: int, product: models.ProductCreate, db: Session = Depends(get_db)
):
    db_product = db.query(models.ProductDB).filter(models.ProductDB.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{id}", response_model=models.Product)
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.ProductDB).filter(models.ProductDB.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return db_product
