document.getElementById("scan-btn").addEventListener("click", async () => {
  document.getElementById("category").textContent = "Scanning...";
  document.getElementById("reason").textContent = "";

  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const url = tabs[0].url;

    try {
      const response = await fetch("http://localhost:5000/api/classify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
      });

      const result = await response.json();
      document.getElementById("category").textContent = result.category || "Error";
      document.getElementById("reason").textContent = result.reason || "No reason provided.";
    } catch (error) {
      document.getElementById("category").textContent = "Error";
      document.getElementById("reason").textContent = error.message;
    }
  });
});
