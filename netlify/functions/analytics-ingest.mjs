/**
 * AI Wingman Analytics — Handbook Ingest
 * Endpoint: uas-handbook.com/.netlify/functions/analytics-ingest
 *
 * Receives events from handbook pages (same-origin).
 * Writes to thebluefairy's analytics-events Blobs store via cross-site access.
 * Requires on the handbook Netlify site:
 *   ANALYTICS_SITE_ID  — thebluefairy site ID
 *   NETLIFY_API_TOKEN  — Netlify personal access token
 */

const ALLOWED_ORIGINS = [
  // New canonical uas-* domain (primary going forward)
  'https://uas-handbook.com',
  'https://www.uas-handbook.com',
  // Legacy domains — keep during transition window
  'https://nvmilldoitmyself.com',
  'https://www.nvmilldoitmyself.com',
  'https://illdoitmyself.com',
  'https://www.illdoitmyself.com',
  'http://localhost:8888',
  'http://localhost:3000',
];

export default async (req, context) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders(req) });
  }
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405, headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
    });
  }

  try {
    const body = await req.json();
    const events = Array.isArray(body.events) ? body.events : [];
    if (!events.length) {
      return new Response(JSON.stringify({ accepted: 0 }), {
        status: 200, headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
      });
    }

    const valid = events.filter(e =>
      e.event_id && e.timestamp && e.surface && e.event_type && e.event_action
    ).map(e => ({
      event_id:     e.event_id,
      timestamp:    e.timestamp,
      surface:      e.surface,
      page:         e.page || null,
      event_type:   e.event_type,
      event_action: e.event_action,
      session_id:   e.context?.session_id || null,
      geo_region:   e.context?.geo_region || null,
      platform:     e.context?.platform || null,
      payload:      e.payload || {},
    }));

    if (!valid.length) {
      return new Response(JSON.stringify({ accepted: 0, rejected: events.length }), {
        status: 200, headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
      });
    }

    // Cross-site Blobs: write to thebluefairy's store
    let store;
    try {
      const blobs = await import('@netlify/blobs');
      const siteID = process.env.ANALYTICS_SITE_ID;
      const token  = process.env.NETLIFY_API_TOKEN;
      if (siteID && token) {
        store = blobs.getStore({ name: 'analytics-events', siteID, token });
      } else {
        store = blobs.getStore('analytics-events');
        console.warn('[ingest] ANALYTICS_SITE_ID or NETLIFY_API_TOKEN not set — writing to local store');
      }
    } catch (e) {
      return new Response(JSON.stringify({ accepted: valid.length, stored: false, error: e.message }), {
        status: 200, headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
      });
    }

    const today = new Date().toISOString().slice(0, 10);
    const month = today.slice(0, 7);

    // Raw archive
    try {
      let raw = [];
      try { raw = await store.get(`raw-hb-${today}`, { type: 'json' }) || []; } catch {}
      raw.push(...valid);
      if (raw.length > 5000) raw = raw.slice(-5000);
      await store.setJSON(`raw-hb-${today}`, raw);
    } catch (e) {
      console.warn('[ingest] raw archive failed:', e.message);
    }

    // Daily aggregate
    let d = null;
    try { d = await store.get(`daily_${today}`, { type: 'json' }); } catch {}
    if (!d) d = {
      date: today,
      handbook: {
        views: 0, searches: 0, scroll_25: 0, scroll_50: 0, scroll_75: 0, scroll_100: 0,
        outbound_clicks: 0, deep_reads: 0, sessions: [],
        top_paths: {}, top_queries: {}, top_outbound: {},
      },
      forge: { views: 0, sessions: [], pages: {}, searches: 0, filters: 0, compares: 0, no_results: 0, component_views: 0, tab_switches: 0, wingman_queries: 0, wingman_cats: {}, flag_views: 0, flag_severities: {}, intel_views: 0, intel_sources: {}, gap_queries: {}, top_pids: {}, top_tabs: {}, top_pages: {}, regions: {}, patterns: { views: 0, tab_switches: 0, flag_views: 0, wingman_queries: 0, intel_views: 0, top_tabs: {}, flag_severities: {}, flag_types: {}, flag_ids: {}, wingman_cats: {}, intel_sources: {} } },
    };

    const hbS = new Set(d.handbook.sessions || []);
    for (const e of valid) {
      const p = e.payload || {};
      if (e.surface === 'handbook') {
        const h = d.handbook;
        if (e.session_id) hbS.add(e.session_id);
        if (e.event_action === 'view')          { h.views++; const pt=p.path||'?'; h.top_paths[pt]=(h.top_paths[pt]||0)+1; }
        if (e.event_action === 'search')        { h.searches++; const qk=(p.query||'').toLowerCase().slice(0,100); if(qk) h.top_queries[qk]=(h.top_queries[qk]||0)+1; }
        if (e.event_action === 'scroll_depth')  { const dp=p.depth_pct; if(dp===25)h.scroll_25++; if(dp===50)h.scroll_50++; if(dp===75)h.scroll_75++; if(dp===100)h.scroll_100++; }
        if (e.event_action === 'outbound_link') { h.outbound_clicks++; const dom=p.to||p.to_domain||'?'; h.top_outbound[dom]=(h.top_outbound[dom]||0)+1; }
        if (e.event_action === 'time_on_page' && p.deep_read) h.deep_reads++;
      }
    }
    d.handbook.sessions = [...hbS];
    await store.setJSON(`daily_${today}`, d);

    // Monthly archive
    try {
      let arc = null;
      try { arc = await store.get(`archive-${month}`, { type: 'json' }); } catch {}
      if (!arc) arc = { month, forge: { views:0,sessions:0,flag_views:0,wingman_queries:0,intel_views:0,searches:0,tab_switches:0 }, handbook: { views:0,sessions:0,searches:0 } };
      arc.handbook.views    += d.handbook.views;
      arc.handbook.searches += d.handbook.searches;
      arc.handbook.sessions  = (arc.handbook.sessions||0) + hbS.size;
      arc.last_updated = new Date().toISOString();
      await store.setJSON(`archive-${month}`, arc);
    } catch (e) {
      console.warn('[ingest] monthly archive failed:', e.message);
    }

    return new Response(JSON.stringify({ accepted: valid.length, rejected: events.length - valid.length }), {
      status: 200, headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500, headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
    });
  }
};

function corsHeaders(req) {
  const origin = req.headers.get('origin') || '';
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

export const config = { path: '/.netlify/functions/analytics-ingest' };
