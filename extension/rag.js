const API_ENDPOINT = "http://localhost/v1/rag";

document.addEventListener("DOMContentLoaded", () => {
  const promptInput = document.getElementById("prompt");
  const askBtn = document.getElementById("askBtn");
  const outputDiv = document.getElementById("output");
  const contextSection = document.getElementById("contextSection");
  const contextList = document.getElementById("contextList");

  if (
    !promptInput ||
    !askBtn ||
    !outputDiv ||
    !contextSection ||
    !contextList
  ) {
    console.error("Required DOM elements not found");
    return;
  }

  async function queryRAG(prompt) {
    try {
      askBtn.disabled = true;
      outputDiv.className = "output loading";
      outputDiv.textContent = "Loading...";
      contextList.innerHTML = "";
      contextSection.style.display = "none";

      const response = await fetch(API_ENDPOINT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      outputDiv.className = "output";
      outputDiv.textContent = data.results || "No response";

      if (
        data.context &&
        Array.isArray(data.context) &&
        data.context.length > 0
      ) {
        contextList.innerHTML = data.context
          .filter((ctx) => ctx && ctx !== "None")
          .map((ctx) => `<div class="context-item">${escapeHtml(ctx)}</div>`)
          .join("");

        if (contextList.children.length > 0) {
          contextSection.style.display = "block";
        }
      }
    } catch (error) {
      outputDiv.className = "output error";
      outputDiv.textContent = `Error: ${error.message}`;
      contextSection.style.display = "none";
    } finally {
      askBtn.disabled = false;
    }
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  askBtn.addEventListener("click", () => {
    const prompt = promptInput.value.trim();
    if (prompt) {
      queryRAG(prompt);
    }
  });

  promptInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && e.ctrlKey) {
      const prompt = promptInput.value.trim();
      if (prompt) {
        queryRAG(prompt);
      }
    }
  });
});
