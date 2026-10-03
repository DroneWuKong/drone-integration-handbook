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
 assert.equal(value.max_output_tokens,4096);assert.equal(value.max_tool_calls,2);assert.equal(value.service_tier,"default");assert.equal(value.previous_response_id,undefined);assert.equal(value.conversation,undefined);
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
