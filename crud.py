from sqlalchemy.orm import Session
from typing import List, Optional
import models


def get_product(db: Session, product_id: int) -> Optional[models.ProductDB]:
    """
    Fetch a single product by its ID.

    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to retrieve.

    Returns:
        Optional[models.ProductDB]: The product object if found, else None.
    """
    return db.query(models.ProductDB).filter(models.ProductDB.id == product_id).first()


def get_product_by_name(db: Session, name: str) -> Optional[models.ProductDB]:
    """
    Fetch a single product by its name.

    Args:
        db (Session): The database session.
        name (str): The name of the product to retrieve.

    Returns:
        Optional[models.ProductDB]: The product object if found, else None.
    """
    return db.query(models.ProductDB).filter(models.ProductDB.name == name).first()


def get_products(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.ProductDB]:
    """
    Retrieve a list of products with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of ProductDB objects
    """
    return db.query(models.ProductDB).offset(skip).limit(limit).all()


def create_product(db: Session, product: models.ProductCreate) -> models.ProductDB:
    """
    Create a new product in the database.

    Args:
        db: Database session
        product: Product creation schema

    Returns:
        The created ProductDB object
    """
    db_product = models.ProductDB(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
    db: Session, product_id: int, product_data: dict
) -> Optional[models.ProductDB]:
    """
    Update an existing product.

    Args:
        db: Database session
        product_id: ID of the product to update
        product_data: Dictionary containing fields to update

    Returns:
        Updated ProductDB object if found, None otherwise
    """
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> Optional[models.ProductDB]:
    """
    Delete a product from the database.

    Args:
        db: Database session
        product_id: ID of the product to delete

    Returns:
        The deleted ProductDB object if found, None otherwise
    """
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
