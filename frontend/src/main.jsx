import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import SimpleApp from "./SimpleApp.jsx";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <SimpleApp />
  </React.StrictMode>
);
