import streamlit as st
import pandas as pd

# FastAPI backend URL
import models
import crud
from database import SessionLocal

st.set_page_config(
    page_title="Product Manager",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
# --- Custom CSS ---
st.markdown(
    """
<style>
    /* Global Styles */
    .stApp {
        background-color: #232b6e; /* Lighter Blue for Main Content */
        color: #FFD700; /* Default Text: Gold */
    }
    
    /* UNIVERSAL TEXT OVERRIDES */
    h1, h2, h3, h4, h5, h6, p, li, span, div {
        color: #FFD700; /* Try to default everything to Gold */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Headers specific override to ensure importance */
    h1, h2, h3 {
        color: #FFD700 !important; 
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #151B54; /* Deep Navy Blue */
    }
    [data-testid="stSidebar"] * {
        color: #FFD700 !important; /* Sidebar Text Gold */
    }
    
    /* TOP HEADER */
    header[data-testid="stHeader"] {
        background-color: #FFD700 !important; /* Gold Header */
    }
    
    /* Inject Title Text into Header */
    header[data-testid="stHeader"]::after {
        content: "Next week shopping tool";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #151B54; /* Dark Blue Text */
        font-weight: bold;
        font-size: 1.5rem;
        font-family: 'Helvetica Neue', sans-serif;
        z-index: 1; /* Ensure it's above background but below controls if they have higher z-index */
    }
    /* Controls in header (Hamburger etc) need to be Blue to contrast with Gold */
    header[data-testid="stHeader"] button, header[data-testid="stHeader"] svg {
        color: #151B54 !important;
        fill: #151B54 !important;
    }
    
    /* PRODUCT CARDS (Expanded Containers) */
    /* Target the container with border */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
        background-color: #151B54 !important; /* Blue Background */
        border: 2px solid #FFD700 !important; /* Gold Border */
        color: #FFD700 !important; /* Gold Text */
    }
    
    /* Text INSIDE the card */
    div[data-testid="stContainer"] p, 
    div[data-testid="stContainer"] div, 
    div[data-testid="stContainer"] span, 
    div[data-testid="stContainer"] h1,
    div[data-testid="stContainer"] h2,
    div[data-testid="stContainer"] h3 {
        color: #FFD700 !important;
    }

    /* METRICS (Inside Cards or Dashboard) */
    div[data-testid="stMetric"] {
        background-color: #151B54 !important;
        border: 1px solid #FFD700 !important;
        color: #FFD700 !important;
    }
    div[data-testid="stMetric"] label {
        color: #E0E0E0 !important; /* Slightly lighter for label distinction */
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #FFD700 !important;
    }
    
    /* INPUTS (Text, Number, Date, Select) */
    /* We want Blue text on White background for inputs to ensure they look like standard inputs but match theme */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        color: #151B54 !important;
        background-color: #FFFFFF !important;
        border: 1px solid #FFD700 !important;
    }
    /* Labels for inputs */
    .stTextInput label, .stNumberInput label, .stTextArea label, .stSelectbox label {
        color: #FFD700 !important;
    }
    
    /* DATAFRAME / TABLES */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border: 2px solid #FFD700;
        padding: 5px;
        border-radius: 5px;
    }
    div[data-testid="stDataFrame"] * {
        color: #151B54 !important; /* Dark text for table readability */
    }
    
    /* DROPDOWNS & MENUS & POPOVERS */
    div[role="listbox"] li {
        background-color: #151B54 !important;
        color: #FFD700 !important;
    }
    div[role="listbox"] li:hover {
        background-color: #232b6e !important;
    }
    
    /* The 'Three Dots' menu and other popups */
    div[role="menu"], div[data-baseweb="popover"] {
        background-color: #151B54 !important; 
    }
    div[role="menu"] div, div[role="menu"] li, div[role="menu"] span,
    div[data-baseweb="popover"] div, div[data-baseweb="popover"] li, div[data-baseweb="popover"] span {
        color: #FFD700 !important; /* Gold text in menus */
        background-color: #151B54 !important; /* Blue bg */
    }
    
    /* MODALS */
    div[role="dialog"] {
        background-color: #151B54 !important;
        color: #FFD700 !important;
        border: 2px solid #FFD700;
    }
    div[role="dialog"] * {
        color: #FFD700 !important;
    }
    
    /* TABS */
    button[data-baseweb="tab"] {
        color: #E0E0E0 !important; /* Unselected Tab */
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFD700 !important; /* Selected Tab */
        border-bottom-color: #FFD700 !important;
    }
    
    /* BUTTONS */
    div.stButton > button[kind="primary"] {
        background-color: #FFD700 !important;
        color: #151B54 !important;
        border: none;
    }
    div.stButton > button[kind="secondary"] {
        background-color: transparent !important;
        border: 1px solid #FFD700 !important;
        color: #FFD700 !important;
    }
    
    /* Custom Button-Card */
    div.stButton > button {
        background-color: #151B54;
        color: #FFD700;
        border: 1px solid #FFD700;
    }
    div.stButton > button:hover {
        background-color: #FFD700;
        color: #151B54;
    }

    /* SIDEBAR TOGGLE (Aggressive) */
    button[kind="header"] {
        color: #151B54 !important; 
        background-color: transparent !important;
    }
    button[kind="header"] svg {
        fill: #151B54 !important;
    }
    [data-testid="stSidebar"] button[kind="header"] {
        color: #FFD700 !important;
    }
    [data-testid="stSidebar"] button[kind="header"] svg {
        fill: #FFD700 !important;
    }
    [data-testid="stSidebarCollapsedControl"] button, [data-testid="stSidebarCollapsedControl"] svg {
        color: #151B54 !important;
        fill: #151B54 !important;
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        color: #FFD700 !important;
        background-color: #151B54 !important;
        border: 1px solid #FFD700;
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #151B54 !important;
        color: #FFD700 !important;
        border: 1px solid #FFD700;
    }
    
    /* Divider */
    hr {
        border-color: #FFD700;
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- Helper Functions ---
def fetch_products():
    try:
        with SessionLocal() as db:
            products = crud.get_products(db)
            # Use Pydantic to serialize SQLAlchemy objects to clean dictionaries
            # This avoids including internal SQLAlchemy state (like _sa_instance_state)
            return [models.Product.model_validate(p).model_dump() for p in products]
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return []


# --- Sidebar Navigation ---
st.sidebar.title("🛍️ Navigation")
st.sidebar.markdown("### My first API project successfully implemented")
page = st.sidebar.radio("Go to", ["Dashboard", "Product Gallery", "Manage Inventory"])

products = fetch_products()

# --- Page: Dashboard ---
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Overview of your inventory performance.")

    if products:
        df = pd.DataFrame(products)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Products", len(products))
        with col2:
            st.metric(
                "Total Stock Value", f"₹{(df['price'] * df['quantity']).sum():.2f}"
            )
        with col3:
            st.metric("Avg. Price", f"₹{df['price'].mean():.2f}")

        st.divider()
        st.subheader("Quick Inventory View")
        st.dataframe(
            df[["name", "price", "quantity", "description"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No products available to generate analytics.")

# --- Page: Product Gallery ---
elif page == "Product Gallery":
    st.title("🖼️ Product Gallery")
    st.markdown("Browse your product catalog.")

    # Search Bar
    search_term = st.text_input(
        "🔍 Search Products",
        placeholder="Type to search by name or description...",
        key="gallery_search",
    )

    # Filter Logic
    if search_term:
        filtered_products = [
            p
            for p in products
            if search_term.lower() in p["name"].lower()
            or search_term.lower() in p["description"].lower()
        ]
    else:
        filtered_products = products

    if filtered_products:
        cols = st.columns(3)
        for i, product in enumerate(filtered_products):
            with cols[i % 3]:
                # Selection State Logic
                is_selected = st.session_state.get("selected_product") == product["id"]

                if is_selected:
                    # EXPANDED STATE (Detailed Card)
                    with st.container(border=True):
                        # Header with Close Button
                        c_head, c_close = st.columns([0.8, 0.2])
                        with c_head:
                            st.subheader(product["name"])
                            st.caption(f"ID: {product['id']}")
                        with c_close:
                            if st.button(
                                "❌", key=f"close_{product['id']}", help="Close details"
                            ):
                                st.session_state["selected_product"] = None
                                st.rerun()

                        # Details
                        st.write(product["description"])
                        st.divider()

                        # Metrics in Card
                        c1, c2 = st.columns(2)
                        c1.metric("Price", f"₹{product['price']:.2f}")
                        c2.metric("Stock", product["quantity"])

                        st.divider()

                        # Sell Controls
                        if product["quantity"] > 0:
                            sell_qty = st.number_input(
                                "Sell Qty",
                                min_value=1,
                                max_value=product["quantity"],
                                key=f"sell_{product['id']}",
                            )

                            if st.button(
                                "Confirm Sale 💸",
                                key=f"btn_{product['id']}",
                                use_container_width=True,
                                type="primary",
                            ):
                                # Calculate new data
                                new_quantity = product["quantity"] - sell_qty
                                updated_product = product.copy()
                                updated_product["quantity"] = new_quantity

                                try:
                                    with SessionLocal() as db:
                                        crud.update_product(
                                            db, product["id"], updated_product
                                        )
                                    st.toast(
                                        f"Sold {sell_qty} of {product['name']}!",
                                        icon="🎉",
                                    )
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to update stock: {e}")
                        else:
                            st.error("Out of Stock")

                else:
                    # COLLAPSED STATE (Button Card)
                    # We use a button to act as the "Product Card"
                    # We format the label to show key info
                    label = f"{product['name']}\n₹{product['price']:.2f} | Stock: {product['quantity']}"

                    if st.button(
                        label,
                        key=f"select_{product['id']}",
                        use_container_width=True,
                        help="Click to view details and sell",
                    ):
                        st.session_state["selected_product"] = product["id"]
                        st.rerun()
    else:
        st.info("No products found in the gallery.")

# --- Page: Manage Inventory ---
elif page == "Manage Inventory":
    st.title("🛠️ Manage Inventory")

    tab1, tab2, tab3 = st.tabs(["➕ Add Product", "✏️ Update", "🗑️ Delete"])

    # Tab 1: Add Product
    with tab1:
        st.header("Add New Item")
        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name")
                price = st.number_input("Price (₹)", min_value=0.0, format="%.2f")
            with col2:
                quantity = st.number_input("Quantity", min_value=0, step=1)
                description = st.text_input("Short Description")

            submitted = st.form_submit_button("Add Product", use_container_width=True)
            if submitted:
                if not name.strip():
                    st.error("❌ Product Name is required.")
                elif price <= 0:
                    st.error("❌ Price must be greater than $0.")
                elif quantity < 0:
                    # Though min_value handles this, good to be explicit safely
                    st.error("❌ Quantity cannot be negative.")
                else:
                    # DB handles ID generation
                    new_product_data = models.ProductCreate(
                        name=name,
                        description=description,
                        price=price,
                        quantity=quantity,
                    )
                    try:
                        with SessionLocal() as db:
                            # Check for duplicates before trying (optional optimization, but DB constraint is the source of truth)
                            existing = crud.get_product_by_name(
                                db, name
                            )  # We need to implement this or generic catch
                            if existing:
                                st.error(f"❌ Product '{name}' already exists!")
                            else:
                                crud.create_product(db, new_product_data)
                                st.success(f"Added **{name}** successfully!")
                                st.balloons()
                    except Exception as e:
                        if "unique constraint" in str(e).lower():
                            st.error(
                                f"❌ Error: A product with the name '{name}' already exists."
                            )
                        else:
                            st.error(f"Failed to add product: {e}")

    # Tab 2: Update Product
    with tab2:
        st.header("Edit Item Details")
        if products:
            product_options = {f"{p['name']} (ID: {p['id']})": p for p in products}
            selected_name = st.selectbox("Select Product", list(product_options.keys()))
            selected_p = product_options[selected_name]

            with st.form("update_product_form"):
                u_name = st.text_input("Name", value=selected_p["name"])
                u_desc = st.text_area("Description", value=selected_p["description"])
                c1, c2 = st.columns(2)
                u_price = c1.number_input(
                    "Price", min_value=0.0, format="%.2f", value=selected_p["price"]
                )
                u_qty = c2.number_input(
                    "Quantity", min_value=0, step=1, value=selected_p["quantity"]
                )

                if st.form_submit_button("Save Changes", use_container_width=True):
                    updated_data = {
                        "name": u_name,
                        "description": u_desc,
                        "price": u_price,
                        "quantity": u_qty,
                    }
                    try:
                        with SessionLocal() as db:
                            crud.update_product(db, selected_p["id"], updated_data)
                        st.success("Updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Update failed: {e}")
        else:
            st.info("No products to update.")

    # Tab 3: Delete Product
    with tab3:
        st.header("Remove Item")
        if products:
            del_options = {f"{p['name']} (ID: {p['id']})": p for p in products}
            del_name = st.selectbox(
                "Select Product to Delete", list(del_options.keys()), key="del_select"
            )
            del_p = del_options[del_name]

            st.warning(
                f"Are you sure you want to delete **{del_p['name']}**? This action cannot be undone."
            )
            if st.button("🗑️ Delete Permanently", type="primary"):
                try:
                    with SessionLocal() as db:
                        crud.delete_product(db, del_p["id"])
                    st.success("Deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Deletion failed: {e}")
        else:
            st.info("No products to delete.")

# --- Footer ---
st.divider()
with st.expander("🔧 Technologies Used"):
    st.markdown(
        """
    *   **Frontend**: [Streamlit](https://streamlit.io/) 🎈
    *   **Backend**: [FastAPI](https://fastapi.tiangolo.com/) ⚡
    *   **Data Handling**: [Pandas](https://pandas.pydata.org/) 🐼
    *   **API Communication**: [Requests](https://requests.readthedocs.io/) 🔌
    *   **Language**: [Python](https://www.python.org/) 🐍
    """
    )
