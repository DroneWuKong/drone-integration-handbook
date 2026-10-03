// This is an additional workload guard, not a substitute for a provider hard
// spend limit. No trial is activated by installing this module or migration.
export async function trialStatus(db, now = Date.now()) {
  const row = await db.prepare("SELECT * FROM research_trial WHERE id=1").first();
  return { ...row, active: !!row && row.enabled === 1 &&
    Number.isSafeInteger(row.starts_ms) && Number.isSafeInteger(row.ends_ms) &&
    row.ends_ms > row.starts_ms && row.ends_ms - row.starts_ms <= 14 * 86400000 &&
    now >= row.starts_ms && now < row.ends_ms };
}

export function boundedRequest(request) {
  // Construct an allowlist rather than forwarding arbitrary billed tools,
  // conversation history, attachments, stored prompts, or premium tiers.
  if (request.model !== "gpt-5.5" || typeof request.input !== "string" ||
      new TextEncoder().encode(request.input).length > 24000 ||
      request.tools?.length !== 1 || request.tools[0].type !== "web_search") {
    throw Error("Invalid trial research request");
  }
  return {
    model: "gpt-5.5", background: true, store: true, service_tier: "default",
    reasoning: { effort: "high" }, max_output_tokens: 4096, max_tool_calls: 2,
    tools: [{ type: "web_search", search_context_size: "low",
      external_web_access: true, ...(request.tools[0].filters ? { filters: request.tools[0].filters } : {}) }],
    tool_choice: "required", include: ["web_search_call.action.sources"],
    input: request.input, text: request.text, metadata: request.metadata,
  };
}

export async function reserveTrialJob(db, jobId, specId, now = Date.now()) {
  // One atomic statement enforces expiry, two distinct claims per rolling day,
  // 56 lifetime jobs, and at-most-once dispatch even after an ambiguous timeout.
  // Reservations are never deleted or refunded automatically.
  const result = await db.prepare(`INSERT OR IGNORE INTO research_trial_dispatches
    (job_id,spec_id,started_ms)
    SELECT ?1,?2,?3 FROM research_trial WHERE id=1 AND enabled=1
      AND starts_ms<=?3 AND ends_ms>?3 AND ends_ms>starts_ms
      AND ends_ms-starts_ms<=1209600000
      AND (SELECT count(*) FROM research_trial_dispatches)<56
      AND ((SELECT count(DISTINCT spec_id) FROM research_trial_dispatches
              WHERE started_ms>?3-86400000)<2
           OR EXISTS(SELECT 1 FROM research_trial_dispatches
              WHERE spec_id=?2 AND started_ms>?3-86400000))
      AND (SELECT count(*) FROM research_trial_dispatches WHERE spec_id=?2)<2`
  ).bind(jobId, specId, now).run();
  if (result.meta.changes !== 1) throw Error("Trial stopped: expired, disabled, workload limit, or dispatch already reserved");
}
