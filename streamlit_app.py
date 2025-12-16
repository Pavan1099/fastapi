import streamlit as st
import requests
import pandas as pd

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Product Manager",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown(
    """
<style>
    /* Global Styles */
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Metrics Styling */
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    
    /* Force text colors for metrics to match the white background */
    div[data-testid="stMetric"] label {
        color: #666666 !important; /* Label Color */
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #2c3e50 !important; /* Value Color */
    }
    
    /* Product Card Styling */
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: translateY(-5px);
    }
    .product-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .product-price {
        font-size: 1.5em;
        color: #27ae60;
        font-weight: bold;
    }
    .product-meta {
        color: #7f8c8d;
        font-size: 0.9em;
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- Helper Functions ---
def fetch_products():
    try:
        response = requests.get(f"{API_URL}/products")
        if response.status_code == 200:
            return response.json()
        else:
            st.toast("Failed to fetch products", icon="❌")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
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
                "Total Stock Value", f"${(df['price'] * df['quantity']).sum():.2f}"
            )
        with col3:
            st.metric("Avg. Price", f"${df['price'].mean():.2f}")

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

    if products:
        cols = st.columns(3)  # Grid layout
        for i, product in enumerate(products):
            with cols[i % 3]:
                st.markdown(
                    f"""
                <div class="product-card">
                    <div class="product-title">{product['name']}</div>
                    <p>{product['description']}</p>
                    <div class="product-price">${product['price']:.2f}</div>
                    <div class="product-meta">Stock: {product['quantity']} units</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
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
                price = st.number_input("Price ($)", min_value=0.0, format="%.2f")
            with col2:
                quantity = st.number_input("Quantity", min_value=0, step=1)
                description = st.text_input("Short Description")

            submitted = st.form_submit_button("Add Product", use_container_width=True)
            if submitted:
                new_product = {
                    "id": (
                        len(products) + 100 if products else 1
                    ),  # Improved ID logic needed for real apps
                    "name": name,
                    "description": description,
                    "price": price,
                    "quantity": quantity,
                }
                res = requests.post(f"{API_URL}/products", json=new_product)
                if res.status_code == 200:
                    st.success(f"Added **{name}** successfully!")
                    st.balloons()
                    # No rerun here to let the success message show, user can navigate or wait
                else:
                    st.error("Failed to add product.")

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
                        "id": selected_p["id"],
                        "name": u_name,
                        "description": u_desc,
                        "price": u_price,
                        "quantity": u_qty,
                    }
                    res = requests.put(
                        f"{API_URL}/products/{selected_p['id']}", json=updated_data
                    )
                    if res.status_code == 200:
                        st.success("Updated successfully!")
                        st.rerun()
                    else:
                        st.error("Update failed.")
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
                res = requests.delete(f"{API_URL}/products/{del_p['id']}")
                if res.status_code == 200:
                    st.success("Deleted successfully!")
                    st.rerun()
                else:
                    st.error("Deletion failed.")
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
