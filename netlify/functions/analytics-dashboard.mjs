/**
 * AI Wingman Analytics — Netlify Function Dashboard API
 * 
 * Serverless endpoint: /.netlify/functions/analytics-dashboard
 * Reads aggregated data from Netlify Blobs
 * 
 * Query params:
 *   ?surface=handbook|forge (default: handbook)
 *   ?days=7|14|30|90 (default: 7)
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

export default async (req, context) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders(req) });
  }

  try {
    const url = new URL(req.url);
    const surface = url.searchParams.get('surface') || 'handbook';
    const days = parseInt(url.searchParams.get('days')) || 7;

    const { getStore } = await import("@netlify/blobs");
    const store = getStore("analytics-events");

    // Collect daily aggregates for the requested period
    const dailyData = [];
    for (let i = 0; i < days; i++) {
      const date = new Date(Date.now() - i * 86400000).toISOString().slice(0, 10);
      const key = `daily_${date}`;
      try {
        const data = await store.get(key, { type: 'json' });
        if (data) dailyData.push(data);
      } catch {
        // No data for this day
      }
    }

    let dashboard;

    if (surface === 'handbook') {
      // Aggregate handbook metrics
      let totalViews = 0;
      let totalSearches = 0;
      const allSessions = new Set();
      const pathCounts = {};
      const queryCounts = {};

      for (const day of dailyData) {
        const hb = day.handbook || {};
        totalViews += hb.views || 0;
        totalSearches += hb.searches || 0;
        (hb.sessions || []).forEach(s => allSessions.add(s));
        for (const [path, count] of Object.entries(hb.top_paths || {})) {
          pathCounts[path] = (pathCounts[path] || 0) + count;
        }
        for (const [query, count] of Object.entries(hb.top_queries || {})) {
          queryCounts[query] = (queryCounts[query] || 0) + count;
        }
      }

      const topPages = Object.entries(pathCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .map(([path, views]) => ({ path, views }));

      const topSearches = Object.entries(queryCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .map(([query, searches]) => ({ query, searches }));

      dashboard = {
        surface: 'handbook',
        period_days: days,
        overview: {
          total_views: totalViews,
          total_searches: totalSearches,
          unique_sessions: allSessions.size,
          days_with_data: dailyData.length,
        },
        top_pages: topPages,
        top_searches: topSearches,
        daily_views: dailyData.map(d => ({
          date: d.date,
          views: d.handbook?.views || 0,
          searches: d.handbook?.searches || 0,
          sessions: (d.handbook?.sessions || []).length,
        })).reverse(),
      };

    } else if (surface === 'forge') {
      // Aggregate forge metrics
      let totalViews = 0;
      let totalSearches = 0;
      let totalFilters = 0;
      let totalCompares = 0;
      let totalSaves = 0;
      const allSessions = new Set();
      const pidCounts = {};
      const gapCounts = {};

      for (const day of dailyData) {
        const fg = day.forge || {};
        totalViews += fg.views || 0;
        totalSearches += fg.searches || 0;
        totalFilters += fg.filters || 0;
        totalCompares += fg.compares || 0;
        totalSaves += fg.saves || 0;
        (fg.sessions || []).forEach(s => allSessions.add(s));
        for (const [pid, count] of Object.entries(fg.top_pids || {})) {
          pidCounts[pid] = (pidCounts[pid] || 0) + count;
        }
        for (const [query, count] of Object.entries(fg.gaps || {})) {
          gapCounts[query] = (gapCounts[query] || 0) + count;
        }
      }

      const topComponents = Object.entries(pidCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .map(([pid, views]) => ({ pid, views }));

      const databaseGaps = Object.entries(gapCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .map(([query, occurrences]) => ({ query, occurrences }));

      dashboard = {
        surface: 'forge',
        period_days: days,
        overview: {
          total_views: totalViews,
          total_searches: totalSearches,
          total_filters: totalFilters,
          total_comparisons: totalCompares,
          total_saves: totalSaves,
          unique_sessions: allSessions.size,
          days_with_data: dailyData.length,
        },
        top_components: topComponents,
        database_gaps: databaseGaps,
        daily_activity: dailyData.map(d => ({
          date: d.date,
          views: d.forge?.views || 0,
          searches: d.forge?.searches || 0,
          filters: d.forge?.filters || 0,
          sessions: (d.forge?.sessions || []).length,
        })).reverse(),
      };
    } else {
      return new Response(JSON.stringify({ error: 'surface must be handbook or forge' }), {
        status: 400,
        headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify(dashboard), {
      status: 200,
      headers: { ...corsHeaders(req), 'Content-Type': 'application/json' },
    });

  } catch (err) {
    console.error('[analytics] dashboard error:', err);
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
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

export const config = {
  path: "/.netlify/functions/analytics-dashboard",
};
