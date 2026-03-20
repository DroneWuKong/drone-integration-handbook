/**
 * AI Wingman Analytics — Netlify Function Event Receiver
 * 
 * Serverless endpoint: /.netlify/functions/analytics-ingest
 * Storage: Netlify Blobs (free tier: 1GB storage, 10K reads/day)
 * 
 * Deploy this function on EITHER the Handbook or Forge site
 * (or a dedicated analytics site). Both sites point to the same endpoint.
 */

const ALLOWED_ORIGINS = [
  'https://nvmilldoitmyself.com',
  'https://www.nvmilldoitmyself.com',
  'https://forgeprole.netlify.app',
  'https://geprole.netlify.app',
  'http://localhost:3000',
  'http://localhost:8888',
  'https://thebluefairy.netlify.app',
];

// In-memory buffer — Netlify Functions are ephemeral, so we write to Blobs on each invocation
// For higher volume, swap to a proper DB (Supabase, PlanetScale, Turso)

export default async (req, context) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: corsHeaders(req),
    });
  }

  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
    });
  }

  try {
    const body = await req.json();
    const { events } = body;

    if (!Array.isArray(events) || events.length === 0) {
      return new Response(JSON.stringify({ error: 'events array required' }), {
        status: 400,
        headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
      });
    }

    // Validate and sanitize
    const valid = events.filter(e =>
      e.event_id && e.timestamp && e.surface && e.event_type && e.event_action
    ).map(e => ({
      event_id: e.event_id,
      timestamp: e.timestamp,
      surface: e.surface,
      event_type: e.event_type,
      event_action: e.event_action,
      session_id: e.context?.session_id || null,
      geo_region: e.context?.geo_region || null,
      platform: e.context?.platform || null,
      collection_tier: e.data_policy?.collection_tier || 'anonymous',
      payload: e.payload || {},
    }));

    if (valid.length === 0) {
      return new Response(JSON.stringify({ accepted: 0, rejected: events.length }), {
        status: 200,
        headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
      });
    }

    // Store using Netlify Blobs
    const { getStore } = await import("@netlify/blobs");
    const store = getStore("analytics-events");

    // Write events as a batch blob keyed by timestamp
    const batchKey = `batch_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    await store.setJSON(batchKey, {
      received_at: new Date().toISOString(),
      event_count: valid.length,
      events: valid,
    });

    // Also append to daily aggregate blob for fast dashboard reads
    const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    const dailyKey = `daily_${today}`;
    
    let dailyData;
    try {
      dailyData = await store.get(dailyKey, { type: 'json' });
    } catch {
      dailyData = null;
    }

    if (!dailyData) {
      dailyData = {
        date: today,
        handbook: { views: 0, searches: 0, sessions: new Set(), top_paths: {}, top_queries: {} },
        forge: { views: 0, searches: 0, filters: 0, compares: 0, saves: 0, sessions: new Set(), top_pids: {}, gaps: {} },
      };
    }

    // Convert Sets back from arrays (JSON serialization loses Set)
    if (Array.isArray(dailyData.handbook?.sessions)) {
      dailyData.handbook.sessions = new Set(dailyData.handbook.sessions);
    }
    if (Array.isArray(dailyData.forge?.sessions)) {
      dailyData.forge.sessions = new Set(dailyData.forge.sessions);
    }

    // Aggregate
    for (const e of valid) {
      if (e.surface === 'handbook') {
        const hb = dailyData.handbook;
        if (e.session_id) hb.sessions.add(e.session_id);
        if (e.event_action === 'view') {
          hb.views++;
          const path = e.payload?.path || 'unknown';
          hb.top_paths[path] = (hb.top_paths[path] || 0) + 1;
        }
        if (e.event_action === 'search') {
          hb.searches++;
          const q = e.payload?.query || '';
          hb.top_queries[q] = (hb.top_queries[q] || 0) + 1;
        }
      }

      if (e.surface === 'forge') {
        const fg = dailyData.forge;
        if (e.session_id) fg.sessions.add(e.session_id);
        if (e.event_action === 'component_detail') {
          fg.views++;
          const pid = e.payload?.component_pid || 'unknown';
          fg.top_pids[pid] = (fg.top_pids[pid] || 0) + 1;
        }
        if (e.event_action === 'component_search') fg.searches++;
        if (e.event_action === 'apply_filter') fg.filters++;
        if (e.event_action === 'side_by_side') fg.compares++;
        if (e.event_action === 'bookmark_component') fg.saves++;
        if (e.event_action === 'no_results') {
          const q = e.payload?.query || '';
          fg.gaps[q] = (fg.gaps[q] || 0) + 1;
        }
      }
    }

    // Serialize Sets as arrays for JSON storage
    const serializable = {
      ...dailyData,
      handbook: {
        ...dailyData.handbook,
        sessions: [...(dailyData.handbook?.sessions || [])],
      },
      forge: {
        ...dailyData.forge,
        sessions: [...(dailyData.forge?.sessions || [])],
      },
    };

    await store.setJSON(dailyKey, serializable);

    return new Response(JSON.stringify({ accepted: valid.length, rejected: events.length - valid.length }), {
      status: 200,
      headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
    });

  } catch (err) {
    console.error('[analytics] ingest error:', err);
    return new Response(JSON.stringify({ error: 'internal', message: err.message }), {
      status: 500,
      headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
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

export const config = {
  path: "/.netlify/functions/analytics-ingest",
};
