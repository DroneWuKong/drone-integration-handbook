import {test} from "node:test";
import assert from "node:assert/strict";
import {DatabaseSync} from "node:sqlite";
import {readFileSync} from "node:fs";
import {handleAutonomy,verifyWebhook} from "../server/autonomy.mjs";
import {boundedRequest,reserveTrialJob,trialStatus} from "../server/research-trial.mjs";

function setup(){
 const sql=new DatabaseSync(":memory:");
 for(const name of ["0001_reports.sql","0002_attachments.sql","0003_autonomous_evidence.sql","0004_research_trial.sql"])sql.exec(readFileSync(new URL("../migrations/"+name,import.meta.url),"utf8"));
 sql.prepare("INSERT INTO research_trial VALUES(1,1,?,?)").run(Date.now()-1000,Date.now()+86400000);
 const REPORTS={prepare(query){let values={};return{bind(...args){values=Object.fromEntries(args.map((v,i)=>[i+1,v]));return this;},async first(){return sql.prepare(query).get(values)||null;},async all(){return{results:sql.prepare(query).all(values)};},async run(){return{meta:sql.prepare(query).run(values)};}};}};
 return {sql,env:{REPORTS,REVIEW_TOKEN:"review",OPENAI_API_KEY:"key",OPENAI_WEBHOOK_SECRET:"whsec_ZXhhbXBsZS1zZWNyZXQ="}};
}
const req=(path,method="GET",payload,token,headers={})=>new Request("https://uas-handbook.com/api/autonomy/"+path,{method,headers:{"content-type":"application/json",...(token?{authorization:"Bearer "+token}:{}),...headers},...(payload===undefined?{}:{body:typeof payload==="string"?payload:JSON.stringify(payload)})});
const spec={schema_version:1,id:"a".repeat(24),claim_id:"claim-1",release:"release-1",claim_type:"factual",risk:"medium",statement:"Example",anchor:"ch1",candidate_sources:["https://example.test/manual"],requirements:{},created_at:"2026-10-02T00:00:00Z"};
test('durable ledger and decision bundles require authorization and page without losing records',async()=>{
 const {env,sql}=setup();
 for(const route of ['ledger','decisions'])assert.equal((await handleAutonomy(req(route),env)).status,401);
 for(let n=1;n<=101;n++){
  const row={...spec,id:n.toString(16).padStart(24,'0'),claim_id:'claim-'+n};
  assert.equal((await handleAutonomy(req('specs','POST',row,'review'),env)).status,201);
 }
 const first=await (await handleAutonomy(req('ledger','GET',undefined,'review'),env)).json();
 assert.equal(first.rows.length,100);assert.ok(first.next_cursor);
 const second=await (await handleAutonomy(req('ledger?cursor='+first.next_cursor,'GET',undefined,'review'),env)).json();
 assert.equal(second.rows.length,1);assert.equal(second.next_cursor,null);
 assert.equal(new Set([...first.rows,...second.rows].map(r=>r.id)).size,101);
 assert.equal((await handleAutonomy(req('ledger?cursor=invalid','GET',undefined,'review'),env)).status,400);
 const row=first.rows[0];const decision={id:'d'.repeat(24),created_at:'2026-10-07T00:00:00Z',publish:false};
 sql.prepare("INSERT INTO evidence_decisions VALUES(?,?,?,'abstained',0,0,?,?)").run(decision.id,row.id,row.spec.claim_id,JSON.stringify(decision),decision.created_at);
 const bundles=await (await handleAutonomy(req('decisions','GET',undefined,'review'),env)).json();
 assert.equal(bundles.rows[0].spec.id,row.id);assert.equal(bundles.rows[0].decision.id,decision.id);
 assert.deepEqual(bundles.rows[0].packets,[]);sql.close();
});
const researchRequest=role=>({model:"gpt-5.5",input:"Check this claim against public sources.",background:true,tool_choice:"required",tools:[{type:"web_search"}],text:{format:{type:"json_schema",strict:true,schema:{}}},metadata:{research_spec_id:spec.id,claim_id:spec.claim_id,role}});
const evidencePacket=role=>({claim_id:spec.claim_id,role,conclusion:"supports",proposed_statement:"Scoped statement",scope:"Example scope",jurisdiction:"",effective_date:"2026-10-02",sources:[{url:"https://example.test/manual",title:"Manual",publisher:"Example",source_class:"manufacturer",passage:"Exact passage",locator:"Section 1",retrieved_at:"2026-10-02",content_sha256:"a".repeat(64),supports:"Exact claim",version:"1"}],contradictions:[],calculations:[],alternatives:[],confidence:.9,limitations:[],notes:""});
async function webhookHeaders(raw,secret="whsec_ZXhhbXBsZS1zZWNyZXQ="){const id="wh_"+crypto.randomUUID(),timestamp=String(Math.floor(Date.now()/1000)),key=await crypto.subtle.importKey("raw",Buffer.from("example-secret"),{name:"HMAC",hash:"SHA-256"},false,["sign"]),signed=Buffer.from(await crypto.subtle.sign("HMAC",key,new TextEncoder().encode(`${id}.${timestamp}.${raw}`))).toString("base64");return{"webhook-id":id,"webhook-timestamp":timestamp,"webhook-signature":"v1,"+signed};}

test("status is explicit with and without storage",async()=>{
 assert.equal((await (await handleAutonomy(req("status"),{})).json()).enabled,false);
 const {env,sql}=setup();const value=await (await handleAutonomy(req("status"),env)).json();assert.equal(value.enabled,true);assert.equal(value.live_research,true);sql.close();
});

test("trial fails closed when absent, disabled, future, expired, or malformed",async()=>{
 const {env,sql}=setup(),now=Date.now();
 for(const [enabled,start,end] of [[0,now-1000,now+1000],[1,now+1000,now+2000],[1,now-2000,now]]){
  sql.prepare("UPDATE research_trial SET enabled=?,starts_ms=?,ends_ms=?").run(enabled,start,end);
  assert.equal((await trialStatus(env.REPORTS,now)).active,false);
  const response=await handleAutonomy(req("runs","POST",{spec,requests:{researcher:researchRequest("researcher"),verifier:researchRequest("verifier")}},"review"),env);
  assert.equal(response.status,503);
 }
 sql.exec("DELETE FROM research_trial");assert.equal((await trialStatus(env.REPORTS)).active,false);sql.close();
});

test("trial strips cost-expanding options and pins output, tools and tier",()=>{
 const value=boundedRequest({...researchRequest("researcher"),max_output_tokens:100000,max_tool_calls:99,service_tier:"priority",previous_response_id:"old",conversation:"old"});
 assert.equal(value.max_output_tokens,4096);assert.equal(value.max_tool_calls,2);assert.equal(value.service_tier,"default");assert.equal(value.text.verbosity,"low");assert.equal(value.previous_response_id,undefined);assert.equal(value.conversation,undefined);
 assert.throws(()=>boundedRequest({...researchRequest("researcher"),model:"other"}));
 assert.throws(()=>boundedRequest({...researchRequest("researcher"),input:"x".repeat(24001)}));
 assert.throws(()=>boundedRequest({...researchRequest("researcher"),tools:[{type:"web_search"},{type:"code_interpreter"}]}));
});

test("trial atomic reservations bound daily claims and prevent ambiguous paid retries",async()=>{
 const {env,sql}=setup();let starts=0;const original=globalThis.fetch;
 globalThis.fetch=async()=>{starts++;return new Response(JSON.stringify({id:"resp_"+starts,status:"queued"}));};
 const payload=n=>{const s={...spec,id:n.toString(16).padStart(24,"0"),claim_id:"claim-"+n};return{spec:s,requests:Object.fromEntries(["researcher","verifier"].map(role=>[role,{...researchRequest(role),metadata:{research_spec_id:s.id,claim_id:s.claim_id,role}}]))};};
 try{
  const results=await Promise.all([1,2,3].map(n=>handleAutonomy(req("runs","POST",payload(n),"review"),env)));
  assert.equal(results.filter(r=>r.status===202).length,2);assert.equal(starts,4);
  assert.equal(sql.prepare("SELECT count(*) n FROM research_trial_dispatches").get().n,4);
  const row=sql.prepare("SELECT job_id,spec_id FROM research_trial_dispatches LIMIT 1").get();
  await assert.rejects(reserveTrialJob(env.REPORTS,row.job_id,row.spec_id));
  assert.equal(starts,4);
 }finally{globalThis.fetch=original;sql.close();}
});

test("daily trial limit counts claims rather than release-specific spec ids",async()=>{
 const {env,sql}=setup(),now=Date.now();
 const insert=sql.prepare("INSERT INTO research_specs(id,claim_id,release,claim_type,risk,data,state,created,updated) VALUES(?,?,'release','factual','medium','{}','planned','now','now')");
 const insertJob=sql.prepare("INSERT INTO research_jobs(id,spec_id,role,provider,state,created,updated) VALUES(?,?,'researcher','openai','planned','now','now')");
 const prior="1".repeat(24),current="2".repeat(24),other="3".repeat(24),blocked="4".repeat(24);
 insert.run(prior,"same-claim");insert.run(current,"same-claim");insert.run(other,"other-claim");insert.run(blocked,"third-claim");
 insertJob.run("prior-job",prior);insertJob.run("current-job",current);insertJob.run("other-job",other);insertJob.run("blocked-job",blocked);
 sql.prepare("INSERT INTO research_trial_dispatches VALUES(?,?,?)").run("prior-job",prior,now-1000);
 await reserveTrialJob(env.REPORTS,"current-job",current,now);
 await reserveTrialJob(env.REPORTS,"other-job",other,now);
 await assert.rejects(reserveTrialJob(env.REPORTS,"blocked-job",blocked,now));
 assert.equal(sql.prepare("SELECT count(*) n FROM research_trial_dispatches").get().n,3);sql.close();
});

test("provider timeout consumes reservation and a retry cannot bill twice",async()=>{
 const {env,sql}=setup(),original=globalThis.fetch;let starts=0;
 globalThis.fetch=async()=>{starts++;throw Error("timeout after possible acceptance");};
 try{
  const payload={spec,requests:{researcher:researchRequest("researcher"),verifier:researchRequest("verifier")}};
  for(let i=0;i<2;i++)assert.equal((await handleAutonomy(req("runs","POST",payload,"review"),env)).status,503);
  assert.equal(starts,1);
 }finally{globalThis.fetch=original;sql.close();}
});

test("trial reservations stop at 56 lifetime jobs even across dates",async()=>{
 const {env,sql}=setup(),now=Date.now();
 await handleAutonomy(req("specs","POST",spec,"review"),env);
 for(let i=1;i<=28;i++)await handleAutonomy(req("specs","POST",{...spec,id:i.toString(16).padStart(24,"0")},"review"),env);
 for(const job of sql.prepare("SELECT id,spec_id FROM research_jobs WHERE spec_id!=?").all(spec.id))sql.prepare("INSERT INTO research_trial_dispatches VALUES(?,?,?)").run(job.id,job.spec_id,now-2*86400000);
 const fresh=sql.prepare("SELECT id FROM research_jobs WHERE spec_id=? LIMIT 1").get(spec.id);
 await assert.rejects(reserveTrialJob(env.REPORTS,fresh.id,spec.id,now));sql.close();
});
test("reviewer can idempotently enqueue a two-role research spec",async()=>{
 const {env,sql}=setup();assert.equal((await handleAutonomy(req("specs","POST",spec),env)).status,401);
 assert.equal((await handleAutonomy(req("specs","POST",spec,"review"),env)).status,201);
 assert.equal((await handleAutonomy(req("specs","POST",spec,"review"),env)).status,201);
 assert.equal(sql.prepare("select count(*) n from research_specs").get().n,1);assert.equal(sql.prepare("select count(*) n from research_jobs").get().n,2);sql.close();
});
test("webhook signature validation rejects stale and altered payloads",async()=>{
 const secret="whsec_ZXhhbXBsZS1zZWNyZXQ=",id="wh_test",timestamp="1790942400",raw='{"ok":true}';
 const key=await crypto.subtle.importKey("raw",Buffer.from("example-secret"),{name:"HMAC",hash:"SHA-256"},false,["sign"]);const signed=Buffer.from(await crypto.subtle.sign("HMAC",key,new TextEncoder().encode(`${id}.${timestamp}.${raw}`))).toString("base64");
 const headers=new Headers({"webhook-id":id,"webhook-timestamp":timestamp,"webhook-signature":"v1,"+signed});
 assert.equal(await verifyWebhook(raw,headers,secret,1790942400),true);assert.equal(await verifyWebhook(raw+"x",headers,secret,1790942400),false);assert.equal(await verifyWebhook(raw,headers,secret,1790943001),false);
});
test("exceptions remain private and reviewer dispositions are idempotent",async()=>{const {env,sql}=setup();assert.equal((await handleAutonomy(req("exceptions"),env)).status,401);await handleAutonomy(req("specs","POST",spec,"review"),env);const decision={id:"b".repeat(24),claim_id:spec.claim_id,publication_state:"exception",reasons:["critical-risk-policy-requires-exception-review"]};sql.prepare("INSERT INTO evidence_decisions(id,spec_id,claim_id,publication_state,publish,human_intervention,data,created) VALUES(?1,?2,?3,'exception',0,1,?4,?5)").run(decision.id,spec.id,spec.claim_id,JSON.stringify(decision),"2026-10-02T00:00:00Z");const listed=await (await handleAutonomy(req("exceptions","GET",undefined,"review"),env)).json();assert.equal(listed.exceptions.length,1);assert.equal(listed.exceptions[0].spec.anchor,"ch1");const payload={action:"needs-field-evidence",notes:"Bench evidence cannot establish field behavior."};for(let i=0;i<2;i++)assert.equal((await handleAutonomy(req("exceptions/"+decision.id,"POST",payload,"review"),env)).status,200);assert.equal(sql.prepare("SELECT count(*) n FROM evidence_events WHERE event_type='reviewer-disposition'").get().n,1);sql.close();});
test("dispatched background jobs complete through signed webhooks and deterministic adjudication",async()=>{
 const {env,sql}=setup(),original=globalThis.fetch;let starts=0;
 globalThis.fetch=async(url,options={})=>{
  if(String(url).endsWith("/v1/responses")){starts++;return new Response(JSON.stringify({id:`resp_job_${starts}`,status:"queued"}),{status:200});}
  const role=String(url).endsWith("resp_job_1")?"researcher":"verifier";return new Response(JSON.stringify({id:String(url).split("/").at(-1),status:"completed",output:[{type:"message",content:[{type:"output_text",text:JSON.stringify(evidencePacket(role))}]}]}),{status:200});
 };
 try{
  const started=await handleAutonomy(req("runs","POST",{spec,requests:{researcher:researchRequest("researcher"),verifier:researchRequest("verifier")}},"review"),env);assert.equal(started.status,202,await started.text());
  for(const id of ["resp_job_1","resp_job_2"]){const raw=JSON.stringify({object:"event",id:"evt_"+id,type:"response.completed",created_at:Date.now()/1000,data:{id}}),headers=await webhookHeaders(raw);assert.equal((await handleAutonomy(req("webhooks/openai","POST",raw,undefined,headers),env)).status,202);}
  const decision=sql.prepare("select publication_state,publish,human_intervention from evidence_decisions").get();assert.equal(decision.publication_state,"corroborated");assert.equal(decision.publish,1);assert.equal(decision.human_intervention,0);
  assert.equal(sql.prepare("select state from research_specs").get().state,"complete");
 }finally{globalThis.fetch=original;sql.close();}
});
test("incomplete provider work is terminal and deterministically abstains",async()=>{
 const {env,sql}=setup(),original=globalThis.fetch;let starts=0;
 globalThis.fetch=async(url)=>String(url).endsWith("/v1/responses")
  ?new Response(JSON.stringify({id:`resp_incomplete_${++starts}`,status:"queued"}),{status:200})
  :new Response(JSON.stringify({id:String(url).split("/").at(-1),status:"completed",output:[{type:"message",content:[{type:"output_text",text:JSON.stringify(evidencePacket("researcher"))}]}]}),{status:200});
 try{
  assert.equal((await handleAutonomy(req("runs","POST",{spec,requests:{researcher:researchRequest("researcher"),verifier:researchRequest("verifier")}},"review"),env)).status,202);
  const completed=JSON.stringify({object:"event",id:"evt_completed",type:"response.completed",created_at:Date.now()/1000,data:{id:"resp_incomplete_1"}});
  assert.equal((await handleAutonomy(req("webhooks/openai","POST",completed,undefined,await webhookHeaders(completed)),env)).status,202);
  const incomplete=JSON.stringify({object:"event",id:"evt_incomplete",type:"response.incomplete",created_at:Date.now()/1000,data:{id:"resp_incomplete_2"}});
  assert.equal((await handleAutonomy(req("webhooks/openai","POST",incomplete,undefined,await webhookHeaders(incomplete)),env)).status,202);
  assert.equal(sql.prepare("SELECT state FROM research_jobs WHERE role='verifier'").get().state,"failed");
  assert.equal(sql.prepare("SELECT state FROM webhook_events WHERE id='evt_incomplete'").get().state,"processed");
  const decision=sql.prepare("SELECT publication_state,publish,human_intervention FROM evidence_decisions").get();
  assert.equal(decision.publication_state,"abstained");assert.equal(decision.publish,0);assert.equal(decision.human_intervention,0);
  assert.equal(sql.prepare("SELECT state FROM research_specs").get().state,"abstained");
 }finally{globalThis.fetch=original;sql.close();}
});
test("completed output rejected by trusted validation is terminal and abstains",async()=>{
 const {env,sql}=setup(),original=globalThis.fetch;let starts=0;
 globalThis.fetch=async(url)=>{
  const value=String(url);
  if(value.endsWith("/v1/responses"))return new Response(JSON.stringify({id:`resp_rejected_${++starts}`,status:"queued"}),{status:200});
  if(value.includes("/v1/responses/")){const role=value.endsWith("_1")?"researcher":"verifier",packet=evidencePacket(role);if(role==="researcher")packet.sources[0].url="https://example.test/oversized.pdf";return new Response(JSON.stringify({id:value.split("/").at(-1),status:"completed",output:[{type:"message",content:[{type:"output_text",text:JSON.stringify(packet)}]}]}),{status:200});}
  if(value.endsWith("/oversized.pdf"))return new Response("too large",{status:200,headers:{"content-length":"5000000"}});
  return new Response("trusted source bytes",{status:200});
 };
 try{
  assert.equal((await handleAutonomy(req("runs","POST",{spec,requests:{researcher:researchRequest("researcher"),verifier:researchRequest("verifier")}},"review"),env)).status,202);
  for(const [suffix,eventId] of [["1","evt_rejected"],["2","evt_verified"]]){const raw=JSON.stringify({object:"event",id:eventId,type:"response.completed",created_at:Date.now()/1000,data:{id:`resp_rejected_${suffix}`}});assert.equal((await handleAutonomy(req("webhooks/openai","POST",raw,undefined,await webhookHeaders(raw)),env)).status,202);}
  assert.equal(sql.prepare("SELECT state FROM research_jobs WHERE role='researcher'").get().state,"failed");
  assert.equal(sql.prepare("SELECT state FROM webhook_events WHERE id='evt_rejected'").get().state,"failed");
  assert.equal(sql.prepare("SELECT state FROM research_jobs WHERE role='verifier'").get().state,"completed");
  const decision=sql.prepare("SELECT publication_state,publish FROM evidence_decisions").get();assert.equal(decision.publication_state,"abstained");assert.equal(decision.publish,0);
  assert.equal(sql.prepare("SELECT state FROM research_specs").get().state,"abstained");
 }finally{globalThis.fetch=original;sql.close();}
});
test('exact-statement protocol checks retrieved passages and canonical scope before allowing publication',async()=>{
 const originalFetch=globalThis.fetch;
 for(const failure of [null,'scope','passage']){
  const {env,sql}=setup();let starts=0;
  const exact={...spec,statement:'Scoped statement',scope:'Example scope',verification_protocol:'exact-statement-v2'};
  globalThis.fetch=async(url)=>{
   const value=String(url);
   if(value.endsWith('/v1/responses'))return new Response(JSON.stringify({id:`resp_exact_${++starts}`,status:'queued'}));
   if(value.includes('/v1/responses/')){
    const role=value.endsWith('_1')?'researcher':'verifier',packet=evidencePacket(role);
    if(role==='verifier'&&failure==='scope')packet.scope='A different version';
    if(role==='verifier'&&failure==='passage')packet.sources[0].passage='An invented supporting passage';
    return new Response(JSON.stringify({status:'completed',output:[{type:'message',content:[{type:'output_text',text:JSON.stringify(packet)}]}]}));
   }
   return new Response('<p>Exact passage</p>');
  };
  try{
   assert.equal((await handleAutonomy(req('runs','POST',{spec:exact,requests:{researcher:researchRequest('researcher'),verifier:researchRequest('verifier')}},'review'),env)).status,202);
   for(const n of [1,2]){
    const raw=JSON.stringify({id:`evt_${failure||'valid'}_${n}`,type:'response.completed',data:{id:`resp_exact_${n}`}});
    assert.equal((await handleAutonomy(req('webhooks/openai','POST',raw,undefined,await webhookHeaders(raw)),env)).status,202);
   }
   const decision=sql.prepare('SELECT publish,publication_state FROM evidence_decisions').get();
   assert.equal(decision.publish,failure?0:1);assert.equal(decision.publication_state,failure?'abstained':'corroborated');
  }finally{sql.close();globalThis.fetch=originalFetch;}
 }
});
