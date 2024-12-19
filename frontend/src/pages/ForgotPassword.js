import React, { useState } from "react";
import sha1 from "crypto-js/sha1"; // ייבוא ספריית SHA-1
import "../styles/forgotPassword.css";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [generatedCode, setGeneratedCode] = useState("");
  const [userCode, setUserCode] = useState("");
  const [isCodeVerified, setIsCodeVerified] = useState(false);

  const handleGenerateCode = (e) => {
    e.preventDefault();

    // יצירת קוד אקראי באמצעות SHA-1
    const randomCode = sha1(new Date().toISOString()).toString();
    setGeneratedCode(randomCode);

    // סימולציה של שליחת המייל
    alert(`Verification code sent to ${email}: ${randomCode}`);
  };

  const handleVerifyCode = (e) => {
    e.preventDefault();

    if (userCode === generatedCode) {
      setIsCodeVerified(true);
      alert("Code verified! You can reset your password.");
    } else {
      alert("Invalid code. Please try again.");
    }
  };

  return (
    <div className="forgot-password-container">
      <h2>Forgot Password</h2>

      {!isCodeVerified ? (
        <>
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
        </>
      ) : (
        <p>You can now reset your password.</p>
      )}
    </div>
  );
}

export default ForgotPassword;
