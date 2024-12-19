import React, { useState } from "react";
import '../styles/resetPassword.css'; // ייבוא עיצוב

function ResetPassword() {
  const [username, setUsername] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // בדיקת התאמה בסיסית לסיסמה החדשה
    if (newPassword.length < 10) {
      alert("Password must be at least 10 characters long.");
      return;
    }

    if (newPassword !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    try {
      // שלח בקשת POST ל-Backend
      const response = await fetch("http://localhost:5000/api/reset-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          currentPassword,
          newPassword,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message); // הצגת הודעת הצלחה
      } else {
        alert(data.message); // הצגת הודעת שגיאה
      }
    } catch (error) {
      console.error("Error resetting password:", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
      <div className="reset-password-container">
        <h2>Reset Password</h2>
        <form onSubmit={handleSubmit}>
          <label>
            User Name:
            <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
            />
          </label>
          <br />
          <label>
            Current Password:
            <input
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
            />
          </label>
          <br />
          <label>
            New Password:
            <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
            />
          </label>
          <br />
          <label>
            Confirm Password:
            <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
            />
          </label>
          <br />
          <button type="submit">Change Password</button>
        </form>
      </div>
  );
}

export default ResetPassword;
