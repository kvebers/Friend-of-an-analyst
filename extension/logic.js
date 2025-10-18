chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "logLinks") {
    const links = document.querySelectorAll("a");
    const hrefs = Array.from(links).map((a) => a.href);
    hrefs.forEach((href) => console.log(href));
    sendResponse({ count: links.length, links: hrefs });
  }
});

function logLinks() {
  const links = document.querySelectorAll("a");
  links.forEach((a) => console.log(a.href));
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", logLinks);
} else {
  logLinks();
}

const observer = new MutationObserver(logLinks);
observer.observe(document.body, { childList: true, subtree: true });
