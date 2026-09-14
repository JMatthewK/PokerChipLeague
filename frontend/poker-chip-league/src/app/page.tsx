"use client"; // Required because we are using React state (useState, useEffect)

import { useState, useEffect } from "react";

export default function Home() {
  // State to hold data from your FastAPI backend
  const [backendMessage, setBackendMessage] = useState<string>("Connecting to API...");

  // Fetch data from FastAPI when the component loads
  useEffect(() => {
    fetch("http://localhost:8000/")
      .then((res) => res.json())
      .then((data) => setBackendMessage(data.message || "Connected!"))
      .catch((err) => {
        console.error("Error connecting to backend:", err);
        setBackendMessage("Failed to connect to FastAPI backend.");
      });
  }, []);

  return (
    <main style={styles.container}>
      <header style={styles.header}>
        <h1>My Full-Stack AWS App</h1>
        <p>Built with Next.js & FastAPI</p>
      </header>

      <section style={styles.card}>
        <h2>Backend Status</h2>
        <p style={styles.statusText}>{backendMessage}</p>
      </section>
    </main>
  );
}

// Simple inline styles to get you started without fighting CSS files
const styles = {
  container: {
    fontFamily: "system-ui, sans-serif",
    padding: "2rem",
    maxWidth: "800px",
    margin: "0 auto",
  },
  header: {
    borderBottom: "1px solid #ccc",
    paddingBottom: "1rem",
    marginBottom: "2rem",
  },
  card: {
    padding: "1.5rem",
    borderRadius: "8px",
    backgroundColor: "#f9f9f9",
    border: "1px solid #eaeaea",
  },
  statusText: {
    fontWeight: "bold",
    color: "#0070f3",
  },
};
