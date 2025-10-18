if (window.location.hostname.includes("youtube.com")) {
  const overlayMap = new Map();
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "logLinks") {
      const links = document.querySelectorAll("a");
      const hrefs = Array.from(links).map((a) => a.href);
      hrefs.forEach((href) => console.log(href));
      sendResponse({ count: links.length, links: hrefs });
    } else if (request.action === "updateOverlayText") {
      updateOverlayText(request.videoId, request.text);
      sendResponse({ success: true });
    }
  });

  function addOverlays() {
    const mobileThumbnails = document.querySelectorAll("ytm-thumbnail-cover");
    console.log("Found mobile thumbnails:", mobileThumbnails.length);

    mobileThumbnails.forEach((thumbnailCover) => {
      if (thumbnailCover.querySelector(".custom-overlay")) return;
      const parentLink = thumbnailCover.closest("a");
      if (!parentLink) return;

      const videoId = extractVideoId(parentLink.href);
      if (!videoId) return;

      const overlay = createOverlay(videoId);
      thumbnailCover.style.position = "relative";
      thumbnailCover.appendChild(overlay);
      overlayMap.set(videoId, overlay);
      console.log("Added mobile overlay for video:", videoId);
    });
    const desktopThumbnails = document.querySelectorAll(
      "yt-thumbnail-view-model"
    );
    console.log("Found desktop thumbnails:", desktopThumbnails.length);
    desktopThumbnails.forEach((thumbnailView) => {
      if (thumbnailView.querySelector(".custom-overlay")) return;
      const parentLink = thumbnailView.closest("a");
      if (!parentLink) return;
      const videoId = extractVideoId(parentLink.href);
      if (!videoId) return;
      const overlay = createOverlay(videoId);
      thumbnailView.style.position = "relative";
      thumbnailView.appendChild(overlay);
      overlayMap.set(videoId, overlay);
    });
    const searchThumbnails = document.querySelectorAll("ytd-thumbnail");
    searchThumbnails.forEach((thumbnail) => {
      if (thumbnail.querySelector(".custom-overlay")) return;
      const link = thumbnail.querySelector("a#thumbnail");
      if (!link) return;
      const videoId = extractVideoId(link.href);
      if (!videoId) return;
      const overlay = createOverlay(videoId);
      thumbnail.style.position = "relative";
      thumbnail.appendChild(overlay);
      overlayMap.set(videoId, overlay);
    });
  }

  function createOverlay(videoId) {
    const overlay = document.createElement("div");
    overlay.className = "custom-overlay";
    overlay.style.cssText = `
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(0, 0, 0, 0.8);
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: bold;
      z-index: 100;
      pointer-events: none;
    `;
    overlay.textContent = videoId;
    fetchOverlayText(videoId).then((text) => {
      if (text) {
        overlay.textContent = text;
      }
    });
    return overlay;
  }

  async function fetchOverlayText(videoId) {
    try {
      const response = await fetch("http://localhost:3000/v2/video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoId }),
      });
      if (response.ok) {
        const data = await response.json();
        console.log(`Received text for ${videoId}:`, data.text);
        return data.text;
      } else {
        console.error("API error:", response.status, response.statusText);
        return null;
      }
    } catch (error) {
      console.error("Network error:", error);
      return null;
    }
  }

  function extractVideoId(url) {
    const match = url.match(/[?&]v=([^&]+)/);
    return match ? match[1] : null;
  }

  function updateOverlayText(videoId, text) {
    const overlay = overlayMap.get(videoId);
    if (overlay) overlay.textContent = text;
  }

  function updateAllOverlays(referenceData) {
    for (const [videoId, text] of Object.entries(referenceData)) {
      updateOverlayText(videoId, text);
    }
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", addOverlays);
  else addOverlays();
  const observer = new MutationObserver(addOverlays);
  observer.observe(document.body, { childList: true, subtree: true });
  window.updateYouTubeOverlays = updateAllOverlays;
}
