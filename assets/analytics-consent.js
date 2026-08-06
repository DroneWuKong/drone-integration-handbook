(() => {
  "use strict";

  const STORAGE_KEY = "uas.analytics-consent.v1";
  const MEASUREMENT_ID = "G-DXC5B1KWY5";
  const CSS = `
    #uas-analytics-consent{position:fixed;z-index:2147483646;right:max(12px,env(safe-area-inset-right));bottom:max(12px,env(safe-area-inset-bottom));width:min(420px,calc(100vw - 24px));padding:13px 14px;background:#151512;color:#e9e5dc;border:1px solid #3a3a30;border-radius:10px;box-shadow:0 12px 34px rgba(0,0,0,.32);font:13px/1.4 Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    #uas-analytics-consent[hidden],#uas-analytics-choices[hidden]{display:none!important}
    .uas-consent-copy strong{display:block;margin:0 0 3px;color:#fff;font-size:13px}.uas-consent-copy p{margin:0;color:#c2beb4}.uas-consent-copy a{color:#8ee6b0;text-underline-offset:2px}
    .uas-consent-actions{display:flex;gap:8px;margin-top:10px}.uas-consent-actions button{flex:1;min-height:34px;padding:7px 10px;border:1px solid #5b5b4e;border-radius:6px;background:transparent;color:#f5f2ea;font:600 12px Inter,system-ui,sans-serif;cursor:pointer}.uas-consent-actions button:hover,.uas-consent-actions button:focus-visible{border-color:#a8e4b9;background:rgba(112,210,143,.1);outline:none}
    #uas-analytics-choices{position:fixed;z-index:2147483645;left:max(10px,env(safe-area-inset-left));bottom:max(10px,env(safe-area-inset-bottom));padding:6px 9px;border:1px solid #3a3a30;border-radius:999px;background:rgba(21,21,18,.94);color:#c2beb4;font:600 11px Inter,system-ui,sans-serif;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.2)}#uas-analytics-choices:hover,#uas-analytics-choices:focus-visible{color:#fff;border-color:#8ee6b0;outline:none}
    @media(max-width:520px){#uas-analytics-consent{bottom:max(8px,env(safe-area-inset-bottom));right:12px;width:calc(100vw - 24px);padding:12px}.uas-consent-actions button{min-height:36px}}
  `;
  let analyticsStarted = false;
  let banner;
  let choicesButton;

  function readChoice() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (_) {
      return null;
    }
  }

  function saveChoice(choice) {
    try {
      localStorage.setItem(STORAGE_KEY, choice);
    } catch (_) {
      // A blocked storage API simply means the visitor is asked again next visit.
    }
  }

  function privacyUrl() {
    return document.documentElement.getAttribute("data-analytics-privacy-url") || "/privacy/";
  }

  function loadGoogleAnalytics() {
    if (document.getElementById("uas-ga4-loader")) return;

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag("consent", "default", {
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      analytics_storage: "denied",
    });
    window.gtag("consent", "update", { analytics_storage: "granted" });
    window.gtag("js", new Date());
    window.gtag("config", MEASUREMENT_ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });

    const tag = document.createElement("script");
    tag.id = "uas-ga4-loader";
    tag.async = true;
    tag.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(MEASUREMENT_ID);
    tag.referrerPolicy = "strict-origin-when-cross-origin";
    document.head.appendChild(tag);
  }

  function startFirstPartyAnalytics() {
    const deferred = document.getElementById("uas-first-party-analytics");
    if (!deferred || deferred.dataset.started === "true") return;

    deferred.dataset.started = "true";
    const script = document.createElement("script");
    script.text = deferred.textContent;
    document.body.appendChild(script);
  }

  function startAnalytics() {
    if (analyticsStarted) return;
    analyticsStarted = true;
    loadGoogleAnalytics();
    startFirstPartyAnalytics();
  }

  function eraseAnalyticsCookies() {
    const expired = "expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; path=/; SameSite=Lax";
    const domains = [location.hostname, "." + location.hostname];
    document.cookie.split(";").forEach((item) => {
      const name = item.trim().split("=")[0];
      if (!/^_(?:ga|gid)(?:_|$)/i.test(name)) return;
      document.cookie = name + "=; " + expired;
      domains.forEach((domain) => {
        document.cookie = name + "=; " + expired + "; domain=" + domain;
      });
    });
  }

  function revokeAnalytics() {
    if (window.gtag) {
      window.gtag("consent", "update", {
        ad_storage: "denied",
        ad_user_data: "denied",
        ad_personalization: "denied",
        analytics_storage: "denied",
      });
    }
    eraseAnalyticsCookies();
  }

  function setControls(choice) {
    const isGranted = choice === "granted";
    banner.querySelector("[data-consent-status]").textContent = isGranted
      ? "Analytics are on. You can turn them off at any time."
      : "Analytics are off. You can enable them at any time.";
    banner.querySelector("[data-reject]").textContent = isGranted ? "Turn off analytics" : "No thanks";
    banner.querySelector("[data-allow]").textContent = isGranted ? "Keep analytics on" : "Allow analytics";
  }

  function hideBanner() {
    banner.hidden = true;
    choicesButton.hidden = false;
  }

  function choose(choice) {
    const wasGranted = readChoice() === "granted" || analyticsStarted;
    saveChoice(choice);

    if (choice === "granted") {
      startAnalytics();
    } else {
      revokeAnalytics();
    }

    hideBanner();
    if (choice === "denied" && wasGranted) {
      window.setTimeout(() => window.location.reload(), 25);
    }
  }

  function showChoices() {
    const choice = readChoice();
    if (choice) {
      setControls(choice);
    }
    choicesButton.hidden = true;
    banner.hidden = false;
  }

  function createInterface() {
    const style = document.createElement("style");
    style.id = "uas-analytics-consent-style";
    style.textContent = CSS;
    document.head.appendChild(style);

    banner = document.createElement("section");
    banner.id = "uas-analytics-consent";
    banner.hidden = true;
    banner.setAttribute("aria-labelledby", "uas-analytics-consent-title");
    banner.innerHTML =
      '<div class="uas-consent-copy">' +
        '<strong id="uas-analytics-consent-title">Help improve this site?</strong>' +
        '<p data-consent-status>Optional analytics show us which guides and tools need work. No ads or data sale. <a href="' + privacyUrl() + '">Privacy</a></p>' +
      "</div>" +
      '<div class="uas-consent-actions">' +
        '<button type="button" data-reject>No thanks</button>' +
        '<button type="button" data-allow>Allow analytics</button>' +
      "</div>";
    banner.querySelector("[data-reject]").addEventListener("click", () => choose("denied"));
    banner.querySelector("[data-allow]").addEventListener("click", () => choose("granted"));

    choicesButton = document.createElement("button");
    choicesButton.id = "uas-analytics-choices";
    choicesButton.type = "button";
    choicesButton.textContent = "Privacy choices";
    choicesButton.setAttribute("aria-label", "Change analytics privacy choices");
    choicesButton.addEventListener("click", showChoices);

    document.body.append(banner, choicesButton);
  }

  function initialise() {
    createInterface();
    const choice = readChoice();
    if (choice === "granted") {
      startAnalytics();
      choicesButton.hidden = false;
      return;
    }
    if (choice === "denied") {
      choicesButton.hidden = false;
      return;
    }
    showChoices();
  }

  window.UASAnalyticsConsent = Object.freeze({ showChoices });
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialise, { once: true });
  } else {
    initialise();
  }
})();
