import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import ResetPassword from "./pages/ResetPassword";
import ForgotPassword from "./pages/ForgotPassword";
import System from "./pages/System";

function App() {
  return (
    <Router>
      <div>
        <h1>Comunication_LTD</h1>
        <nav>
          <Link to="/login">Login</Link> |{" "}
          <Link to="/register">Register</Link> |{" "}
          <Link to="/reset-password">Reset Password</Link> |{" "}
          <Link to="/forgot-password">Forgot Password</Link> |{" "}
          <Link to="/system">System</Link>
        </nav>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/system" element={<System />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
