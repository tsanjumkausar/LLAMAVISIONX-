import React, { useState } from "react";
import axios from "axios";
import "./UrlScanner.css";

function UrlScanner() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const handleScan = async () => {
    if (!url) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await axios.post("http://localhost:5000/api/classify", { url });
      setResult(res.data);
    } catch (err) {
      setResult({ category: "Error", reason: "Failed to fetch from API" });
    }
    setLoading(false);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`scanner-container ${darkMode ? "dark" : ""}`}>
      <div className="toggle-container">
        <label className="switch">
          <input type="checkbox" checked={darkMode} onChange={toggleDarkMode} />
          <span className="slider round"></span>
        </label>
        <span>{darkMode ? "🌙 Dark Mode" : "☀️ Light Mode"}</span>
      </div>

      <h1>🔐 CyberEye 2.0</h1>
      <p className="subheading">Real-time URL Phishing & Threat Detection</p>

      <div className="form-group">
        <input
          type="text"
          placeholder="Enter a URL (e.g., https://example.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button onClick={handleScan} disabled={loading}>
          {loading ? "Scanning..." : "Scan"}
        </button>
      </div>

      {result && (
        <div className="result">
          <h3>🔍 Scan Result</h3>
          <p><strong>Category:</strong> {result.category}</p>
          <p><strong>Reason:</strong></p>
          <ul>
            {result.reason.split('\n').map((line, i) => (
              <li key={i}>• {line.trim()}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default UrlScanner;

