import React, { useState } from "react";
import '../styles/register.css';

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // בדיקת אורך הסיסמה
    if (password.length < 10) {
      alert("Password must be at least 10 characters long.");
      // מאפשר המשך כדי לבדוק SQLI
    }

    // בדיקת תקינות אימייל
    if (!email.includes("@")) {
      alert("Please enter a valid email address.");
      // מאפשר המשך כדי לבדוק SQLI
    }

    try {
      const response = await fetch("http://localhost:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password, email }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message); // הודעה אם המשתמש נרשם בהצלחה
      } else {
        alert(data.message); // הודעת שגיאה אם יש בעיה ברישום
      }
    } catch (error) {
      console.error("Error registering user:", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
      <div className="register-container">
        <h2>Register</h2>
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
          <label>
            Email:
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
          </label>
          <br />
          <button type="submit">Register</button>
        </form>
      </div>
  );
}

export default Register;
