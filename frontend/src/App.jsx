import { useState, useEffect } from "react";
import axios from "axios";

const BACKEND = "http://127.0.0.1:8001";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState(null);
  const [cart, setCart] = useState(null);

  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [products, setProducts] = useState([]);

  const [orders, setOrders] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");

  // Fetch categories on load
  useEffect(() => {
    axios
      .get(`${BACKEND}/products/categories`)
      .then((res) => setCategories(res.data))
      .catch(() => setErrorMsg("Failed to load categories"));
  }, []);

  const createUserAndCart = async () => {
    try {
      setErrorMsg("");

      // 1. Create user
      const res = await axios.post(`${BACKEND}/users/`, {
        email,
        password,
      });

      setUser(res.data);

      // 2. Create or load cart
      const cartRes = await axios.post(`${BACKEND}/cart/${res.data.id}`);
      setCart(cartRes.data);
    } catch (err) {
      setErrorMsg("Failed to create user");
    }
  };

  const loadProductsInCategory = async (category) => {
    setSelectedCategory(category);
    try {
      const res = await axios.get(`${BACKEND}/products/category/${category}`);
      setProducts(res.data);
    } catch {
      setErrorMsg("Failed to load products");
    }
  };

  const addToCart = async (productId) => {
    if (!cart) return;

    try {
      const res = await axios.post(`${BACKEND}/cart/${cart.id}/items`, {
        product_id: productId,
        quantity: 1,
      });
      setCart(res.data);
    } catch {
      setErrorMsg("Failed to add item to cart");
    }
  };

  const createOrder = async () => {
    if (!user) return;
    try {
      const res = await axios.post(`${BACKEND}/orders/${user.id}`);
      alert("Order created with total: " + res.data.total);
      loadOrders();
    } catch {
      setErrorMsg("Failed to create order");
    }
  };

  const loadOrders = async () => {
    if (!user) return;

    try {
      const res = await axios.get(`${BACKEND}/orders/user/${user.id}`);
      setOrders(res.data);
    } catch {
      setErrorMsg("Failed to load orders");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>DevOps Shop Frontend</h1>
      <p>Backend: {BACKEND}</p>

      {errorMsg && (
        <div style={{ color: "white", background: "#ffb3b3", padding: "10px" }}>
          {errorMsg}
        </div>
      )}

      {/* USER SECTION */}
      <div style={{ border: "1px solid #ccc", padding: "20px", marginTop: "20px" }}>
        <h2>User</h2>

        {!user ? (
          <>
            <p>No user yet. Create one:</p>
            <input
              placeholder="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              placeholder="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ marginLeft: "10px" }}
            />
            <button onClick={createUserAndCart} style={{ marginLeft: "10px" }}>
              Create user + cart
            </button>
          </>
        ) : (
          <p>User logged in: <b>{user.email}</b></p>
        )}
      </div>

      {/* PRODUCTS + CATEGORIES */}
      <div style={{ border: "1px solid #ccc", padding: "20px", marginTop: "20px" }}>
        <h2>Products (via FakeStore API → your backend)</h2>

        <h4>Categories:</h4>
        <div>
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => loadProductsInCategory(c)}
              style={{ marginRight: "10px", marginTop: "5px" }}
            >
              {c}
            </button>
          ))}
        </div>

        <h4 style={{ marginTop: "20px" }}>Products:</h4>
        {products.length === 0 ? (
          <p>No products yet.</p>
        ) : (
          products.map((p) => (
            <div key={p.id} style={{ marginBottom: "10px" }}>
              <b>{p.title}</b> — ${p.price}
              <button
                onClick={() => addToCart(p.id)}
                style={{ marginLeft: "10px" }}
              >
                Add to cart
              </button>
            </div>
          ))
        )}
      </div>

      {/* ORDERS */}
      <div style={{ border: "1px solid #ccc", padding: "20px", marginTop: "20px" }}>
        <h2>Orders</h2>

        <button onClick={createOrder}>Create order from cart</button>
        <button onClick={loadOrders} style={{ marginLeft: "10px" }}>
          Refresh my orders
        </button>

        <div style={{ marginTop: "20px" }}>
          {orders.length === 0 ? (
            <p>No orders yet.</p>
          ) : (
            orders.map((o) => (
              <div key={o.id}>
                Order #{o.id} — Total: ${o.total.toFixed(2)}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
