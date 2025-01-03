import React, { useState } from "react";
import '../styles/login.css'; // ייבוא עיצוב
import ForgotPassword from './ForgotPassword';

function Login() {
  const [username, setUsername] = useState(""); // state עבור שם משתמש
  const [password, setPassword] = useState(""); // state עבור סיסמה

  // פונקציה לטיפול בשליחת הטופס
  const handleSubmit = async (e) => {
    e.preventDefault(); // מניעת טעינת עמוד מחדש

    try {
      // שליחת בקשת API לשרת ה-Backend
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
});


      const data = await response.json(); // קבלת תגובת השרת

      if (response.ok) {
        alert(data.message); // הודעה במקרה של התחברות מוצלחת
      } else {
        alert(data.message); // הודעה במקרה של שגיאה
      }
    } catch (error) {
      console.error('Error during login:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <h2>Login to Comunication_LTD</h2>
      <div className="login-box">
        <form onSubmit={handleSubmit}> {/* קריאה לפונקציית handleSubmit */}
          <label>
            Username:
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)} // עדכון ה-state של שם המשתמש
              required
            />
          </label>
          <br />
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)} // עדכון ה-state של הסיסמה
              required
            />
          </label>
          <br />
          <button type="submit">Login</button>
        </form>
        <a href="/forgot-password" className="forgot-password">Forgot Password?</a>
        {/* הקישור Forgot Password הוסר מהשורה העליונה */}
      </div>
    </div>
  );
}

export default Login;
