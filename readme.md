# Product Inventory Management System 🛍️

Welcome to the Product Inventory Management System! This application helps you track products, manage stock levels, and analyze inventory value through a beautiful, interactive dashboard.

## 🚀 Quick Start (Automated Setup)

We have included a "magic script" to get you up and running instantly on any new device (Mac/Linux).

1.  **Open Terminal** in the project folder (`fastapi/`).
2.  **Run the script**:
    ```bash
    ./setup_and_run.sh
    ```

**What the script does:**
*   Checks for Python 3.
*   Creates a virtual environment (`venv`) automatically.
*   Installs all required dependencies.
*   Launches the Streamlit App for you!

---

## 📖 Project Documentation

### 1. Project Overview
This project is a Product Inventory Management System that allows users to:
- View a dashboard of inventory metrics (Total Products, Stock Value, etc.).
- Browse a gallery of products.
- Manage inventory (Add, Update, Delete products).

The application is built using Python and leverages several powerful libraries:

#### Core Frameworks
- **FastAPI**: High-performance API framework (in `main.py` & `routers/`).
- **Streamlit**: Interactive Data App framework (in `streamlit_app.py`).

#### Data & Configuration
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic & Pydantic-Settings**: Data validation and configuration management.
- **Pandas**: Data manipulation for the dashboard.
- **SQLite**: Lightweight database (default).

#### Utilities
- **Uvicorn**: ASGI server to run FastAPI.
- **HTTPX**: Async HTTP client for testing.
- **Python-dotenv**: Environment variable management.

### 2. Architecture & Data Flow
The project uses a structured architecture separating concerns into Database, Models, Logic (CRUD), and Presentation (API & UI).

```
[ Database (SQLite) ] <--- [ SQLAlchemy ORM ] <--- [ CRUD Logic ] <--- [ FastAPI (API) ] OR [ Streamlit (UI) ]
```

**Key Characteristic**:
Unlike a traditional decoupled architecture where the Frontend talks to the Backend ONLY via HTTP requests, this specific implementation is "Self-Contained".
- The **Streamlit App** imports the database logic (`crud.py`) directly to perform operations. This makes it fast and easy to deploy as a standalone unit without needing a separate running API server for the UI to work.
- The **FastAPI App** (`main.py`) exposes the SAME logic over HTTP, allowing external systems (like a mobile app or another server) to interact with your inventory data programmatically.

### 3. File-by-File Explanation

#### A. `config.py` (Configuration)
- **Purpose**: Centralizes application settings (Database URL, Debug Mode) using `pydantic-settings`.
- **Key Code**: `Settings` class that reads from environment variables.

#### B. `database.py` (The Foundation)
- **Purpose**: Sets up the connection to the Database using settings from `config.py`.
- **Key Code**:
  - `create_engine`: Creates the connection engine.
  - `SessionLocal`: A factory to create database sessions (transactions).
  - `Base`: The class that all database models will inherit from.

#### C. `models.py` (The Data Structure)
- **Purpose**: Defines what a "Product" looks like in Python and the Database.
- **Components**:
  - `ProductDB` (SQLAlchemy): Maps Python objects to the SQL table `products`. Columns: `id`, `name`, `description`, `price`, `quantity`.
  - `ProductBase / ProductCreate / Product` (Pydantic): Defines the shape of data for validation (used by FastAPI to validate incoming JSON and by code to ensure type safety).

#### D. `crud.py` (The Logic / Operations)
- **Purpose**: Contains the "Create, Read, Update, Delete" (CRUD) functions. It isolates the logic so it can be re-used by both FastAPI and Streamlit.
- **Functions**:
  - `get_products`: Fetches a list of items.
  - `create_product`: Adds a new item to the DB.
  - `update_product`: Modifies an existing item.
  - `delete_product`: Removes an item.

#### E. `routers/products.py` (API Routes)
- **Purpose**: Defines the specific API endpoints for Product operations, keeping `main.py` clean.
- **Components**: `APIRouter` containing GET/POST/PUT/DELETE logic.

#### F. `main.py` (The API Entrypoint)
- **Purpose**: Initializes the FastAPI app and includes the routers.
- **Endpoints**:
  - `GET /products`: Returns all products as JSON.
  - `POST /products`: Accepts JSON data to create a product.
  - `PUT /products/{id}`: Updates a product.
  - `DELETE /products/{id}`: Deletes a product.
- **How it works**: When a request comes in (e.g., from a mobile app), it opens a DB session, calls a function from `crud.py`, and returns the result.

#### G. `streamlit_app.py` (The User Interface)
- **Purpose**: A web dashboard for humans to interact with the system.
- **How it works**:
  - **Direct Access**: Instead of calling the API URLs (like `http://localhost:8000/products`), it imports `crud` and `SessionLocal` directly.
  - **State Management**: Uses `st.rerun()` to refresh the page after data changes (like adding a product).
  - **Components**:
    - **Dashboard**: Uses Pandas to calculate metrics (Sum of prices, averages).
    - **Gallery**: Displays products in a grid layout.
    - **Manage**: Forms to Add/Edit/Delete utilizing `crud` functions.

### 4. Step-by-Step Flow Examples

#### Scenario 1: Adding a Product (via Streamlit)
1.  **User Action**: Goes to "Manage Inventory" tab, fills in Name/Price/Qty, clicks "Add Product".
2.  **Code Execution**:
    - `streamlit_app.py` creates a `ProductCreate` object.
    - It opens a database session: `with SessionLocal() as db:`.
    - It calls `crud.create_product(db, new_data)`.
    - `crud.create_product` converts the data to a `ProductDB` SQL object, adds it to the session, and commits (saves) it to `inventory.db`.
3.  **Result**: Streamlit shows a success message and balloons.

#### Scenario 2: Viewing Products (via API)
1.  **User Action**: A developer sends a GET request to `http://localhost:8000/products`.
2.  **Code Execution**:
    - `main.py` receives the request.
    - The `get_products` function is triggered.
    - Dependency injection `Depends(get_db)` provides a database session.
    - It calls `crud.get_products(db)`.
    - `crud.py` asks SQLAlchemy to run `SELECT * FROM products`.
3.  **Result**: The list of products is converted to JSON and sent back to the requester.

### 5. Summary
This project demonstrates a clean "Layered Architecture":
1.  **Data Layer**: `database.py` & `models.py`
2.  **Logic Layer**: `crud.py`
3.  **Interface Layer**: `main.py` (for machines) and `streamlit_app.py` (for humans).
