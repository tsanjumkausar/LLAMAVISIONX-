// import React from "react";
// import UrlScanner from "./components/UrlScanner";

// function App() {
//   return (
//     <div style={{ padding: "2rem", fontFamily: "Arial" }}>
//       <h2>🌐 CyberEye 2.0 – URL Phishing Scanner</h2>
//       <UrlScanner />
//     </div>
//   );
// }

// export default App;

import React, { useState } from "react";
import UrlScanner from "./components/UrlScanner";

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  return (
    <div
      style={{
        backgroundColor: "#f79175", // 🎨 Beautiful purple background
        minHeight: "100vh",
        padding: "2rem",
        transition: "background-color 0.3s ease",
      }}
    >
      <UrlScanner isDarkMode={isDarkMode} setIsDarkMode={setIsDarkMode} />
    </div>
  );
}

export default App;
