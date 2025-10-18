const btn = document.getElementById("toggle");
let enabled = localStorage.getItem("enabled") !== "false";

function update() {
  if (enabled) {
    btn.textContent = "Disable";
    btn.className = "enabled";
  } else {
    btn.textContent = "Enable";
    btn.className = "disabled";
  }
}

update();

btn.onclick = async () => {
  enabled = !enabled;
  localStorage.setItem("enabled", enabled);
  update();

  if (enabled) {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    chrome.tabs.sendMessage(tab.id, { action: "logLinks" }, (response) => {
      if (response) {
        console.log("Links found:", response.count);
      }
    });
  }
};
