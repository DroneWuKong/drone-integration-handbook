import {test} from "node:test";
import assert from "node:assert/strict";
import {DatabaseSync} from "node:sqlite";
import {readFileSync} from "node:fs";
import {handleAutonomy,verifyWebhook} from "../server/autonomy.mjs";

function setup(){
 const sql=new DatabaseSync(":memory:");
 for(const name of ["0001_reports.sql","0002_attachments.sql","0003_autonomous_evidence.sql"])sql.exec(readFileSync(new URL("../migrations/"+name,import.meta.url),"utf8"));
 const REPORTS={prepare(query){let values={};return{bind(...args){values=Object.fromEntries(args.map((v,i)=>[i+1,v]));return this;},async first(){return sql.prepare(query).get(values)||null;},async all(){return{results:sql.prepare(query).all(values)};},async run(){return{meta:sql.prepare(query).run(values)};}};}};
 return {sql,env:{REPORTS,REVIEW_TOKEN:"review",OPENAI_API_KEY:"key",OPENAI_WEBHOOK_SECRET:"whsec_ZXhhbXBsZS1zZWNyZXQ="}};
}
const req=(path,method="GET",payload,token,headers={})=>new Request("https://uas-handbook.com/api/autonomy/"+path,{method,headers:{"content-type":"application/json",...(token?{authorization:"Bearer "+token}:{}),...headers},...(payload===undefined?{}:{body:typeof payload==="string"?payload:JSON.stringify(payload)})});
const spec={schema_version:1,id:"a".repeat(24),claim_id:"claim-1",release:"release-1",claim_type:"factual",risk:"medium",statement:"Example",anchor:"ch1",candidate_sources:["https://example.test/manual"],requirements:{},created_at:"2026-10-02T00:00:00Z"};
const researchRequest=role=>({model:"gpt-5.5",background:true,tool_choice:"required",tools:[{type:"web_search"}],text:{format:{type:"json_schema",strict:true,schema:{}}},metadata:{research_spec_id:spec.id,claim_id:spec.claim_id,role}});
const evidencePacket=role=>({claim_id:spec.claim_id,role,conclusion:"supports",proposed_statement:"Scoped statement",scope:"Example scope",jurisdiction:"",effective_date:"2026-10-02",sources:[{url:"https://example.test/manual",title:"Manual",publisher:"Example",source_class:"manufacturer",passage:"Exact passage",locator:"Section 1",retrieved_at:"2026-10-02",content_sha256:"a".repeat(64),supports:"Exact claim",version:"1"}],contradictions:[],calculations:[],alternatives:[],confidence:.9,limitations:[],notes:""});
async function webhookHeaders(raw,secret="whsec_ZXhhbXBsZS1zZWNyZXQ="){const id="wh_"+crypto.randomUUID(),timestamp=String(Math.floor(Date.now()/1000)),key=await crypto.subtle.importKey("raw",Buffer.from("example-secret"),{name:"HMAC",hash:"SHA-256"},false,["sign"]),signed=Buffer.from(await crypto.subtle.sign("HMAC",key,new TextEncoder().encode(`${id}.${timestamp}.${raw}`))).toString("base64");return{"webhook-id":id,"webhook-timestamp":timestamp,"webhook-signature":"v1,"+signed};}

test("status is explicit with and without storage",async()=>{
 assert.equal((await (await handleAutonomy(req("status"),{})).json()).enabled,false);
 const {env,sql}=setup();const value=await (await handleAutonomy(req("status"),env)).json();assert.equal(value.enabled,true);assert.equal(value.live_research,true);sql.close();
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
