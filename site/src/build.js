/**
 * The Drone Integration Handbook — Static Site Generator
 * Public edition. Converts handbook markdown into a browsable HTML site.
 * Output: site/dist/
 */

const fs = require("fs");
const path = require("path");
const { marked } = require("marked");

// ── Paths (relative to repo root, not docs/handbook/) ──
const ROOT_DIR = path.resolve(__dirname, "../..");
const OUT_DIR = path.resolve(__dirname, "../dist");

// ── Handbook structure ──
const TOC = [
  {
    part: "RF Fundamentals",
    chapters: [
      { file: "fundamentals/five-link-types.md", title: "The Five Link Types", num: 1 },
      { file: "fundamentals/frequency-bands.md", title: "Frequency Bands", num: 2 },
      { file: "fundamentals/antennas.md", title: "Antennas", num: 3 },
      { file: "fundamentals/link-budgets.md", title: "Link Budgets", num: 4 },
    ],
  },
  {
    part: "Flight Controller Firmware",
    chapters: [
      { file: "firmware/four-firmwares.md", title: "The Four Firmwares", num: 5 },
      { file: "firmware/msp-protocol.md", title: "MSP Protocol", num: 6 },
      { file: "firmware/mavlink-protocol.md", title: "MAVLink Protocol", num: 7 },
      { file: "firmware/uart-layout.md", title: "UART Layout", num: 8 },
    ],
  },
  {
    part: "Field Operations",
    chapters: [
      { file: "field/preflight.md", title: "Pre-Flight Checklist", num: 9 },
      { file: "field/blackbox.md", title: "Blackbox Logs", num: 10 },
      { file: "field/pid-tuning.md", title: "PID Tuning", num: 11 },
      { file: "field/troubleshooting.md", title: "Troubleshooting", num: 12 },
      { file: "field/unsolved-problems.md", title: "Unsolved Problems", num: 13 },
    ],
  },
  {
    part: "Integration",
    chapters: [
      { file: "integration/companion.md", title: "Companion Computers", num: 14 },
      { file: "integration/mesh-radios.md", title: "Mesh Radios", num: 15 },
      { file: "integration/tak.md", title: "TAK Integration", num: 16 },
    ],
  },
  {
    part: "Components",
    chapters: [
      { file: "components/flight-controllers.md", title: "Flight Controllers", num: 17 },
      { file: "components/escs.md", title: "ESCs", num: 18 },
      { file: "components/motors.md", title: "Motors", num: 19 },
      { file: "components/batteries.md", title: "Batteries", num: 20 },
      { file: "components/comms-datalinks.md", title: "Comms & Datalinks", num: 21 },
      { file: "components/companion-computers.md", title: "Companion Computers", num: 22 },
      { file: "components/thermal-cameras.md", title: "Thermal Cameras", num: 23 },
      { file: "components/propulsion-non-electric.md", title: "Non-Electric Propulsion", num: 24 },
      { file: "components/counter-uas.md", title: "Counter-UAS", num: 25 },
      { file: "components/platforms-global.md", title: "Global Platforms", num: 26 },
    ],
  },
];

// ── Platform profiles ──
const PLATFORM_CATEGORIES = [
  { dir: "platforms/blue-uas", label: "Blue UAS / NDAA" },
  { dir: "platforms/cots", label: "COTS" },
  { dir: "platforms/tactical", label: "Tactical" },
  { dir: "platforms/open-source", label: "Open Source" },
];

// ── Helpers ──
function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function slugify(title) {
  return title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function readMarkdown(filepath) {
  try {
    return fs.readFileSync(filepath, "utf8");
  } catch (e) {
    console.warn(`⚠ Missing: ${filepath}`);
    return `# File Not Found\n\nExpected: \`${filepath}\``;
  }
}

// ── Configure marked ──
marked.setOptions({ gfm: true, breaks: false });

// ── CSS (matches Ai-Project / thebluefairy visual identity) ──
const CSS = `
:root {
  --teal: #4ECDC4;
  --teal-dim: #3BA99E;
  --teal-glow: rgba(78, 205, 196, 0.15);
  --bg: #0B0F14;
  --bg-card: #111820;
  --bg-nav: #0D1117;
  --text: #C9D1D9;
  --text-dim: #8B949E;
  --text-bright: #E6EDF3;
  --border: #21262D;
  --code-bg: #161B22;
  --danger: #F85149;
  --warning: #D29922;
  --success: #3FB950;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

@font-face {
  font-family: 'JetBrains Mono';
  src: url('https://cdn.jsdelivr.net/gh/JetBrains/JetBrainsMono@2.304/fonts/webfonts/JetBrainsMono-Regular.woff2') format('woff2');
  font-weight: 400; font-display: swap;
}
@font-face {
  font-family: 'JetBrains Mono';
  src: url('https://cdn.jsdelivr.net/gh/JetBrains/JetBrainsMono@2.304/fonts/webfonts/JetBrainsMono-Bold.woff2') format('woff2');
  font-weight: 700; font-display: swap;
}
@font-face {
  font-family: 'Outfit';
  src: url('https://fonts.gstatic.com/s/outfit/v11/QGYyz_MVcBeNP4NjuGObqx1XmO1I4TC0C4G-EiAou6Y.woff2') format('woff2');
  font-weight: 300 800; font-display: swap;
}

html { scroll-behavior: smooth; }

body {
  font-family: 'Outfit', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
}

.site-wrapper { display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }

/* Sidebar */
.sidebar {
  background: var(--bg-nav); border-right: 1px solid var(--border);
  padding: 2rem 0; position: sticky; top: 0; height: 100vh;
  overflow-y: auto; scrollbar-width: thin; scrollbar-color: var(--border) transparent;
}
.sidebar-header { padding: 0 1.5rem 1.5rem; border-bottom: 1px solid var(--border); margin-bottom: 1rem; }
.sidebar-header h1 { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 700; color: var(--teal); letter-spacing: -0.02em; }
.sidebar-header .tagline { font-size: 0.75rem; color: var(--text-dim); margin-top: 0.25rem; font-style: italic; }
.nav-section { padding: 0.75rem 1.5rem 0.25rem; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--text-dim); }
.nav-link { display: block; padding: 0.4rem 1.5rem 0.4rem 2rem; color: var(--text); text-decoration: none; font-size: 0.875rem; transition: all 0.15s; border-left: 2px solid transparent; }
.nav-link:hover { color: var(--teal); background: var(--teal-glow); border-left-color: var(--teal); }
.nav-link.active { color: var(--teal); border-left-color: var(--teal); background: var(--teal-glow); font-weight: 600; }
.nav-link .ch-num { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--text-dim); margin-right: 0.5rem; }
.nav-divider { height: 1px; background: var(--border); margin: 0.75rem 1.5rem; }

/* Main */
.main-content { padding: 3rem 4rem 6rem; max-width: 52rem; }
.main-content h1 { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 700; color: var(--teal); margin-bottom: 0.5rem; letter-spacing: -0.03em; }
.main-content h2 { font-size: 1.4rem; font-weight: 700; color: var(--text-bright); margin: 2.5rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
.main-content h3 { font-size: 1.1rem; font-weight: 600; color: var(--text-bright); margin: 2rem 0 0.75rem; }
.main-content h4 { font-size: 0.95rem; font-weight: 600; color: var(--teal-dim); margin: 1.5rem 0 0.5rem; }
.main-content p { margin-bottom: 1rem; color: var(--text); }
.main-content a { color: var(--teal); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color 0.15s; }
.main-content a:hover { border-bottom-color: var(--teal); }
.main-content ul, .main-content ol { margin: 0 0 1rem 1.5rem; }
.main-content li { margin-bottom: 0.4rem; }
.main-content strong { color: var(--text-bright); font-weight: 600; }
.main-content em { color: var(--text-dim); }
.main-content blockquote { border-left: 3px solid var(--teal); padding: 0.75rem 1.25rem; margin: 1.5rem 0; background: var(--teal-glow); border-radius: 0 6px 6px 0; }
.main-content blockquote p { margin-bottom: 0; color: var(--text-bright); }
.main-content code { font-family: 'JetBrains Mono', monospace; font-size: 0.85em; background: var(--code-bg); padding: 0.15em 0.4em; border-radius: 4px; color: var(--teal); }
.main-content pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; overflow-x: auto; margin: 1.5rem 0; }
.main-content pre code { background: none; padding: 0; font-size: 0.85rem; color: var(--text); }
.main-content table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.9rem; }
.main-content th { background: var(--code-bg); color: var(--teal); font-weight: 600; text-align: left; padding: 0.75rem 1rem; border: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
.main-content td { padding: 0.6rem 1rem; border: 1px solid var(--border); }
.main-content tr:hover { background: rgba(78, 205, 196, 0.04); }
.main-content hr { border: none; border-top: 1px solid var(--border); margin: 2.5rem 0; }

/* Chapter nav */
.chapter-nav { display: flex; justify-content: space-between; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border); }
.chapter-nav a { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; color: var(--text); text-decoration: none; font-size: 0.875rem; transition: all 0.15s; }
.chapter-nav a:hover { border-color: var(--teal); color: var(--teal); }

/* Feedback */
.feedback-section { margin-top: 4rem; padding: 2rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; }
.feedback-section h3 { font-family: 'JetBrains Mono', monospace; color: var(--teal); font-size: 1rem; margin-bottom: 1rem; }
.feedback-section textarea { width: 100%; min-height: 100px; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1rem; color: var(--text); font-family: 'Outfit', system-ui, sans-serif; font-size: 0.9rem; resize: vertical; transition: border-color 0.15s; }
.feedback-section textarea:focus { outline: none; border-color: var(--teal); }
.feedback-section button { margin-top: 0.75rem; padding: 0.6rem 1.5rem; background: var(--teal); color: var(--bg); border: none; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: opacity 0.15s; }
.feedback-section button:hover { opacity: 0.85; }

/* Home */
.hero { padding: 2rem 0 3rem; }
.hero h1 { font-size: 2.5rem; line-height: 1.2; }
.hero .subtitle { font-size: 1.1rem; color: var(--text-dim); margin-top: 0.5rem; font-style: italic; }
.hero .description { margin-top: 1.5rem; font-size: 1rem; max-width: 40rem; }
.toc-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin: 2rem 0; }
.toc-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 1.25rem; transition: border-color 0.15s; text-decoration: none; display: block; color: inherit; }
.toc-card:hover { border-color: var(--teal); }
.toc-card h4 { font-family: 'JetBrains Mono', monospace; color: var(--teal); font-size: 0.9rem; margin: 0 0 0.5rem; }
.toc-card p { font-size: 0.85rem; color: var(--text-dim); margin: 0; }
.toc-card .ch-list { list-style: none; margin: 0.5rem 0 0; padding: 0; }
.toc-card .ch-list li { font-size: 0.8rem; color: var(--text-dim); padding: 0.15rem 0; }
.toc-card .ch-list li a { color: var(--text); text-decoration: none; }
.toc-card .ch-list li a:hover { color: var(--teal); }

/* Platform list */
.platform-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0.75rem; margin: 1rem 0 2rem; }
.platform-link { display: block; padding: 0.6rem 1rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; color: var(--text); text-decoration: none; font-size: 0.875rem; transition: all 0.15s; }
.platform-link:hover { border-color: var(--teal); color: var(--teal); }

/* Mobile */
.mobile-header { display: none; background: var(--bg-nav); border-bottom: 1px solid var(--border); padding: 1rem 1.5rem; position: sticky; top: 0; z-index: 100; }
.mobile-header h1 { font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: var(--teal); }
.menu-toggle { background: none; border: 1px solid var(--border); border-radius: 6px; color: var(--text); padding: 0.4rem 0.75rem; font-size: 0.85rem; cursor: pointer; }

@media (max-width: 768px) {
  .site-wrapper { grid-template-columns: 1fr; }
  .sidebar { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 200; height: 100vh; }
  .sidebar.open { display: block; }
  .mobile-header { display: flex; justify-content: space-between; align-items: center; }
  .main-content { padding: 2rem 1.5rem 4rem; }
  .main-content h1 { font-size: 1.5rem; }
  .sidebar-close { display: block; padding: 1rem 1.5rem; text-align: right; }
  .sidebar-close button { background: none; border: 1px solid var(--border); border-radius: 6px; color: var(--text); padding: 0.4rem 0.75rem; font-size: 0.85rem; cursor: pointer; }
}
@media (min-width: 769px) { .sidebar-close { display: none; } }
`;

// ── Analytics snippet ──
const ANALYTICS_SNIPPET = `
<!-- AI Wingman Analytics v1.0 — No cookies, no PII -->
<script>
(function(){var E='https://nvmilldoitmyself.com/.netlify/functions/analytics-ingest',S='sess_'+crypto.randomUUID().replace(/-/g,'').slice(0,16),T=Date.now(),q=[],t=null;function r(){try{var z=Intl.DateTimeFormat().resolvedOptions().timeZone;if(z.includes('America'))return'Americas';if(z.includes('Europe'))return'Europe';if(z.includes('Asia')||z.includes('Australia')||z.includes('Pacific'))return'Asia-Pacific';if(z.includes('Africa'))return'Africa'}catch(e){}return'Unknown'}function ev(tp,ac,p){q.push({event_id:crypto.randomUUID(),timestamp:new Date().toISOString(),surface:'handbook',event_type:tp,event_action:ac,context:{session_id:S,account_id:null,geo_region:r(),platform:/Android|iPhone|iPad/i.test(navigator.userAgent)?'mobile':'web',viewport:innerWidth+'x'+innerHeight},payload:p,data_policy:{collection_tier:'anonymous',consent_version:'none',retention_days:90,anonymized:true}});if(q.length>=20)fl();else if(!t)t=setTimeout(fl,5e3)}function fl(){if(t){clearTimeout(t);t=null}if(!q.length)return;var b=q.splice(0);fetch(E,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({events:b}),keepalive:true}).catch(function(){})}var P=location.pathname,sc=P.split('/').filter(Boolean)[0]||'home';ev('page_view','view',{path:P,title:document.title,section:sc,referrer:document.referrer?new URL(document.referrer).hostname:'direct'});var ds=[25,50,75,100],ht=new Set;addEventListener('scroll',function(){var pct=Math.round(scrollY/(document.body.scrollHeight-innerHeight)*100),el=(Date.now()-T)/1e3;ds.forEach(function(d){if(pct>=d&&!ht.has(d)){ht.add(d);ev('engagement','scroll_depth',{path:P,depth_pct:d,time_on_page_sec:Math.round(el)})}})},{passive:true});document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a)return;try{var u=new URL(a.href);if(u.hostname!==location.hostname)ev('click','outbound_link',{from_path:P,to_domain:u.hostname,link_text:a.textContent.trim().slice(0,100)})}catch(e){}});addEventListener('visibilitychange',function(){if(document.visibilityState==='hidden'){ev('engagement','time_on_page',{path:P,duration_sec:Math.round((Date.now()-T)/1e3),deep_read:(Date.now()-T)>12e4});fl()}});addEventListener('pagehide',fl);window.__wingmanAnalytics={search:function(q,n){ev('search','search',{query:q.slice(0,200),result_count:n,had_results:n>0})},flush:fl}})();
</script>`;

// ── Sidebar nav ──
function buildNav(activePage) {
  let nav = "";
  nav += `<a class="nav-link${activePage === "index" ? " active" : ""}" href="index.html">Home</a>\n`;
  nav += `<div class="nav-divider"></div>\n`;

  for (const part of TOC) {
    nav += `<div class="nav-section">${part.part}</div>\n`;
    for (const ch of part.chapters) {
      const slug = slugify(ch.title);
      const isActive = activePage === slug;
      nav += `<a class="nav-link${isActive ? " active" : ""}" href="${slug}.html"><span class="ch-num">${String(ch.num).padStart(2, "0")}</span>${ch.title}</a>\n`;
    }
  }

  nav += `<div class="nav-divider"></div>\n`;
  nav += `<div class="nav-section">Platform Profiles</div>\n`;
  nav += `<a class="nav-link${activePage === "platforms" ? " active" : ""}" href="platforms.html">All Platforms</a>\n`;

  nav += `<div class="nav-divider"></div>\n`;
  nav += `<a class="nav-link" href="https://forgeprole.netlify.app" target="_blank">Forge ↗</a>\n`;
  nav += `<a class="nav-link${activePage === "feedback" ? " active" : ""}" href="feedback.html">Feedback</a>\n`;

  return nav;
}

// ── Page template ──
function wrapPage(title, content, activePage) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — The Drone Integration Handbook</title>
  <style>${CSS}</style>
</head>
<body>
  <div class="mobile-header">
    <h1>Drone Handbook</h1>
    <button class="menu-toggle" onclick="document.querySelector('.sidebar').classList.toggle('open')">Menu</button>
  </div>
  <div class="site-wrapper">
    <nav class="sidebar">
      <div class="sidebar-close"><button onclick="document.querySelector('.sidebar').classList.remove('open')">Close</button></div>
      <div class="sidebar-header">
        <h1>Drone Integration Handbook</h1>
        <div class="tagline">Built by operators, for operators.</div>
      </div>
      ${buildNav(activePage)}
    </nav>
    <main class="main-content">
      ${content}
    </main>
  </div>
${ANALYTICS_SNIPPET}
</body>
</html>`;
}

// ── Chapter prev/next nav ──
function getChapterNav(currentNum) {
  const allChapters = TOC.flatMap((p) => p.chapters);
  const idx = allChapters.findIndex((c) => c.num === currentNum);
  const prev = idx > 0 ? allChapters[idx - 1] : null;
  const next = idx < allChapters.length - 1 ? allChapters[idx + 1] : null;

  let html = '<div class="chapter-nav">';
  if (prev) {
    html += `<a href="${slugify(prev.title)}.html">\u2190 ${String(prev.num).padStart(2, "0")}. ${prev.title}</a>`;
  } else {
    html += "<span></span>";
  }
  if (next) {
    html += `<a href="${slugify(next.title)}.html">${String(next.num).padStart(2, "0")}. ${next.title} \u2192</a>`;
  } else {
    html += "<span></span>";
  }
  html += "</div>";
  return html;
}

// ── Discover platform profiles ──
function discoverPlatforms() {
  const platforms = [];
  for (const cat of PLATFORM_CATEGORIES) {
    const dir = path.join(ROOT_DIR, cat.dir);
    if (!fs.existsSync(dir)) continue;
    const files = fs.readdirSync(dir).filter((f) => f.endsWith(".md") && f !== "README.md").sort();
    for (const file of files) {
      const name = file.replace(".md", "").split("-").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
      platforms.push({
        file: path.join(cat.dir, file),
        name,
        category: cat.label,
        slug: "platform-" + slugify(name),
      });
    }
  }
  return platforms;
}

// ══════════════════════════════════════════
// BUILD
// ══════════════════════════════════════════
function build() {
  ensureDir(OUT_DIR);

  const platforms = discoverPlatforms();

  // ── Home page ──
  let tocCards = "";
  for (const part of TOC) {
    let chList = "";
    for (const ch of part.chapters) {
      chList += `<li><a href="${slugify(ch.title)}.html">${String(ch.num).padStart(2, "0")}. ${ch.title}</a></li>`;
    }
    tocCards += `
      <div class="toc-card">
        <h4>${part.part}</h4>
        <ul class="ch-list">${chList}</ul>
      </div>`;
  }

  const homeContent = `
    <div class="hero">
      <h1>The Drone Integration Handbook</h1>
      <div class="subtitle">Built by operators, for operators.</div>
      <div class="description">
        <p>A practical reference for anyone integrating, operating, or troubleshooting
        multi-platform drone systems. No vendor lock-in. No marketing fluff. Just field-tested
        knowledge from people who actually fly.</p>
      </div>
    </div>

    <h2>Chapters</h2>
    <div class="toc-grid">${tocCards}</div>

    <h2>Platform Profiles</h2>
    <p>${platforms.length} platforms documented across Blue UAS, COTS, tactical, and open-source categories.</p>
    <p><a href="platforms.html">Browse all platforms &rarr;</a></p>

    <h2>Tools</h2>
    <div class="toc-grid">
      <a href="https://forgeprole.netlify.app" target="_blank" class="toc-card">
        <h4>Forge ↗</h4>
        <p>Component browser, model builder, build guide, FPV academy. 3,300+ parts across 16 categories.</p>
      </a>
      <a href="feedback.html" class="toc-card">
        <h4>Feedback</h4>
        <p>Found something wrong? Know something we don't? Tell us.</p>
      </a>
    </div>

    <hr>
    <p style="color: var(--text-dim); font-style: italic; text-align: center; margin-top: 2rem;">Buddy up.</p>
  `;
  fs.writeFileSync(path.join(OUT_DIR, "index.html"), wrapPage("Home", homeContent, "index"));
  console.log("✓ index.html");

  // ── Handbook chapters ──
  for (const part of TOC) {
    for (const ch of part.chapters) {
      const slug = slugify(ch.title);
      const md = readMarkdown(path.join(ROOT_DIR, ch.file));
      const html = marked.parse(md);
      const content = `
        <p style="color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">
          Chapter ${ch.num} · ${part.part}
        </p>
        ${html}
        ${getChapterNav(ch.num)}
      `;
      fs.writeFileSync(path.join(OUT_DIR, `${slug}.html`), wrapPage(ch.title, content, slug));
      console.log(`✓ ${slug}.html`);
    }
  }

  // ── Platforms index page ──
  let platformsContent = `<h1>Platform Profiles</h1>
    <p>Detailed breakdowns of ${platforms.length} drone platforms across four categories.</p>`;

  const byCat = {};
  for (const p of platforms) {
    if (!byCat[p.category]) byCat[p.category] = [];
    byCat[p.category].push(p);
  }
  for (const cat of PLATFORM_CATEGORIES) {
    const list = byCat[cat.label] || [];
    if (list.length === 0) continue;
    platformsContent += `<h2>${cat.label} (${list.length})</h2><div class="platform-grid">`;
    for (const p of list) {
      platformsContent += `<a class="platform-link" href="${p.slug}.html">${p.name}</a>`;
    }
    platformsContent += `</div>`;
  }
  fs.writeFileSync(path.join(OUT_DIR, "platforms.html"), wrapPage("Platforms", platformsContent, "platforms"));
  console.log("✓ platforms.html");

  // ── Individual platform pages ──
  for (const p of platforms) {
    const md = readMarkdown(path.join(ROOT_DIR, p.file));
    const html = marked.parse(md);
    const content = `
      <p style="color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">
        Platform Profile · ${p.category}
      </p>
      ${html}
      <div class="chapter-nav">
        <a href="platforms.html">\u2190 All Platforms</a>
        <span></span>
      </div>
    `;
    fs.writeFileSync(path.join(OUT_DIR, `${p.slug}.html`), wrapPage(p.name, content, p.slug));
    console.log(`✓ ${p.slug}.html`);
  }

  // ── Feedback page ──
  const feedbackContent = `
    <h1>Feedback</h1>
    <p>This handbook is built by operators, for operators. If you've got corrections, field experience,
    platform knowledge, or just want to tell us what's missing — we want to hear it.</p>
    <p>No login required. No tracking. Just a text box.</p>

    <div class="feedback-section">
      <h3>// drop a note</h3>
      <form name="feedback" method="POST" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="feedback">
        <p style="display:none"><label>Don't fill this out: <input name="bot-field"></label></p>
        <div style="margin-bottom: 1rem;">
          <label style="display: block; font-size: 0.85rem; color: var(--text-dim); margin-bottom: 0.4rem;">
            What chapter or topic? (optional)
          </label>
          <input type="text" name="topic" placeholder="e.g. PID Tuning, Mesh Radios, general"
            style="width: 100%; background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
            padding: 0.6rem 1rem; color: var(--text); font-family: 'Outfit', system-ui, sans-serif; font-size: 0.9rem;">
        </div>
        <textarea name="message" placeholder="What did we get wrong? What's missing? What would help you in the field?" required></textarea>
        <div style="margin-top: 0.75rem;">
          <label style="display: block; font-size: 0.85rem; color: var(--text-dim); margin-bottom: 0.4rem;">
            Name or callsign (optional)
          </label>
          <input type="text" name="name" placeholder="Anonymous is fine"
            style="width: 100%; background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
            padding: 0.6rem 1rem; color: var(--text); font-family: 'Outfit', system-ui, sans-serif; font-size: 0.9rem;">
        </div>
        <button type="submit">Send Feedback</button>
      </form>
    </div>

    <hr>
    <p style="color: var(--text-dim); font-style: italic; text-align: center; margin-top: 2rem;">Buddy up.</p>
  `;
  fs.writeFileSync(path.join(OUT_DIR, "feedback.html"), wrapPage("Feedback", feedbackContent, "feedback"));
  console.log("✓ feedback.html");

  // ── Count ──
  const files = fs.readdirSync(OUT_DIR).filter((f) => f.endsWith(".html"));
  console.log(`\n✅ Built ${files.length} pages → site/dist/`);
}

build();
