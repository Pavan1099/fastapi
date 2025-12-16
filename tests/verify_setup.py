import sys
import os

# Add parent directory to path so we can import from the main app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, engine
from models import Base, ProductCreate
import crud


def test_setup():
    print("1. Testing Database Connection...")
    try:
        connection = engine.connect()
        print("   ✅ Database connection successful!")
        connection.close()
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        return

    print("\n2. Testing API Router Configuration...")
    client = TestClient(app)
    response = client.get("/")
    if response.status_code == 200:
        print("   ✅ Root endpoint is reachable.")
    else:
        print(f"   ❌ Root endpoint failed with status {response.status_code}")

    response = client.get("/products")
    # It might be 200 (empty list) or 200 (list of products)
    if response.status_code == 200:
        print("   ✅ /products endpoint is reachable (Router is working).")
    else:
        print(f"   ❌ /products endpoint failed: {response.status_code}")

    print("\n3. Testing CRUD Operations (In-Memory Check)...")
    db = SessionLocal()
    try:
        # Create a dummy product
        test_product = ProductCreate(
            name="Test Widget",
            description="A temporary test widget",
            price=19.99,
            quantity=10,
        )
        created = crud.create_product(db, test_product)
        print(f"   ✅ Created product: ID {created.id}")

        # Read
        fetched = crud.get_product(db, created.id)
        assert fetched.name == "Test Widget"
        print("   ✅ Fetched product successfully.")

        # Delete (cleanup)
        crud.delete_product(db, created.id)
        print("   ✅ Deleted test product.")

    except Exception as e:
        print(f"   ❌ CRUD operations failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    test_setup()
