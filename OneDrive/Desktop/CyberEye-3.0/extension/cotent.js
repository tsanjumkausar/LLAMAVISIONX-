(async function () {
  const currentUrl = window.location.href;

  try {
    const response = await fetch("http://localhost:5000/api/classify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: currentUrl })
    });

    const data = await response.json();

    if (["Phishing", "Malicious", "Defacement"].includes(data.category)) {
      showWarning(data.category, data.reason);
    }
  } catch (error) {
    console.error("Error fetching classification:", error);
  }

  function showWarning(category, reason) {
    const warning = document.createElement("div");
    warning.style.position = "fixed";
    warning.style.top = "0";
    warning.style.left = "0";
    warning.style.width = "100%";
    warning.style.backgroundColor = "#ff0000";
    warning.style.color = "#fff";
    warning.style.zIndex = "999999";
    warning.style.padding = "12px";
    warning.style.fontSize = "16px";
    warning.style.fontFamily = "Arial, sans-serif";
    warning.innerHTML = `
      ⚠️ <b>CyberEye Warning:</b> This site may be <b>${category}</b>.<br/>
      Reason: ${reason}
    `;
    document.body.prepend(warning);
  }
})();
