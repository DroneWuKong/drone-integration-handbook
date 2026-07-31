(() => {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const menuButton = $("#menuButton");
  const drawer = $("#navDrawer");
  const drawerBackdrop = $("#drawerBackdrop");
  const drawerClose = $("#drawerClose");
  const searchOverlay = $("#searchOverlay");
  const searchButton = $("#searchButton");
  const searchClose = $("#searchClose");
  const searchInput = $("#searchInput");
  const searchResults = $("#searchResults");
  const currentSection = $("#currentSection");
  const readingProgress = $("#readingProgress");
  const backToTop = $("#backToTop");
  const toast = $("#toast");

  let lastDrawerFocus = null;
  let lastSearchFocus = null;
  let toastTimer = 0;

  function syncBodyLock() {
    const drawerOpen = drawer?.classList.contains("open");
    const searchOpen = searchOverlay && !searchOverlay.hidden;
    document.body.classList.toggle("modal-open", Boolean(drawerOpen || searchOpen));
  }

  function openDrawer() {
    if (!drawer || !drawerBackdrop) return;
    lastDrawerFocus = document.activeElement;
    drawerBackdrop.hidden = false;
    drawer.setAttribute("aria-hidden", "false");
    menuButton?.setAttribute("aria-expanded", "true");
    requestAnimationFrame(() => drawer.classList.add("open"));
    syncBodyLock();
    window.setTimeout(() => drawerClose?.focus(), 30);
  }

  function closeDrawer({ restoreFocus = true } = {}) {
    if (!drawer || !drawerBackdrop) return;
    drawer.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    menuButton?.setAttribute("aria-expanded", "false");
    window.setTimeout(() => {
      if (!drawer.classList.contains("open")) drawerBackdrop.hidden = true;
    }, 230);
    syncBodyLock();
    if (restoreFocus && lastDrawerFocus instanceof HTMLElement) lastDrawerFocus.focus();
  }

  menuButton?.addEventListener("click", openDrawer);
  drawerClose?.addEventListener("click", () => closeDrawer());
  drawerBackdrop?.addEventListener("click", () => closeDrawer());
  drawer?.addEventListener("click", (event) => {
    if (event.target.closest("a[href^='#']")) closeDrawer({ restoreFocus: false });
  });

  function showToast(message) {
    if (!toast) return;
    window.clearTimeout(toastTimer);
    toast.textContent = message;
    toast.classList.add("visible");
    toastTimer = window.setTimeout(() => toast.classList.remove("visible"), 1800);
  }

  async function copyText(value) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
      return;
    }
    const textarea = document.createElement("textarea");
    textarea.value = value;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    const copied = document.execCommand("copy");
    textarea.remove();
    if (!copied) throw new Error("copy failed");
  }

  document.addEventListener("click", async (event) => {
    const copyButton = event.target.closest("[data-copy-anchor]");
    if (!copyButton) return;
    const anchor = copyButton.dataset.copyAnchor;
    const url = `${window.location.href.split("#")[0]}#${anchor}`;
    try {
      await copyText(url);
      showToast("Reference link copied");
    } catch {
      showToast("Could not copy the link");
    }
  });

  const trackedSections = $$(".part-divider, .chapter");
  const navLinks = $$("[data-nav-target]");
  let scrollScheduled = false;
  let activeAnchor = "";

  function openNavigationParents(link) {
    let parent = link?.parentElement;
    while (parent) {
      if (parent.tagName === "DETAILS") parent.open = true;
      parent = parent.parentElement;
    }
  }

  function setActiveSection(section) {
    if (!section) return;
    const title = section.dataset.title || section.dataset.sectionTitle || "Overview";
    if (currentSection) currentSection.textContent = title;

    const nextAnchor = section.classList.contains("chapter") ? section.id : "";
    if (nextAnchor === activeAnchor) return;
    activeAnchor = nextAnchor;
    navLinks.forEach((link) => {
      const active = Boolean(nextAnchor && link.dataset.navTarget === nextAnchor);
      link.classList.toggle("active", active);
      if (active) {
        link.setAttribute("aria-current", "location");
        openNavigationParents(link);
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  function updateScrollState() {
    scrollScheduled = false;
    const threshold =
      (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--topbar-height")) || 52) + 92;
    let selected = null;
    for (const section of trackedSections) {
      if (section.getBoundingClientRect().top <= threshold) selected = section;
      else break;
    }

    if (selected) {
      setActiveSection(selected);
    } else {
      if (currentSection) currentSection.textContent = "Overview";
      activeAnchor = "";
      navLinks.forEach((link) => {
        link.classList.remove("active");
        link.removeAttribute("aria-current");
      });
    }

    const scrollable = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    const percent = Math.min(100, Math.max(0, (window.scrollY / scrollable) * 100));
    if (readingProgress) readingProgress.style.width = `${percent}%`;
    backToTop?.classList.toggle("visible", window.scrollY > 700);
  }

  function scheduleScrollState() {
    if (scrollScheduled) return;
    scrollScheduled = true;
    requestAnimationFrame(updateScrollState);
  }

  window.addEventListener("scroll", scheduleScrollState, { passive: true });
  window.addEventListener("resize", scheduleScrollState, { passive: true });
  updateScrollState();

  backToTop?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: reducedMotion ? "auto" : "smooth" });
  });

  let metadata = [];
  try {
    metadata = JSON.parse($("#handbookMetadata")?.textContent || "[]");
  } catch (error) {
    console.warn("Handbook search metadata could not be read", error);
  }

  const metadataByAnchor = new Map(metadata.map((entry) => [entry.anchor, entry]));
  let searchIndex = null;
  let searchFilter = "all";
  let activeResultIndex = -1;
  let currentResults = [];
  let searchDebounce = 0;

  function normalize(value) {
    return value.toLocaleLowerCase().normalize("NFKD");
  }

  function buildSearchIndex() {
    if (searchIndex) return searchIndex;
    searchIndex = [];

    $$(".chapter").forEach((section) => {
      const meta = metadataByAnchor.get(section.id) || {
        anchor: section.id,
        title: section.dataset.title || section.id,
        kind: section.dataset.kind || "chapter",
        group: section.dataset.group || "Handbook",
        source: section.dataset.source || "",
      };
      const title = section.dataset.title || meta.title;
      const sectionText = section.textContent.replace(/\s+/g, " ").trim();
      const firstHeading = $("h1", section);

      searchIndex.push({
        ...meta,
        title,
        heading: firstHeading?.textContent.trim() || title,
        text: sectionText,
        target: section,
        targetId: section.id,
      });

      $$("h2, h3", section).forEach((heading) => {
        let text = heading.textContent || "";
        let sibling = heading.nextElementSibling;
        while (sibling && !/^H[1-3]$/.test(sibling.tagName)) {
          text += ` ${sibling.textContent || ""}`;
          sibling = sibling.nextElementSibling;
        }
        searchIndex.push({
          ...meta,
          title,
          heading: heading.textContent.trim(),
          text: text.replace(/\s+/g, " ").trim(),
          target: heading,
          targetId: heading.id || section.id,
        });
      });
    });

    return searchIndex;
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function highlight(value, terms) {
    let result = escapeHtml(value);
    for (const term of terms) {
      if (term.length < 2) continue;
      const expression = new RegExp(`(${escapeRegExp(escapeHtml(term))})`, "gi");
      result = result.replace(expression, "<mark>$1</mark>");
    }
    return result;
  }

  function snippetFor(text, terms, maxLength = 190) {
    const lower = normalize(text);
    let start = 0;
    let best = -1;
    for (const term of terms) {
      const position = lower.indexOf(term);
      if (position !== -1 && (best === -1 || position < best)) best = position;
    }
    if (best > maxLength / 2) start = best - Math.floor(maxLength / 3);
    const boundary = text.lastIndexOf(" ", start);
    if (boundary > 0) start = boundary + 1;
    let snippet = text.slice(start, start + maxLength).trim();
    if (start > 0) snippet = `…${snippet}`;
    if (start + maxLength < text.length) snippet += "…";
    return snippet;
  }

  function scoreEntry(entry, query, terms) {
    if (searchFilter !== "all" && entry.kind !== searchFilter) return 0;
    const title = normalize(entry.title);
    const heading = normalize(entry.heading);
    const context = normalize(`${entry.group} ${entry.source}`);
    const body = normalize(entry.text);
    let score = 0;

    if (title.includes(query)) score += 48;
    if (heading.includes(query)) score += 42;
    if (context.includes(query)) score += 20;
    if (body.includes(query)) score += 12;

    let allPresent = true;
    for (const term of terms) {
      let termScore = 0;
      if (title.includes(term)) termScore += 18;
      if (heading.includes(term)) termScore += 16;
      if (context.includes(term)) termScore += 7;
      const bodyOccurrences = body.split(term).length - 1;
      termScore += Math.min(bodyOccurrences, 8);
      if (termScore === 0) allPresent = false;
      score += termScore;
    }
    if (allPresent) score += 24;
    if (entry.heading === entry.title) score += 2;
    return score;
  }

  function setActiveResult(index) {
    const items = $$(".search-result", searchResults);
    items.forEach((item) => {
      item.classList.remove("active");
      item.setAttribute("aria-selected", "false");
    });
    if (!items.length) {
      activeResultIndex = -1;
      return;
    }
    activeResultIndex = Math.max(0, Math.min(index, items.length - 1));
    const active = items[activeResultIndex];
    active.classList.add("active");
    active.setAttribute("aria-selected", "true");
    active.scrollIntoView({ block: "nearest" });
  }

  function renderSearchResults(queryValue) {
    if (!searchResults) return;
    const query = normalize(queryValue.trim());
    if (query.length < 2) {
      currentResults = [];
      activeResultIndex = -1;
      searchResults.innerHTML =
        '<div class="search-empty"><strong>Search the whole handbook.</strong><span>Use two or more characters. Search stays in this browser tab and is not transmitted.</span></div>';
      return;
    }

    const terms = query.split(/\s+/).filter((term) => term.length >= 2);
    currentResults = buildSearchIndex()
      .map((entry) => ({ entry, score: scoreEntry(entry, query, terms) }))
      .filter((candidate) => candidate.score > 0)
      .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title))
      .slice(0, 30)
      .map((candidate) => candidate.entry);

    if (!currentResults.length) {
      activeResultIndex = -1;
      searchResults.innerHTML =
        '<div class="search-empty"><strong>No matching references.</strong><span>Try a protocol, platform, component, symptom, or shorter phrase.</span></div>';
      return;
    }

    const rows = currentResults
      .map((entry, index) => {
        const snippet = snippetFor(entry.text, terms);
        return `<a class="search-result" role="option" aria-selected="false" data-result-index="${index}" href="#${escapeHtml(entry.targetId)}">
          <span class="search-result-context">${escapeHtml(entry.group)} · ${escapeHtml(entry.title)}</span>
          <span class="search-result-heading">${highlight(entry.heading, terms)}</span>
          <span class="search-result-kind">${escapeHtml(entry.kind)}</span>
          <span class="search-result-snippet">${highlight(snippet, terms)}</span>
        </a>`;
      })
      .join("");
    searchResults.innerHTML = `<div class="search-count">${currentResults.length} result${currentResults.length === 1 ? "" : "s"}</div>${rows}`;
    setActiveResult(0);
  }

  function flashTarget(target) {
    if (!(target instanceof HTMLElement)) return;
    target.classList.remove("search-hit");
    requestAnimationFrame(() => {
      target.classList.add("search-hit");
      window.setTimeout(() => target.classList.remove("search-hit"), 1700);
    });
  }

  function jumpToResult(index) {
    const entry = currentResults[index];
    if (!entry) return;
    closeSearch({ restoreFocus: false });
    if (entry.targetId) history.pushState(null, "", `#${entry.targetId}`);
    entry.target.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
    flashTarget(entry.target);
  }

  function openSearch() {
    if (!searchOverlay || !searchInput) return;
    lastSearchFocus = document.activeElement;
    buildSearchIndex();
    searchOverlay.hidden = false;
    syncBodyLock();
    searchInput.value = "";
    searchFilter = "all";
    $$("[data-search-filter]").forEach((button) => {
      button.classList.toggle("active", button.dataset.searchFilter === "all");
    });
    renderSearchResults("");
    requestAnimationFrame(() => searchInput.focus());
  }

  function closeSearch({ restoreFocus = true } = {}) {
    if (!searchOverlay || searchOverlay.hidden) return;
    searchOverlay.hidden = true;
    syncBodyLock();
    if (restoreFocus && lastSearchFocus instanceof HTMLElement) lastSearchFocus.focus();
  }

  searchButton?.addEventListener("click", openSearch);
  $$('[data-open-search]').forEach((button) => button.addEventListener("click", openSearch));
  searchClose?.addEventListener("click", () => closeSearch());
  searchOverlay?.addEventListener("click", (event) => {
    if (event.target === searchOverlay) closeSearch();
  });

  searchInput?.addEventListener("input", () => {
    window.clearTimeout(searchDebounce);
    searchDebounce = window.setTimeout(() => renderSearchResults(searchInput.value), 90);
  });

  $$("[data-search-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      searchFilter = button.dataset.searchFilter || "all";
      $$("[data-search-filter]").forEach((candidate) => {
        candidate.classList.toggle("active", candidate === button);
      });
      renderSearchResults(searchInput?.value || "");
    });
  });

  searchResults?.addEventListener("mousemove", (event) => {
    const result = event.target.closest("[data-result-index]");
    if (result) setActiveResult(Number(result.dataset.resultIndex));
  });

  searchResults?.addEventListener("click", (event) => {
    const result = event.target.closest("[data-result-index]");
    if (!result) return;
    event.preventDefault();
    jumpToResult(Number(result.dataset.resultIndex));
  });

  function trapFocus(event, container) {
    if (event.key !== "Tab") return;
    const focusable = $$(
      'button:not([disabled]), input:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])',
      container,
    ).filter((element) => element.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      if (searchOverlay && !searchOverlay.hidden) closeSearch();
      else openSearch();
      return;
    }

    if (event.key === "Escape") {
      if (searchOverlay && !searchOverlay.hidden) closeSearch();
      else if (drawer?.classList.contains("open")) closeDrawer();
      return;
    }

    if (searchOverlay && !searchOverlay.hidden) {
      trapFocus(event, searchOverlay);
      if (event.target === searchInput) {
        if (event.key === "ArrowDown") {
          event.preventDefault();
          setActiveResult(activeResultIndex + 1);
        } else if (event.key === "ArrowUp") {
          event.preventDefault();
          setActiveResult(activeResultIndex - 1);
        } else if (event.key === "Enter" && activeResultIndex >= 0) {
          event.preventDefault();
          jumpToResult(activeResultIndex);
        }
      }
    } else if (drawer?.classList.contains("open")) {
      trapFocus(event, drawer);
    }
  });

  $$('.chapter-body a[href^="http"], .chapter-tools a[href^="http"]').forEach((link) => {
    link.target = "_blank";
    link.rel = "noopener noreferrer";
  });
})();
