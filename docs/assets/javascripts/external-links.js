// Open all external links in a new tab.
// Uses MutationObserver to handle MkDocs Material instant navigation,
// which replaces DOM content without full page reloads.
(function () {
  function processLinks() {
    document.querySelectorAll("a[href^='http']").forEach(function (link) {
      if (!link.hostname || link.hostname === location.hostname) return;
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    });
  }

  // Run on initial load
  processLinks();

  // Re-run whenever MkDocs Material swaps page content
  var observer = new MutationObserver(processLinks);
  var content = document.querySelector("[data-md-component=content]");
  if (content) {
    observer.observe(content, { childList: true, subtree: true });
  }
})();
