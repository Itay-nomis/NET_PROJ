import React, { useState } from "react";
import "../styles/system.css"; // ייבוא עיצוב
import ResetPassword from './ForgotPassword';

function System() {
  const [clients, setClients] = useState([]); // רשימת לקוחות
  const [clientName, setClientName] = useState("");
  const [clientEmail, setClientEmail] = useState("");

  const handleAddClient = (e) => {
    e.preventDefault();
    const newClient = { name: clientName, email: clientEmail };

    // הוספת לקוח לרשימה
    setClients([...clients, newClient]);

    // איפוס שדות הטופס
    setClientName("");
    setClientEmail("");

    alert(`Client ${newClient.name} added successfully!`);
  };

  return (
    <div className="system-container">
      <h2>System Management</h2>
      <form onSubmit={handleAddClient}>
        <label>
          Client Name:
          <input
            type="text"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Client Email:
          <input
            type="email"
            value={clientEmail}
            onChange={(e) => setClientEmail(e.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit">Add Client</button>
      </form>

      <h3>Client List:</h3>
      <ul>
        {clients.map((client, index) => (
          <li key={index}>
            {client.name} - {client.email}
          </li>
        ))}
      </ul>
	   <a href="/reset-password" className="reset-password">Reset Password?</a>
    </div>
  );
}

export default System;
