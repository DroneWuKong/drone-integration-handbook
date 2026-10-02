/* Autonomous evidence API. Models collect evidence; deterministic code adjudicates it. */
const jsonHeaders={"content-type":"application/json","cache-control":"no-store","x-content-type-options":"nosniff"};
const respond=(status,data)=>new Response(JSON.stringify(data),{status,headers:jsonHeaders});
const enc=new TextEncoder();
const hex=bytes=>Array.from(bytes).map(x=>x.toString(16).padStart(2,"0")).join("");
const sha=async value=>hex(new Uint8Array(await crypto.subtle.digest("SHA-256",enc.encode(value))));
const policies={administrative:{min:0,auto:true},factual:{min:1,auto:true},configuration:{min:1,auto:true},commercial:{min:1,auto:true},calculation:{min:1,auto:true,reproduce:true},performance:{min:2,auto:true},compatibility:{min:2,auto:true},regulatory:{min:1,auto:true,authority:true},safety:{min:2,auto:false},recommendation:{min:2,auto:false,alternatives:true}};
const conclusions=new Set(["supports","partially-supports","contradicts","insufficient"]),sourceClasses=new Set(["controlling-authority","government-guidance","standard","manufacturer","peer-reviewed","independent-technical","field-observation","other"]);
const safeEqual=(a,b)=>{if(a.length!==b.length)return false;let value=0;for(let i=0;i<a.length;i++)value|=a.charCodeAt(i)^b.charCodeAt(i);return value===0;};
async function reviewer(request,secret){const value=request.headers.get("authorization")||"";if(!secret||!value.startsWith("Bearer "))return false;return safeEqual(await sha(value.slice(7)),await sha(secret));}
async function body(request,limit=262144){const text=await request.text();if(new TextEncoder().encode(text).length>limit)throw Error("Body too large");return {text,data:JSON.parse(text)};}
function decodeSecret(secret){const value=secret.startsWith("whsec_")?secret.slice(6):secret;const normalized=value.replace(/-/g,"+").replace(/_/g,"/");try{return Uint8Array.from(atob(normalized),c=>c.charCodeAt(0));}catch{return enc.encode(secret);}}
async function hmac(secret,message){const key=await crypto.subtle.importKey("raw",decodeSecret(secret),{name:"HMAC",hash:"SHA-256"},false,["sign"]);const signed=new Uint8Array(await crypto.subtle.sign("HMAC",key,enc.encode(message)));let raw="";for(const byte of signed)raw+=String.fromCharCode(byte);return btoa(raw);}
async function recordEvent(env,entityType,entityId,eventType,data){const serialized=JSON.stringify(data),id=(await sha(`${entityType}\x1f${entityId}\x1f${eventType}\x1f${serialized}`)).slice(0,24),now=new Date().toISOString();await env.REPORTS.prepare("INSERT OR IGNORE INTO evidence_events(id,entity_type,entity_id,event_type,data,created) VALUES(?1,?2,?3,?4,?5,?6)").bind(id,entityType,entityId,eventType,serialized,now).run();return id;}
export async function verifyWebhook(raw,headers,secret,nowSeconds=Math.floor(Date.now()/1000)){
 const id=headers.get("webhook-id")||"",timestamp=headers.get("webhook-timestamp")||"",signature=headers.get("webhook-signature")||"";
 if(!secret||!id||!/^\d+$/.test(timestamp)||Math.abs(nowSeconds-Number(timestamp))>300)return false;
 const expected=await hmac(secret,`${id}.${timestamp}.${raw}`);
 return signature.split(" ").some(item=>{const [version,value]=item.split(",",2);return version==="v1"&&value&&safeEqual(value,expected);});
}
function cleanSpec(input){
 if(input?.schema_version!==1||typeof input.id!=="string"||!/^[0-9a-f]{24}$/.test(input.id)||typeof input.claim_id!=="string"||typeof input.release!=="string"||!policies[input.claim_type]||typeof input.risk!=="string")throw Error("Invalid research spec");
 if(!Array.isArray(input.candidate_sources)||input.candidate_sources.length>20)throw Error("Invalid research source candidates");
 if(JSON.stringify(input).length>60000)throw Error("Research spec too large");return input;
}
function cleanResearchRequest(input,spec,role){
 if(!input||input.background!==true||input.tool_choice!=="required"||input.metadata?.research_spec_id!==spec.id||input.metadata?.claim_id!==spec.claim_id||input.metadata?.role!==role)throw Error("Invalid background research request");
 if(!Array.isArray(input.tools)||!input.tools.some(tool=>tool.type==="web_search")||input.text?.format?.type!=="json_schema"||input.text?.format?.strict!==true)throw Error("Research request must use web search and strict structured output");
 if(JSON.stringify(input).length>90000)throw Error("Research request too large");return input;
}
async function startResearchRun(env,spec,requests){
 const now=new Date().toISOString(),result=[];
 await env.REPORTS.prepare("INSERT INTO research_specs(id,claim_id,release,claim_type,risk,data,state,created,updated) VALUES(?1,?2,?3,?4,?5,?6,'planned',?7,?7) ON CONFLICT(id) DO NOTHING").bind(spec.id,spec.claim_id,spec.release,spec.claim_type,spec.risk,JSON.stringify(spec),now).run();
 for(const role of ["researcher","verifier"]){
  const id=(await sha(`${spec.id}\x1f${role}`)).slice(0,24),existing=await env.REPORTS.prepare("SELECT response_id,state FROM research_jobs WHERE id=?1").bind(id).first();
  if(existing?.response_id){result.push({id,role,...existing,replayed:true});continue;}
  const request=cleanResearchRequest(requests?.[role],spec,role);
  await env.REPORTS.prepare("INSERT OR IGNORE INTO research_jobs(id,spec_id,role,provider,state,created,updated) VALUES(?1,?2,?3,'openai','planned',?4,?4)").bind(id,spec.id,role,now).run();
  const remote=await fetch("https://api.openai.com/v1/responses",{method:"POST",headers:{authorization:`Bearer ${env.OPENAI_API_KEY}`,"content-type":"application/json"},body:JSON.stringify(request)});
  if(!remote.ok){const detail=(await remote.text()).slice(0,1000);await env.REPORTS.prepare("UPDATE research_jobs SET state='failed',attempts=attempts+1,last_error=?1,updated=?2 WHERE id=?3").bind(`HTTP ${remote.status}: ${detail}`,now,id).run();throw Error("Research provider rejected a background request");}
  const response=await remote.json();if(!response.id||!["queued","in_progress","completed"].includes(response.status))throw Error("Research provider did not acknowledge background work");
  await env.REPORTS.prepare("UPDATE research_jobs SET response_id=?1,state=?2,attempts=attempts+1,last_error=NULL,updated=?3 WHERE id=?4").bind(response.id,response.status,now,id).run();await recordEvent(env,"job",id,"provider-acknowledged",{response_id:response.id,state:response.status,role});result.push({id,role,response_id:response.id,state:response.status});
 }
 await env.REPORTS.prepare("UPDATE research_specs SET state='researching',updated=?1 WHERE id=?2").bind(now,spec.id).run();return result;
}
function packetFromResponse(response){const text=(response.output||[]).filter(x=>x.type==="message").flatMap(x=>x.content||[]).filter(x=>x.type==="output_text").map(x=>x.text||"").join("");if(!text)throw Error("Completed response has no evidence packet");const packet=JSON.parse(text);if(!packet||typeof packet!=="object"||!packet.claim_id||!["researcher","verifier"].includes(packet.role)||!Array.isArray(packet.sources))throw Error("Invalid evidence packet");return packet;}
function validatePacket(packet,claimId,role){
 const strings=["proposed_statement","scope","jurisdiction","effective_date","notes"],arrays=["sources","contradictions","calculations","alternatives","limitations"];
 if(packet.claim_id!==claimId||packet.role!==role||!conclusions.has(packet.conclusion)||!Number.isFinite(packet.confidence)||packet.confidence<0||packet.confidence>1)throw Error("Invalid evidence packet identity or conclusion");
 if(strings.some(key=>typeof packet[key]!=="string")||arrays.some(key=>!Array.isArray(packet[key])))throw Error("Invalid evidence packet shape");
 if(packet.sources.length>10||packet.contradictions.length>20||packet.calculations.length>20||packet.alternatives.length>20||packet.limitations.length>20)throw Error("Evidence packet exceeds bounded collection limits");
 for(const source of packet.sources){if(!source||typeof source!=="object"||!sourceClasses.has(source.source_class)||!["title","publisher","passage","locator","supports","version"].every(key=>typeof source[key]==="string")||!/^\d{4}-\d{2}-\d{2}$/.test(source.retrieved_at||""))throw Error("Invalid evidence source");}
 for(const calculation of packet.calculations){if(!calculation||typeof calculation!=="object"||!["method","inputs","units","result","code"].every(key=>typeof calculation[key]==="string")||typeof calculation.reproduced!=="boolean")throw Error("Invalid evidence calculation");}
 return packet;
}
const defaultDomains=["faa.gov","ecfr.gov","govinfo.gov","federalregister.gov","fcc.gov","nist.gov","cisa.gov","ntia.gov","itu.int"];
function allowedHost(host,domains){host=String(host||"").toLowerCase().replace(/\.$/,"");if(!host||host==="localhost"||host.endsWith(".localhost")||host.endsWith(".local")||host.endsWith(".internal")||/^\d+(?:\.\d+){3}$/.test(host)||host.includes(":"))return false;return domains.some(domain=>host===domain||host.endsWith("."+domain));}
async function verifyPacketSources(packet,spec,env){
 if(packet.sources.length>10)throw Error("Evidence packet contains too many sources");const domains=[...new Set([...defaultDomains,...(spec.candidate_sources||[]).map(value=>{try{return new URL(value).hostname.toLowerCase();}catch{return "";}}).filter(Boolean)])];
 for(const source of packet.sources){let url;try{url=new URL(source.url);}catch{throw Error("Invalid evidence source URL");}if(url.protocol!=="https:"||!allowedHost(url.hostname,domains))throw Error("Evidence source outside allowlist");
  let remote;for(let redirects=0;redirects<=5;redirects++){remote=await fetch(url,{headers:{"user-agent":"UAS-Handbook-Evidence/1.0"},redirect:"manual"});if(![301,302,303,307,308].includes(remote.status))break;const location=remote.headers.get("location");if(!location)throw Error("Evidence source redirect is missing a target");url=new URL(location,url);if(url.protocol!=="https:"||!allowedHost(url.hostname,domains))throw Error("Evidence source redirect left allowlist");if(redirects===5)throw Error("Evidence source redirect limit exceeded");}
  if(!remote.ok)throw Error("Evidence source snapshot failed");const declared=Number(remote.headers.get("content-length")||0);if(declared>4194304)throw Error("Evidence source snapshot too large");const bytes=new Uint8Array(await remote.arrayBuffer());if(!bytes.length||bytes.length>4194304)throw Error("Evidence source snapshot invalid");const digest=hex(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes)));source.content_sha256=digest;if(env.EVIDENCE)await env.EVIDENCE.put(`source-snapshots/${digest}`,bytes,{customMetadata:{source_url:source.url,retrieved_at:new Date().toISOString()}});
 }
 return packet;
}
async function adjudicateStored(env,specRow){
 const spec=JSON.parse(specRow.data),rows=await env.REPORTS.prepare("SELECT p.role,p.data FROM evidence_packets p JOIN research_jobs j ON j.id=p.job_id WHERE j.spec_id=?1 ORDER BY p.role").bind(spec.id).all(),packets=rows.results.filter(row=>["researcher","verifier"].includes(row.role)).map(row=>JSON.parse(row.data));
 const byRole=Object.fromEntries(packets.map(packet=>[packet.role,packet])),base={schema_version:1,research_spec_id:spec.id,claim_id:spec.claim_id,claim_type:spec.claim_type,created_at:new Date().toISOString(),publication_state:"abstained",publish:false,human_intervention:false,reasons:[],source_count:0};
 let decision;
 if(!byRole.researcher||!byRole.verifier)decision={...base,reasons:["independent-research-and-verification-required"]};
 else{
  const conclusions=new Set(packets.map(packet=>packet.conclusion)),contradictions=packets.flatMap(packet=>packet.contradictions||[]).filter(Boolean);
  if(conclusions.has("contradicts")||(conclusions.has("supports")&&conclusions.has("insufficient")))decision={...base,publication_state:"contradicted",human_intervention:true,reasons:["independent-runs-disagree"]};
  else if(conclusions.size!==1||!conclusions.has("supports"))decision={...base,reasons:["evidence-does-not-fully-support-exact-claim"]};
  else{
   const sources=[...new Map(packets.flatMap(packet=>packet.sources||[]).map(source=>[`${source.url}|${source.content_sha256}`,source])).values()],policy=policies[spec.claim_type]||policies.factual;const next={...base,source_count:sources.length};
   if(sources.length<policy.min)decision={...next,reasons:["minimum-independent-source-count-not-met"]};
   else if(Math.min(...packets.map(packet=>Number(packet.confidence)||0))<.75)decision={...next,reasons:["confidence-below-publication-threshold"]};
   else if(policy.authority&&(!sources.some(source=>["controlling-authority","government-guidance"].includes(source.source_class))||packets.some(packet=>!packet.jurisdiction||!packet.effective_date)))decision={...next,human_intervention:true,reasons:["regulatory-authority-jurisdiction-or-effective-date-missing"]};
   else if(policy.reproduce&&(!packets.flatMap(packet=>packet.calculations||[]).length||!packets.flatMap(packet=>packet.calculations||[]).every(calculation=>calculation.reproduced)))decision={...next,reasons:["deterministic-reproduction-required"]};
   else if(policy.alternatives&&packets.some(packet=>!(packet.alternatives||[]).length))decision={...next,reasons:["recommendation-alternatives-required"]};
   else if(contradictions.length)decision={...next,publication_state:"exception",human_intervention:true,reasons:["unresolved-counterevidence"]};
   else if(!policy.auto)decision={...next,publication_state:"exception",human_intervention:true,reasons:["critical-risk-policy-requires-exception-review"]};
   else decision={...next,publication_state:policy.reproduce?"independently-reproduced":spec.claim_type==="regulatory"?"primary-source-supported":"corroborated",publish:true,reasons:["deterministic-publication-policy-passed"],statement:byRole.verifier.proposed_statement,scope:byRole.verifier.scope,source_urls:[...new Set(sources.map(source=>source.url))].sort()};
  }
 }
 decision.id=(await sha(`${spec.id}\x1f${JSON.stringify(packets)}`)).slice(0,24);const data=JSON.stringify(decision);
 await env.REPORTS.prepare("INSERT OR IGNORE INTO evidence_decisions(id,spec_id,claim_id,publication_state,publish,human_intervention,data,created) VALUES(?1,?2,?3,?4,?5,?6,?7,?8)").bind(decision.id,spec.id,spec.claim_id,decision.publication_state,decision.publish?1:0,decision.human_intervention?1:0,data,decision.created_at).run();
 await recordEvent(env,"decision",decision.id,"adjudicated",{publication_state:decision.publication_state,publish:decision.publish,human_intervention:decision.human_intervention,reasons:decision.reasons});
 const state=decision.human_intervention?"exception":decision.publish?"complete":"abstained";await env.REPORTS.prepare("UPDATE research_specs SET state=?1,updated=?2 WHERE id=?3").bind(state,new Date().toISOString(),spec.id).run();return decision;
}
async function processResponse(env,event){
 const now=new Date().toISOString(),responseId=event.data.id;
 const job=await env.REPORTS.prepare("SELECT id,spec_id,role FROM research_jobs WHERE response_id=?1").bind(responseId).first();
 if(!job){await env.REPORTS.prepare("UPDATE webhook_events SET state='ignored',updated=?1 WHERE id=?2").bind(now,event.id).run();return;}
 const remote=await fetch(`https://api.openai.com/v1/responses/${responseId}`,{headers:{authorization:`Bearer ${env.OPENAI_API_KEY}`}});
 if(!remote.ok)throw Error(`Response retrieval failed: ${remote.status}`);
 const declared=Number(remote.headers.get("content-length")||0);if(declared>2097152)throw Error("Completed response is too large");const responseBytes=new Uint8Array(await remote.arrayBuffer());if(responseBytes.length>2097152)throw Error("Completed response is too large");const response=JSON.parse(new TextDecoder().decode(responseBytes));let packet=packetFromResponse(response);
 const spec=await env.REPORTS.prepare("SELECT claim_id,data FROM research_specs WHERE id=?1").bind(job.spec_id).first();if(!spec)throw Error("Research spec is missing");packet=validatePacket(packet,spec.claim_id,job.role);packet=await verifyPacketSources(packet,JSON.parse(spec.data),env);
 const data=JSON.stringify(packet),digest=await sha(data),packetId=await sha(`${job.id}|${digest}`);
 await env.REPORTS.prepare("INSERT OR IGNORE INTO evidence_packets(id,job_id,claim_id,role,data,digest,created) VALUES(?1,?2,?3,?4,?5,?6,?7)").bind(packetId.slice(0,24),job.id,packet.claim_id,packet.role,data,digest,now).run();
 await recordEvent(env,"job",job.id,"packet-stored",{packet_id:packetId.slice(0,24),digest,role:packet.role});
 await env.REPORTS.prepare("UPDATE research_jobs SET state='completed',updated=?1 WHERE id=?2").bind(now,job.id).run();
 const pending=await env.REPORTS.prepare("SELECT count(*) count FROM research_jobs WHERE spec_id=?1 AND state!='completed'").bind(job.spec_id).first();
 await env.REPORTS.prepare("UPDATE research_specs SET state=?1,updated=?2 WHERE id=?3").bind(pending.count===0?"adjudicating":"researching",now,job.spec_id).run();if(pending.count===0)await adjudicateStored(env,spec);
 await env.REPORTS.prepare("UPDATE webhook_events SET state='processed',updated=?1 WHERE id=?2").bind(now,event.id).run();
}
export async function handleAutonomy(request,env,context){
 const url=new URL(request.url),path=url.pathname.replace(/^\/api\/autonomy\/?/,""),db=env.REPORTS;
 if(path==="status"&&request.method==="GET"){
  if(!db)return respond(200,{enabled:false,schema_version:1});
  const specs=await db.prepare("SELECT state,count(*) count FROM research_specs GROUP BY state").all();const decisions=await db.prepare("SELECT publication_state,count(*) count FROM evidence_decisions GROUP BY publication_state").all();
  return respond(200,{enabled:true,live_research:!!(env.OPENAI_API_KEY&&env.OPENAI_WEBHOOK_SECRET),specs:specs.results,decisions:decisions.results,schema_version:1});
 }
 if(!db)return respond(503,{error:"Autonomous evidence storage is not configured"});
 try{
  if(path==="specs"&&request.method==="POST"){
   if(!await reviewer(request,env.REVIEW_TOKEN))return respond(401,{error:"Reviewer authorization required"});
   const input=cleanSpec((await body(request,65536)).data),now=new Date().toISOString(),data=JSON.stringify(input);
   await db.prepare("INSERT INTO research_specs(id,claim_id,release,claim_type,risk,data,state,created,updated) VALUES(?1,?2,?3,?4,?5,?6,'planned',?7,?7) ON CONFLICT(id) DO NOTHING").bind(input.id,input.claim_id,input.release,input.claim_type,input.risk,data,now).run();
   await recordEvent(env,"spec",input.id,"planned",{claim_id:input.claim_id,release:input.release,claim_type:input.claim_type,risk:input.risk});
   for(const role of ["researcher","verifier"]){const id=(await sha(`${input.id}\x1f${role}`)).slice(0,24);await db.prepare("INSERT OR IGNORE INTO research_jobs(id,spec_id,role,provider,state,created,updated) VALUES(?1,?2,?3,'openai','planned',?4,?4)").bind(id,input.id,role,now).run();}
   return respond(201,{id:input.id,state:"planned"});
  }
  if(path==="runs"&&request.method==="POST"){
   if(!await reviewer(request,env.REVIEW_TOKEN))return respond(401,{error:"Reviewer authorization required"});
   if(!env.OPENAI_API_KEY)return respond(503,{error:"Live research provider is not configured"});
   const input=(await body(request,220000)).data,spec=cleanSpec(input.spec),jobs=await startResearchRun(env,spec,input.requests);
   return respond(202,{id:spec.id,state:"researching",jobs});
  }
  if(path==="webhooks/openai"&&request.method==="POST"){
   const raw=await request.text();if(enc.encode(raw).length>262144)return respond(413,{error:"Webhook body too large"});if(!await verifyWebhook(raw,request.headers,env.OPENAI_WEBHOOK_SECRET))return respond(400,{error:"Invalid webhook signature"});
   const event=JSON.parse(raw),now=new Date().toISOString();if(!event.id||!event.type||!event.data?.id)throw Error("Invalid webhook event");
   const saved=await db.prepare("INSERT OR IGNORE INTO webhook_events(id,event_type,response_id,state,created,updated) VALUES(?1,?2,?3,'received',?4,?4)").bind(event.id,event.type,event.data.id,now).run();
   if(saved.meta.changes===0)return respond(200,{received:true,replayed:true});
   if(event.type!=="response.completed"){await db.prepare("UPDATE webhook_events SET state='ignored',updated=?1 WHERE id=?2").bind(now,event.id).run();return respond(202,{received:true,ignored:true});}
   const work=processResponse(env,event).catch(async error=>{await db.prepare("UPDATE webhook_events SET state='failed',updated=?1 WHERE id=?2").bind(new Date().toISOString(),event.id).run();});
   if(context?.waitUntil)context.waitUntil(work);else await work;
   return respond(202,{received:true});
  }
  if(path==="exceptions"&&request.method==="GET"){
   if(!await reviewer(request,env.REVIEW_TOKEN))return respond(401,{error:"Reviewer authorization required"});
   const result=await db.prepare("SELECT d.id,d.claim_id,d.publication_state,d.data,d.created,s.data spec_data,(SELECT e.data FROM evidence_events e WHERE e.entity_type='decision' AND e.entity_id=d.id AND e.event_type='reviewer-disposition' ORDER BY e.created DESC LIMIT 1) disposition FROM evidence_decisions d JOIN research_specs s ON s.id=d.spec_id WHERE d.human_intervention=1 ORDER BY d.created DESC LIMIT 100").all();
   return respond(200,{exceptions:result.results.map(row=>({id:row.id,claim_id:row.claim_id,publication_state:row.publication_state,created:row.created,data:JSON.parse(row.data),spec:JSON.parse(row.spec_data),disposition:row.disposition?JSON.parse(row.disposition):null}))});
  }
  const exceptionMatch=path.match(/^exceptions\/([0-9a-f]{24})$/);
  if(exceptionMatch&&request.method==="POST"){
   if(!await reviewer(request,env.REVIEW_TOKEN))return respond(401,{error:"Reviewer authorization required"});
   const input=(await body(request,32768)).data,allowed=new Set(["accept-proposal","reject-proposal","needs-field-evidence","defer"]),notes=String(input?.notes||"").trim();
   if(!allowed.has(input?.action)||!notes||notes.length>5000)return respond(400,{error:"A valid disposition and concise reviewer note are required"});
   const decision=await db.prepare("SELECT id FROM evidence_decisions WHERE id=?1 AND human_intervention=1").bind(exceptionMatch[1]).first();if(!decision)return respond(404,{error:"Evidence exception not found"});
   const data={action:input.action,notes};const event_id=await recordEvent(env,"decision",decision.id,"reviewer-disposition",data);return respond(200,{id:decision.id,event_id,disposition:data});
  }
  return respond(404,{error:"Autonomy route unavailable"});
 }catch(error){const message=error?.message||"";if(/Invalid|too large|JSON/i.test(message))return respond(400,{error:message});return respond(503,{error:"Autonomous evidence operation failed closed"});}
}
