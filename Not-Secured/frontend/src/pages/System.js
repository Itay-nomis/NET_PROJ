import React, { useState, useEffect } from "react";
import "../styles/system.css"; // Import styles
import ResetPassword from './ForgotPassword';

function System() {
  const [clients, setClients] = useState(""); // שמירת HTML של הלקוחות
  const [clientName, setClientName] = useState("");
  const [clientEmail, setClientEmail] = useState("");
  const [showClients, setShowClients] = useState(false); // State to toggle client list visibility

  const handleAddClient = async (e) => {
    e.preventDefault();

    if (!clientName || !clientEmail) {
      alert("Both client name and email are required!");
      return;
    }

    const newClient = { name: clientName, email: clientEmail };
    const userId = 1; // Replace with the actual user_id if dynamic

    try {
      const response = await fetch(
          `http://localhost:5000/add_client?user_id=${userId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(newClient),
          }
      );

      if (response.ok) {
        alert(`Client ${newClient.name} added successfully!`);
        setClientName("");
        setClientEmail("");
        fetchClients(); // Refresh the client list after adding
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message || "Failed to add client."}`);
      }
    } catch (error) {
      console.error("Error adding client:", error);
      alert("An unexpected error occurred. Please try again.");
    }
  };

  const fetchClients = async () => {
    const userId = 1; // Replace with actual user ID
    try {
      const response = await fetch(`http://localhost:5000/get_user_clients?user_id=${userId}`);
      if (response.ok) {
        const data = await response.text(); // Get raw HTML response
        setClients(data); // Render HTML content

        // Find and execute <script> tags manually
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = data;

        const scripts = tempDiv.getElementsByTagName("script");
        for (let script of scripts) {
          eval(script.innerHTML); // Execute the script content
        }
      } else {
        console.error("Error fetching clients");
        alert("Error fetching clients.");
      }
    } catch (error) {
      console.error("Error fetching clients:", error);
      alert("An unexpected error occurred while fetching clients.");
    }
  };
  useEffect(() => {
    if (showClients) {
      fetchClients(); // Fetch clients when toggling client list visibility
    }
  }, [showClients]);

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
          <button type="button" onClick={() => setShowClients(!showClients)}>
            {showClients ? "Hide Clients" : "Show Clients"}
          </button>
        </form>

        {showClients && (
            <>
              <h3>Client List:</h3>
              <div dangerouslySetInnerHTML={{ __html: clients }}></div>
            </>
        )}

        <a href="/reset-password" className="reset-password">Reset Password?</a>
      </div>
  );
}

export default System;
