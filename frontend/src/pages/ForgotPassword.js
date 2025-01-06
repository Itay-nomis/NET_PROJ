import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import sha1 from "crypto-js/sha1";
import "../styles/forgotPassword.css";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [generatedCode, setGeneratedCode] = useState("");
  const [userCode, setUserCode] = useState("");
  const [username, setUsername] = useState(""); // שמירת שם המשתמש
  const navigate = useNavigate();

  const handleGenerateCode = (e) => {
    e.preventDefault();
    const randomCode = sha1(new Date().toISOString()).toString();
    setGeneratedCode(randomCode);
    setUsername(email.split("@")[0]); // שמירת שם המשתמש על בסיס האימייל (לדוגמה בלבד)
    alert(`Verification code sent to ${email}: ${randomCode}`);
  };

  const handleVerifyCode = (e) => {
    e.preventDefault();
    if (userCode === generatedCode) {
      alert("Code verified! Redirecting to change password...");
      navigate("/change-password", { state: { username } }); // העברה עם state
    } else {
      alert("Invalid code. Please try again.");
    }
  };
  

  return (
    <div className="forgot-password-container">
      <h2>Forgot Password</h2>
      <form onSubmit={handleGenerateCode}>
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
        <button type="submit">Send Verification Code</button>
      </form>

      {generatedCode && (
        <form onSubmit={handleVerifyCode}>
          <label>
            Enter Verification Code:
            <input
              type="text"
              value={userCode}
              onChange={(e) => setUserCode(e.target.value)}
              required
            />
          </label>
          <br />
          <button type="submit">Verify Code</button>
        </form>
      )}
    </div>
  );
}

export default ForgotPassword;
