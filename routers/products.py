from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import crud
from database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[models.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve products with pagination.
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{id}", response_model=models.Product)
def read_product(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific product by ID.
    """
    product = crud.get_product(db, product_id=id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("/", response_model=models.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: models.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    return crud.create_product(db=db, product=product)


@router.put("/{id}", response_model=models.Product)
def update_product(
    id: int, product: models.ProductCreate, db: Session = Depends(get_db)
):
    """
    Update an existing product.
    """
    # model_dump() is the Pydantic v2 method (equivalent to dict() in v1)
    db_product = crud.update_product(
        db=db, product_id=id, product_data=product.model_dump()
    )
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_product


@router.delete("/{id}", response_model=models.Product)
def delete_product(id: int, db: Session = Depends(get_db)):
    """
    Delete a product.
    """
    db_product = crud.delete_product(db=db, product_id=id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_product
