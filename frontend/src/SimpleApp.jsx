// frontend/src/SimpleApp.jsx

const BACKEND =
  import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8001";

function SimpleApp() {
  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>SimpleApp test</h1>
      <p>Backend (from SimpleApp): {BACKEND}</p>
      <button>Button from SimpleApp</button>
    </div>
  );
}

export default SimpleApp;
