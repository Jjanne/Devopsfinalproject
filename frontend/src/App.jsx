
// frontend/src/App.jsx
import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const BACKEND = "https://devopsgroupproject-api-jjanne-amawf0a8fffcame0.spaincentral-01.azurewebsites.net";

const PAGES = {
  AUTH: "auth",
  PRODUCTS: "products",
  CART: "cart",
  ORDERS: "orders",
};

function prettifyCategory(idOrName) {
  return String(idOrName)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (ch) => ch.toUpperCase());
}

function formatPrice(value) {
  if (typeof value === "number") return `€${value.toFixed(2)}`;
  const n = Number(value || 0);
  return `€${n.toFixed(2)}`;
}

function App() {
  // user + auth
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState(""); // UI-only, backend ignores
  const [user, setUser] = useState(null);
  const [savedUser, setSavedUser] = useState(null);
  const [cart, setCart] = useState(null);

  // shop data
  const [categories, setCategories] = useState([]); // [{id,label,backend}]
  const [selectedCategoryId, setSelectedCategoryId] = useState(null);
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);

  // UI state
  const [currentPage, setCurrentPage] = useState(PAGES.AUTH);
  const [errorMsg, setErrorMsg] = useState("");
  const [loadingCategories, setLoadingCategories] = useState(false);
  const [loadingProducts, setLoadingProducts] = useState(false);
  const [creatingUser, setCreatingUser] = useState(false);
  const [creatingOrder, setCreatingOrder] = useState(false);
  const [loadingOrders, setLoadingOrders] = useState(false);
  const [addingToCartId, setAddingToCartId] = useState(null);

  // ---------------------------------------------------
  // Initial load: saved user + categories
  // ---------------------------------------------------
  useEffect(() => {
    // load saved user from localStorage
    try {
      const raw = localStorage.getItem("devops-shop-user");
      if (raw) {
        const parsed = JSON.parse(raw);
        setSavedUser(parsed);
      }
    } catch {
      // ignore
    }

    // load categories once
    const fetchCategories = async () => {
      setLoadingCategories(true);
      try {
        const res = await axios.get(`${BACKEND}/products/categories`);
        const raw = res.data || [];

        // normalise into {id,label,backend}
        const normalised = raw.map((c) => {
          // CASE 1: backend returns simple strings
          if (typeof c === "string") {
            let id = c;
            let backend = c;

            if (c.toLowerCase() === "men's clothing") {
              id = "mens_clothing";
              backend = "men's clothing";
            } else if (c.toLowerCase() === "women's clothing") {
              id = "womens_clothing";
              backend = "women's clothing";
            }

            return {
              id,
              label: prettifyCategory(
                id === "womens_clothing" ? "women's clothing" : c
              ),
              backend,
            };
          }

          // CASE 2: backend returns objects, e.g.
          // {id: "mens_clothing", name: "men's clothing"}
          const baseName = c.name || c.category || c.id;
          let id = c.id;

          if (!id) {
            // create a slug if there is no explicit id
            id = String(baseName)
              .toLowerCase()
              .replace(/[^a-z0-9]+/g, "_")
              .replace(/^_|_$/g, "");
          }

          // --- THIS IS THE IMPORTANT FIX ---
          let backend = baseName;
          if (id === "mens_clothing") {
            backend = "men's clothing";
          } else if (id === "womens_clothing") {
            backend = "women's clothing";
          }
          // ----------------------------------

          const labelSource =
            id === "womens_clothing" ? "women's clothing" : baseName;

          return {
            id,
            label: prettifyCategory(labelSource),
            backend,
          };
        });

        setCategories(normalised);
        setErrorMsg("");
      } catch (err) {
        console.error(err);
        setErrorMsg("Failed to load categories");
      } finally {
        setLoadingCategories(false);
      }
    };

    fetchCategories();
  }, []);

  const cartItemCount =
    cart?.items?.reduce((sum, item) => sum + (item.quantity || 0), 0) || 0;

  // ---------------------------------------------------
  // Backend helpers
  // ---------------------------------------------------
  const ensureCartForUser = async (userObj) => {
    try {
      const res = await axios.post(`${BACKEND}/cart/${userObj.id}`);
      setCart(res.data);
      setErrorMsg("");
    } catch (err) {
      console.error(err);
      setErrorMsg("Failed to load cart for this user.");
    }
  };

  const refreshOrdersForUser = async (userObj) => {
    try {
      setLoadingOrders(true);
      const res = await axios.get(`${BACKEND}/orders/user/${userObj.id}`);
      setOrders(res.data || []);
      setErrorMsg("");
    } catch (err) {
      console.error(err);
      setErrorMsg("Failed to load orders.");
    } finally {
      setLoadingOrders(false);
    }
  };

  // ---------------------------------------------------
  // Auth
  // ---------------------------------------------------
  const handleCreateUser = async () => {
    if (!email) {
      setErrorMsg("Please enter an email.");
      return;
    }

    try {
      setCreatingUser(true);
      setErrorMsg("");

      const res = await axios.post(`${BACKEND}/users/`, {
        email,
        password,
      });

      const createdUser = res.data;
      setUser(createdUser);
      setPassword("");

      localStorage.setItem("devops-shop-user", JSON.stringify(createdUser));
      setSavedUser(createdUser);

      await ensureCartForUser(createdUser);
      await refreshOrdersForUser(createdUser);

      setCurrentPage(PAGES.PRODUCTS);
    } catch (err) {
      console.error("Create user failed:", err);
      const msg =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Failed to create user";
      setErrorMsg(msg);
    } finally {
      setCreatingUser(false);
    }
  };

  const handleLoginSavedUser = async () => {
    if (!savedUser) return;
    setErrorMsg("");
    setUser(savedUser);
    await ensureCartForUser(savedUser);
    await refreshOrdersForUser(savedUser);
    setCurrentPage(PAGES.PRODUCTS);
  };

  const handleLogout = () => {
    setUser(null);
    setCart(null);
    setOrders([]);
    setSelectedCategoryId(null);
    setProducts([]);
    setErrorMsg("");
    setCurrentPage(PAGES.AUTH);
  };

  // ---------------------------------------------------
  // Products
  // ---------------------------------------------------
  const loadProductsInCategory = async (categoryObj) => {
    if (!categoryObj) return;

    setSelectedCategoryId(categoryObj.id);
    setProducts([]);
    setLoadingProducts(true);

    try {
      const backendCategory = categoryObj.backend;

      const res = await axios.get(
        `${BACKEND}/products/category/${encodeURIComponent(backendCategory)}`
      );
      const data = res.data;
      const list = Array.isArray(data) ? data : data.products || [];
      setProducts(list);
      setErrorMsg("");
    } catch (err) {
      console.error(err);
      setErrorMsg("Failed to load products");
    } finally {
      setLoadingProducts(false);
    }
  };

  const addToCart = async (productId) => {
    if (!cart) {
      setErrorMsg("Create a user first so we can create a cart.");
      return;
    }

    try {
      setAddingToCartId(productId);
      const res = await axios.post(`${BACKEND}/cart/${cart.id}/items`, {
        product_id: productId,
        quantity: 1,
      });
      setCart(res.data);
      setErrorMsg("");
    } catch (err) {
      console.error(err);
      setErrorMsg("Failed to add item to cart");
    } finally {
      setAddingToCartId(null);
    }
  };

  // ---------------------------------------------------
  // Orders
  // ---------------------------------------------------
  const createOrder = async () => {
    if (!user) {
      setErrorMsg("Create or log in as a user first.");
      return;
    }

    try {
      setCreatingOrder(true);
      const res = await axios.post(`${BACKEND}/orders/${user.id}`);
      alert("Order created with total: " + formatPrice(res.data.total));
      setErrorMsg("");
      await refreshOrdersForUser(user);
      await ensureCartForUser(user); // cart becomes empty
    } catch (err) {
      console.error(err);
      setErrorMsg("Failed to create order");
    } finally {
      setCreatingOrder(false);
    }
  };

  // ---------------------------------------------------
  // Render helpers
  // ---------------------------------------------------
  const renderCart = () => {
    if (!cart) return <p className="muted">No cart yet. Create a user first.</p>;
    if (!cart.items || cart.items.length === 0)
      return <p className="muted">Cart is empty.</p>;

    return (
      <ul className="cart-list">
        {cart.items.map((item) => (
          <li
            key={item.id ?? `${item.product_id}-${item.quantity}`}
            className="cart-item"
          >
            <span>Product ID: {item.product_id}</span>
            <span>Qty: {item.quantity}</span>
          </li>
        ))}
      </ul>
    );
  };

  const cartItemCountDisplay = () =>
    cartItemCount === 1 ? "1 item" : `${cartItemCount} items`;

  const UserBadge = () =>
    user ? (
      <div className="user-badge">
        <span className="user-avatar">
          {user.email[0]?.toUpperCase() || "U"}
        </span>
        <div>
          <div className="user-email">{user.email}</div>
          <div className="user-meta">Cart: {cartItemCountDisplay()}</div>
        </div>
      </div>
    ) : null;

  const NavTabs = () =>
    user ? (
      <nav className="nav-tabs">
        <button
          className={
            "nav-tab" + (currentPage === PAGES.PRODUCTS ? " nav-tab-active" : "")
          }
          onClick={() => setCurrentPage(PAGES.PRODUCTS)}
        >
          Products
        </button>
        <button
          className={
            "nav-tab" + (currentPage === PAGES.CART ? " nav-tab-active" : "")
          }
          onClick={() => setCurrentPage(PAGES.CART)}
        >
          Cart
        </button>
        <button
          className={
            "nav-tab" + (currentPage === PAGES.ORDERS ? " nav-tab-active" : "")
          }
          onClick={() => setCurrentPage(PAGES.ORDERS)}
        >
          Orders
        </button>
      </nav>
    ) : null;

  // -------------- PAGE COMPONENTS --------------------

  const AuthPage = () => (
    <div className="page-center">
      <section className="card card-wide">
        <h2 className="card-title">Welcome</h2>
        <p className="muted">
          Create a demo user to start playing with the shop. We’ll remember it
          in this browser so you can log in again easily.
        </p>

        <div className="form-row auth-row">
          <input
            className="input"
            placeholder="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            className="input"
            placeholder="password (not stored)"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            className="btn primary"
            onClick={handleCreateUser}
            disabled={creatingUser}
          >
            {creatingUser ? "Creating…" : "Create user + cart"}
          </button>
        </div>

        {savedUser && (
          <div className="saved-user-row">
            <span className="muted">Or log in with your saved user:</span>
            <button className="btn ghost" onClick={handleLoginSavedUser}>
              Log in as <strong>{savedUser.email}</strong>
            </button>
          </div>
        )}
      </section>
    </div>
  );

  const ProductsPage = () => (
    <section className="card products-card">
      <h2 className="card-title">Products</h2>

      <div className="section-block">
        <h3 className="section-label">Categories</h3>
        {loadingCategories ? (
          <p className="muted">Loading categories…</p>
        ) : categories.length === 0 ? (
          <p className="muted">No categories found.</p>
        ) : (
          <div className="chip-row">
            {categories.map((c) => (
              <button
                key={c.id}
                className={
                  "chip" +
                  (selectedCategoryId === c.id ? " chip-active" : "")
                }
                onClick={() => loadProductsInCategory(c)}
              >
                {c.label}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="section-block">
        <h3 className="section-label">Products</h3>
        {loadingProducts ? (
          <p className="muted">Loading products…</p>
        ) : products.length === 0 ? (
          <p className="muted">Select a category to see products.</p>
        ) : (
          <div className="product-grid">
            {products.map((p) => (
              <div key={p.id} className="product-card">
                {/* NEW: product image */}
                {p.image && (
                  <div className="product-image-wrapper">
                    <img
                      src={p.image}
                      alt={p.title}
                      className="product-image"
                    />
                  </div>
                )}

                <div className="product-header">
                  <div className="product-title">{p.title}</div>
                  <div className="product-price">{formatPrice(p.price)}</div>
                </div>
                {p.description && (
                  <p className="product-description">
                    {p.description.length > 110
                      ? p.description.slice(0, 110) + "…"
                      : p.description}
                  </p>
                )}
                <button
                  className="btn secondary"
                  onClick={() => addToCart(p.id)}
                  disabled={addingToCartId === p.id}
                >
                  {addingToCartId === p.id ? "Adding…" : "Add to cart"}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );

  const CartPage = () => (
    <section className="card">
      <h2 className="card-title">Cart</h2>
      {renderCart()}
    </section>
  );

  const OrdersPage = () => (
    <section className="card">
      <h2 className="card-title">Orders</h2>

      <div className="button-row">
        <button
          className="btn primary"
          onClick={createOrder}
          disabled={creatingOrder}
        >
          {creatingOrder ? "Creating order…" : "Create order from cart"}
        </button>
        <button
          className="btn ghost"
          onClick={() => refreshOrdersForUser(user)}
          disabled={loadingOrders}
        >
          {loadingOrders ? "Refreshing…" : "Refresh my orders"}
        </button>
      </div>

      <div className="orders-list">
        {orders.length === 0 ? (
          <p className="muted">No orders yet.</p>
        ) : (
          orders.map((o) => (
            <div key={o.id} className="order-row">
              <span>Order #{o.id}</span>
              <span className="order-total">{formatPrice(o.total)}</span>
            </div>
          ))
        )}
      </div>
    </section>
  );

  // ---------------- MAIN RENDER --------------------
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1 className="app-title">DevOps Shop</h1>
          <p className="backend-url">Backend: {BACKEND}</p>
        </div>

        {user && (
          <div className="header-user">
            <UserBadge />
            <button className="btn ghost small" onClick={handleLogout}>
              Log out
            </button>
          </div>
        )}
      </header>

      {user && <NavTabs />}

      {errorMsg && <div className="alert alert-error">{errorMsg}</div>}

      <main className="page">
        {!user || currentPage === PAGES.AUTH ? (
          <AuthPage />
        ) : currentPage === PAGES.PRODUCTS ? (
          <ProductsPage />
        ) : currentPage === PAGES.CART ? (
          <CartPage />
        ) : (
          <OrdersPage />
        )}
      </main>
    </div>
  );
}

export default App;