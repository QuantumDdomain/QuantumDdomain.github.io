// warning.js
window.addEventListener("DOMContentLoaded", () => {
    const warningBar = document.createElement("div");
    warningBar.innerHTML = "⚠️ This tool works best on desktop. Mobile support may be limited.";
    warningBar.style.backgroundColor = "#ffcc00";
    warningBar.style.color = "#000";
    warningBar.style.padding = "10px";
    warningBar.style.textAlign = "center";
    warningBar.style.fontWeight = "bold";
    warningBar.style.fontSize = "16px";
    warningBar.style.borderBottom = "2px solid #e0b800";
    warningBar.style.zIndex = "9999";
    warningBar.style.position = "sticky";
    warningBar.style.top = "0";
    document.body.prepend(warningBar);
  });
  