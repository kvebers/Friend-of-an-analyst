if (window.location.hostname.includes("youtube.com")) {
  const overlayMap = new Map();

  let currentVideoId = null;
  let videoOverlay = null;

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "logLinks") {
      const links = document.querySelectorAll("a");
      const hrefs = Array.from(links).map((a) => a.href);
      hrefs.forEach((href) => console.log(href));
      sendResponse({ count: links.length, links: hrefs });
    } else if (request.action === "updateOverlayText") {
      updateOverlayText(request.videoId, request.text);
      sendResponse({ success: true });
    } else if (request.action === "updateVideoOverlayText") {
      updateVideoOverlayText(request.videoId, request.text);
      sendResponse({ success: true });
    }
  });

  function addThumbnailOverlays() {
    const mobileThumbnails = document.querySelectorAll("ytm-thumbnail-cover");
    console.log("Found mobile thumbnails:", mobileThumbnails.length);

    mobileThumbnails.forEach((thumbnailCover) => {
      if (thumbnailCover.querySelector(".custom-overlay")) return;
      const parentLink = thumbnailCover.closest("a");
      if (!parentLink) return;

      const videoId = extractVideoId(parentLink.href);
      if (!videoId) return;

      const overlay = createThumbnailOverlay(videoId);
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
      const overlay = createThumbnailOverlay(videoId);
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
      const overlay = createThumbnailOverlay(videoId);
      thumbnail.style.position = "relative";
      thumbnail.appendChild(overlay);
      overlayMap.set(videoId, overlay);
    });
  }

  function createThumbnailOverlay(videoId) {
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
    fetchThumbnailOverlayText(videoId).then((text) => {
      if (text) {
        overlay.textContent = text;
      }
    });
    return overlay;
  }

  async function fetchThumbnailOverlayText(videoId) {
    try {
      const response = await fetch("http://localhost/v2/video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoId }),
      });
      if (response.ok) {
        const data = await response.json();
        console.log(`Received thumbnail text for ${videoId}:`, data.text);
        return data.text;
      } else {
        console.error(
          "Thumbnail API error:",
          response.status,
          response.statusText
        );
        return null;
      }
    } catch (error) {
      return null;
    }
  }

  function updateOverlayText(videoId, text) {
    const overlay = overlayMap.get(videoId);
    if (overlay) overlay.textContent = text;
  }

  function updateAllThumbnailOverlays(referenceData) {
    for (const [videoId, text] of Object.entries(referenceData)) {
      updateOverlayText(videoId, text);
    }
  }

  function addVideoOverlay() {
    if (videoOverlay && videoOverlay.parentNode) {
      videoOverlay.remove();
    }

    const videoContainer = document.querySelector("#movie_player");
    if (!videoContainer) {
      console.log("Video player not found");
      return;
    }

    const videoId = extractVideoIdFromUrl(window.location.href);
    if (!videoId) {
      console.log("Could not extract video ID");
      return;
    }

    if (currentVideoId === videoId && videoOverlay) {
      return;
    }

    currentVideoId = videoId;
    videoOverlay = document.createElement("div");
    videoOverlay.className = "custom-video-overlay";
    videoOverlay.style.cssText = `
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(0, 0, 0, 0.8);
      color: white;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: bold;
      z-index: 1000;
      pointer-events: none;
      max-width: 300px;
      word-wrap: break-word;
    `;
    videoOverlay.textContent = `Loading... ${videoId}`;

    videoContainer.appendChild(videoOverlay);
    console.log("Added video overlay for:", videoId);

    fetchVideoOverlayText(videoId).then((text) => {
      if (text && videoOverlay) {
        videoOverlay.textContent = text;
      }
    });
  }

  async function fetchVideoOverlayText(videoId) {
    try {
      const response = await fetch("http://localhost/v1/video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoId }),
      });

      if (response.ok) {
        const data = await response.json();
        return data.text;
      } else {
        return null;
      }
    } catch (error) {
      return null;
    }
  }

  function updateVideoOverlayText(videoId, text) {
    if (currentVideoId === videoId && videoOverlay) {
      videoOverlay.textContent = text;
    }
  }

  function extractVideoId(url) {
    const match = url.match(/[?&]v=([^&]+)/);
    return match ? match[1] : null;
  }

  function extractVideoIdFromUrl(url) {
    return extractVideoId(url);
  }

  function initialize() {
    addThumbnailOverlays();
    addVideoOverlay();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }

  const observer = new MutationObserver(() => {
    addThumbnailOverlays();
    const videoContainer = document.querySelector("#movie_player");
    if (videoContainer && !videoOverlay) {
      addVideoOverlay();
    }
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });

  let lastUrl = window.location.href;
  new MutationObserver(() => {
    const currentUrl = window.location.href;
    if (currentUrl !== lastUrl) {
      lastUrl = currentUrl;
      setTimeout(addVideoOverlay, 500);
    }
  }).observe(document.querySelector("title"), {
    childList: true,
    subtree: true,
  });

  window.updateYouTubeOverlays = updateAllThumbnailOverlays;
  window.updateYouTubeVideoOverlay = (videoId, text) => {
    updateVideoOverlayText(videoId, text);
  };
}
