/* Private report API. Public builds never read this database. */
const STATES={new:["triaged","duplicate","rejected"],triaged:["needs-evidence","accepted","duplicate","rejected"],"needs-evidence":["triaged","accepted","duplicate","rejected"],accepted:["correction-prepared","needs-evidence"],"correction-prepared":["published","needs-evidence"],published:[],duplicate:[],rejected:[]};
export {STATES};
const headers={"content-type":"application/json","cache-control":"no-store","x-content-type-options":"nosniff"};
const respond=(status,data)=>new Response(JSON.stringify(data),{status,headers});
const digest=async value=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value)))).map(x=>x.toString(16).padStart(2,"0")).join("");
async function auth(request,secret){const bearer=request.headers.get("authorization")||"";if(!secret||!bearer.startsWith("Bearer "))return false;const a=await digest(bearer.slice(7)),b=await digest(secret);let x=0;for(let i=0;i<a.length;i++)x|=a.charCodeAt(i)^b.charCodeAt(i);return x===0;}
async function body(request){if(!request.headers.get("content-type")?.startsWith("application/json"))throw Error("JSON required");if(Number(request.headers.get("content-length"))>24576)throw Error("Report too large");const reader=request.body?.getReader();if(!reader)throw Error("Body required");let size=0;const parts=[];while(true){const r=await reader.read();if(r.done)break;size+=r.value.length;if(size>24576){await reader.cancel();throw Error("Report too large");}parts.push(r.value);}const bytes=new Uint8Array(size);let offset=0;for(const p of parts){bytes.set(p,offset);offset+=p.length;}return JSON.parse(new TextDecoder().decode(bytes));}
function field(input,key,max,required=false){const v=input[key];if(v!=null&&typeof v!=="string")throw Error(key+" must be text");const t=(v||"").trim();if(t.length>max||required&&!t)throw Error(key+" is missing or too long");return t;}
function clean(input){if(input.consent!==true)throw Error("Consent is required");const out={};for(const[k,max,required]of [["kind",40,true],["claim_id",160,true],["release",80,true],["description",4000,true],["proposed",2000,false],["source_url",2000,false],["configuration",1500,false],["observed_date",10,false],["conditions",2000,false],["measurement",2000,false],["contact",320,false]])out[k]=field(input,k,max,required);
if(!["discrepancy","field-observation"].includes(out.kind))throw Error("Invalid report kind");if(!/^[a-zA-Z0-9_.:-]+$/.test(out.claim_id)||!/^[a-zA-Z0-9_.:-]+$/.test(out.release))throw Error("Invalid claim or release identity");if(out.source_url){const u=new URL(out.source_url);if(u.protocol!=="https:"||!u.hostname||u.username||u.password)throw Error("Public HTTPS source URL required");}if(out.contact&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(out.contact))throw Error("Invalid contact email");
if(out.kind==="field-observation"&&(!out.configuration||!out.observed_date||!out.conditions||!out.measurement))throw Error("Field observations require configuration, date, conditions and measurement");
if(out.observed_date&&(!/^\d{4}-\d{2}-\d{2}$/.test(out.observed_date)||Number.isNaN(Date.parse(out.observed_date))||new Date(out.observed_date).toISOString().slice(0,10)!==out.observed_date||out.observed_date>new Date().toISOString().slice(0,10)))throw Error("Invalid observation date");
if(/-----BEGIN [A-Z ]*PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}/i.test(JSON.stringify(out)))throw Error("Remove credentials before submitting");
out.consent=true;return out;}
const hexBytes=bytes=>Array.from(bytes).map(x=>x.toString(16).padStart(2,"0")).join("");
const idPattern=/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
export async function handle(request,env){
 const url=new URL(request.url),path=url.pathname.replace(/^\/api\/?/,""),db=env.REPORTS;
 if(path==="capabilities"&&request.method==="GET")return respond(200,{submission:!!db,review:!!(db&&env.REVIEW_TOKEN),attachments:!!(db&&env.EVIDENCE),attachment_max_bytes:2097152,attachment_max_count:3,schema_version:1});
 if(!db)return respond(503,{error:"Private report storage is not configured. Use the publisher contact route."});
 const origin=request.headers.get("origin");if(origin&&origin!==url.origin)return respond(403,{error:"Origin not allowed"});
 try{
 if(path==="reports"&&request.method==="POST"){
 const input=await body(request),id=input.id,token=input.receipt_token;if(!idPattern.test(id||"")||!/^[0-9a-f]{64}$/i.test(token||""))throw Error("Invalid receipt identity");
 const data=clean(input),payload=JSON.stringify(data),ph=await digest(payload),th=await digest(token);
 const old=await db.prepare("SELECT id,token_hash,payload_hash,state,created FROM reports WHERE id=?1").bind(id).first();
 if(old)return old.token_hash===th&&old.payload_hash===ph?respond(200,{id,state:old.state,created:old.created,replayed:true}):respond(409,{error:"Receipt identity already used for different content"});
 const now=Date.now(),bucket=await digest((request.headers.get("cf-connecting-ip")||"unknown")+"|"+Math.floor(now/3600000));
 await db.prepare("DELETE FROM rate_limits WHERE expires < ?1").bind(now).run();
 const rate=await db.prepare("INSERT INTO rate_limits(id,count,expires) VALUES(?1,1,?2) ON CONFLICT(id) DO UPDATE SET count=count+1 RETURNING count").bind(bucket,now+86400000).first();
 if(rate.count>20)return respond(429,{error:"Submission limit reached. Try later or contact the publisher."});
 const created=new Date(now).toISOString();await db.prepare("INSERT OR IGNORE INTO reports(id,token_hash,payload_hash,data,state,version,created,updated,history) VALUES(?1,?2,?3,?4,'new',1,?5,?5,'[]')").bind(id,th,ph,payload,created).run();
 const saved=await db.prepare("SELECT token_hash,payload_hash,state,created FROM reports WHERE id=?1").bind(id).first();
 if(!saved)throw Error("Storage not confirmed");if(saved.token_hash!==th||saved.payload_hash!==ph)return respond(409,{error:"Receipt identity already used for different content"});
 return respond(201,{id,state:saved.state,created:saved.created});
 }
 const attachment=path.match(/^reports\/([0-9a-f-]+)\/attachments\/([0-9a-f-]+)$/i);
 if(attachment&&request.method==="PUT"){
 if(!env.EVIDENCE)return respond(503,{error:"Private attachments are not configured"});
 if(!idPattern.test(attachment[2]))throw Error("Invalid attachment identity");
 const report=await db.prepare("SELECT token_hash FROM reports WHERE id=?1").bind(attachment[1]).first(),bearer=request.headers.get("authorization")||"";
 if(!report||!bearer.startsWith("Bearer ")||await digest(bearer.slice(7))!==report.token_hash)return respond(404,{error:"Report unavailable"});
 const name=decodeURIComponent(request.headers.get("x-file-name")||"evidence").replace(/[^a-zA-Z0-9._-]/g,"_").slice(0,100),type=request.headers.get("content-type")||"";
 if(!["image/png","image/jpeg","application/pdf","text/plain"].includes(type))throw Error("Invalid attachment type");
 if(Number(request.headers.get("content-length"))>2097152)throw Error("Attachment too large");
 const reader=request.body?.getReader();if(!reader)throw Error("Attachment body required");const parts=[];let size=0;
 while(true){const r=await reader.read();if(r.done)break;size+=r.value.length;if(size>2097152){await reader.cancel();throw Error("Attachment too large");}parts.push(r.value);}
 if(!size)throw Error("Attachment body required");const bytes=new Uint8Array(size);let offset=0;for(const part of parts){bytes.set(part,offset);offset+=part.length;}
 const prefix=new TextDecoder().decode(bytes.slice(0,8));
 if(type==="image/png"&&hexBytes(bytes.slice(0,8))!=="89504e470d0a1a0a"||type==="image/jpeg"&&hexBytes(bytes.slice(0,3))!=="ffd8ff"||type==="application/pdf"&&!prefix.startsWith("%PDF-"))throw Error("Invalid attachment signature");
 if(type==="text/plain"){const text=new TextDecoder("utf-8",{fatal:true}).decode(bytes);if(/-----BEGIN [A-Z ]*PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}/i.test(text))throw Error("Remove credentials before submitting");}
 const hash=hexBytes(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes))),key=attachment[1]+"/"+attachment[2],created=new Date().toISOString();
 const old=await db.prepare("SELECT report_id,digest,state FROM attachments WHERE id=?1").bind(attachment[2]).first();
 if(old&&(old.report_id!==attachment[1]||old.digest!==hash))return respond(409,{error:"Attachment identity already used for different content"});
 if(old?.state==="ready")return respond(200,{id:attachment[2],stored:true,replayed:true});
 if(!old){const saved=await db.prepare("INSERT OR IGNORE INTO attachments(id,report_id,filename,content_type,bytes,digest,object_key,state,created) SELECT ?1,?2,?3,?4,?5,?6,?7,'uploading',?8 WHERE (SELECT count(*) FROM attachments WHERE report_id=?2)<3").bind(attachment[2],attachment[1],name,type,size,hash,key,created).run();
 if(saved.meta.changes!==1)return respond(409,{error:"Attachment limit or concurrent upload; retry original identity"});}
 await env.EVIDENCE.put(key,bytes,{httpMetadata:{contentType:type}});
 await db.prepare("UPDATE attachments SET state='ready' WHERE id=?1 AND digest=?2").bind(attachment[2],hash).run();
 return respond(201,{id:attachment[2],stored:true});
 }
 const receipt=path.match(/^reports\/([0-9a-f-]+)$/i);
 if(receipt&&request.method==="GET"){const row=await db.prepare("SELECT token_hash,state,created,updated FROM reports WHERE id=?1").bind(receipt[1]).first();const bearer=request.headers.get("authorization")||"";if(!row||!bearer.startsWith("Bearer ")||await digest(bearer.slice(7))!==row.token_hash)return respond(404,{error:"Receipt unavailable"});return respond(200,{id:receipt[1],state:row.state,created:row.created,updated:row.updated});}
 if(path==="review"||path.startsWith("review/")){
 if(!await auth(request,env.REVIEW_TOKEN))return respond(401,{error:"Reviewer authorization required"});
 const download=path.match(/^review\/attachments\/([0-9a-f-]+)$/i);
 if(download&&request.method==="GET"){if(!env.EVIDENCE)return respond(503,{error:"Private attachments are not configured"});
 const row=await db.prepare("SELECT filename,content_type,object_key FROM attachments WHERE id=?1 AND state='ready'").bind(download[1]).first();if(!row)return respond(404,{error:"Attachment unavailable"});
 const object=await env.EVIDENCE.get(row.object_key);if(!object)return respond(404,{error:"Attachment unavailable"});
 return new Response(object.body,{headers:{"content-type":"application/octet-stream","content-disposition":'attachment; filename="'+row.filename+'"',"cache-control":"no-store","x-content-type-options":"nosniff"}});}
 if(path==="review"&&request.method==="GET"){
 const after=url.searchParams.get("after")||"",afterId=url.searchParams.get("after_id")||"";
 const result=await db.prepare("SELECT id,data,state,version,created,updated,history FROM reports WHERE created > ?1 OR (created=?1 AND id > ?2) ORDER BY created,id LIMIT 100").bind(after,afterId).all();
 const metrics=await db.prepare("SELECT substr(created,1,7) AS month,state,count(*) AS count FROM reports GROUP BY month,state ORDER BY month,state").all();
 const reports=[];for(const r of result.results){const attachments=await db.prepare("SELECT id,filename,content_type,bytes,digest,created FROM attachments WHERE report_id=?1 AND state='ready'").bind(r.id).all();reports.push({...r,data:JSON.parse(r.data),history:JSON.parse(r.history),attachments:attachments.results});}
 return respond(200,{reports,metrics:metrics.results,transitions:STATES});
 }
 const target=path.match(/^review\/([0-9a-f-]+)$/i);
 if(target&&request.method==="PATCH"){
 const input=await body(request),reason=field(input,"reason",2000,true),next=field(input,"state",40,true);
 const row=await db.prepare("SELECT state,version FROM reports WHERE id=?1").bind(target[1]).first();
 if(!row)return respond(404,{error:"Report unavailable"});if(input.version!==row.version)return respond(409,{error:"Report changed; reload before editing"});if(!STATES[row.state]?.includes(next))throw Error("Invalid review transition");
 const event={at:new Date().toISOString(),from:row.state,to:next,reason};
 if(next==="duplicate"){const duplicate=field(input,"duplicate_of",80,true);if(duplicate===target[1]||!await db.prepare("SELECT id FROM reports WHERE id=?1").bind(duplicate).first())throw Error("Duplicate target must be another stored report");event.duplicate_of=duplicate;}
 if(next==="published"){const published=field(input,"published_url",2000,true),release=field(input,"published_release",80,true);const u=new URL(published);if(u.protocol!=="https:"||u.hostname!=="uas-handbook.com"||u.username||u.password||input.publisher_approved!==true||input.production_verified!==true)throw Error("Publishing requires exact handbook URL, release, publisher approval and live verification");event.published_url=published;event.published_release=release;event.publisher_approved=true;event.production_verified=true;}
 const changed=await db.prepare("UPDATE reports SET state=?1,version=version+1,updated=?2,history=json_insert(history,'$[#]',json(?3)) WHERE id=?4 AND version=?5").bind(next,event.at,JSON.stringify(event),target[1],row.version).run();
 if(changed.meta.changes!==1)return respond(409,{error:"Report changed; reload before editing"});return respond(200,{id:target[1],state:next,version:row.version+1});
 }}
 return respond(404,{error:"Route unavailable"});
 }catch(error){if(error instanceof SyntaxError||error instanceof TypeError)return respond(400,{error:"Invalid report request"});const message=error.message||"";if(/missing|long|required|Invalid|too large|Remove credentials|Field observations|JSON|already|Duplicate|Publishing/i.test(message))return respond(400,{error:message});return respond(503,{error:"Storage unavailable; submission not confirmed. Keep your draft and retry the same receipt."});}
}
