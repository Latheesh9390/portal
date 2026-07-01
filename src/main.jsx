import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import { AdminAuthProvider } from "./context/AdminAuthContext";
import { StudentAuthProvider } from "./context/StudentAuthContext";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AdminAuthProvider>
        <StudentAuthProvider>
          <App />
        </StudentAuthProvider>
      </AdminAuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
