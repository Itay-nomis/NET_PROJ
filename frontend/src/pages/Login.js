import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

function Login({ setIsLoggedIn }) { // מקבל את setIsLoggedIn כ-פרופס
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (!username || !password) {
      alert("Username and password are required!");
      return;
    }
  
    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }), // שליחה נכונה של שם משתמש וסיסמה
      });
  
      const data = await response.json();
  
      if (response.ok) {
        alert(data.message);
        navigate("/system"); // מעבר למסך System אם ההתחברות הצליחה
      } else {
        alert(data.message); // הצגת הודעת שגיאה משרת ה-Backend
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("An error occurred. Please try again.");
    }
  };
  

  return (
    <div className="login-container">
      <h2>Login to Comunication_LTD</h2>
      <div className="login-box">
        <form onSubmit={handleSubmit}>
          <label>
            Username:
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </label>
          <br />
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          <br />
          <button type="submit">Login</button>
        </form>
        <a href="/forgot-password" className="forgot-password">
          Forgot Password?
        </a>
      </div>
    </div>
  );
}

export default Login;
