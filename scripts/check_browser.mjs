/* Full browser workflow using the actual API and SQLite, with a software-only provider. */
import assert from "node:assert/strict";
import {createServer} from "node:http";
import {readFile,writeFile,mkdir} from "node:fs/promises";
import {readFileSync,existsSync} from "node:fs";
import {DatabaseSync} from "node:sqlite";
import {gzipSync} from "node:zlib";
import {resolve,extname} from "node:path";
import {fileURLToPath} from "node:url";
import {createRequire} from "node:module";
import {chromium} from "playwright";
import {handle} from "../server/reports.mjs";
const ROOT=resolve(fileURLToPath(new URL("..",import.meta.url))),SITE=resolve(ROOT,"site"),OUTPUT=resolve(ROOT,".local/browser-check");
await mkdir(OUTPUT,{recursive:true});
const sql=new DatabaseSync(":memory:");for(const file of ["0001_reports.sql","0002_attachments.sql"])sql.exec(readFileSync(resolve(ROOT,"migrations",file),"utf8"));
const objects=new Map(),env={REVIEW_TOKEN:"software-only-review-token",REPORTS:{prepare(query){let values={};return{bind(...v){values=Object.fromEntries(v.map((value,index)=>[index+1,value]));return this;},async first(){return sql.prepare(query).get(values)||null;},async all(){return{results:sql.prepare(query).all(values)};},async run(){return{meta:sql.prepare(query).run(values)};}};}},EVIDENCE:{async put(k,v){objects.set(k,v);},async get(k){return objects.has(k)?{body:objects.get(k)}:null;}}};
let brokenUpdate=false;
const types={".html":"text/html",".css":"text/css",".js":"application/javascript",".json":"application/json",".svg":"image/svg+xml"};
const server=createServer(async(req,res)=>{try{const url=new URL(req.url,"http://localhost"),host="http://"+req.headers.host;if(url.pathname.startsWith("/api/")){const chunks=[];for await(const chunk of req)chunks.push(chunk);const body=Buffer.concat(chunks),r=await handle(new Request(host+req.url,{method:req.method,headers:req.headers,...(["GET","HEAD"].includes(req.method)?{}:{body})}),env);res.writeHead(r.status,Object.fromEntries(r.headers));res.end(Buffer.from(await r.arrayBuffer()));return;}
const path=resolve(SITE,"."+decodeURIComponent(url.pathname==="/"||url.pathname==="/index.html"?"/index.html":url.pathname));if(!path.startsWith(SITE+"/")){res.writeHead(403);res.end();return;}let body=await readFile(path);if(brokenUpdate&&url.pathname==="/sw.js")body=Buffer.from(body.toString().replace(/const RELEASE="([^"]+)"/,'const RELEASE="failed-update"'));if(brokenUpdate&&url.pathname==="/offline-manifest.json"){const d=JSON.parse(body);d.release="failed-update";d.hashes["/"]="0".repeat(64);body=Buffer.from(JSON.stringify(d));}const contentType=types[extname(path)]||"application/octet-stream";const compressed=contentType.startsWith("text/")||contentType.includes("json")||contentType.includes("javascript");res.writeHead(200,{"content-type":contentType,"cache-control":"no-store",...(compressed?{"content-encoding":"gzip"}:{})});res.end(compressed?gzipSync(body):body);}catch{res.writeHead(404);res.end("Unavailable");}});
await new Promise(resolve=>server.listen(0,"127.0.0.1",resolve));const base="http://127.0.0.1:"+server.address().port;
let launch={headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]};
if(process.env.CHROMIUM_EXECUTABLE_PATH)launch.executablePath=process.env.CHROMIUM_EXECUTABLE_PATH;
else if(existsSync(resolve(ROOT,".local/browser/node_modules/@sparticuz/chromium"))){const mod=await import(resolve(ROOT,".local/browser/node_modules/@sparticuz/chromium/build/index.js")),binary=mod.default||mod;launch={...launch,executablePath:await binary.executablePath(),args:binary.args};}
const browser=await chromium.launch(launch),context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage(),errors=[];
page.on("pageerror",error=>errors.push(error.message));
await context.route("**/*",route=>route.request().url().startsWith(base)?route.continue():route.abort());
try{
const started=performance.now();await page.goto(base+"/reference.html");await page.waitForFunction(()=>document.querySelector("#load-status").textContent.startsWith("Public release"));
assert.equal(await page.locator(".topbar .brand").textContent(),"UAS Handbookfield reference");assert.equal(await page.locator(".tool-rail").count(),1);assert.equal(await page.evaluate(()=>getComputedStyle(document.body).color),"rgb(210, 204, 190)");
await page.screenshot({path:resolve(OUTPUT,"reference-mobile.png"),fullPage:false});
const overflow=await page.evaluate(()=>[...document.querySelectorAll("body *")].filter(n=>n.getBoundingClientRect().right>innerWidth+1).slice(0,10).map(n=>({tag:n.tagName,cls:n.className,width:n.getBoundingClientRect().width,text:n.textContent.slice(0,80)})));assert.deepEqual(overflow,[]);
await page.screenshot({path:resolve(OUTPUT,"reference-mobile.png"),fullPage:false});
await page.selectOption('[name="dataset"]',"records");await page.selectOption('[name="status"]',"derived");await page.locator("#search").evaluate(f=>f.requestSubmit());await page.waitForFunction(()=>document.querySelectorAll(".record").length===24);
await page.locator(".record input[type=checkbox]").nth(0).check();await page.locator(".record input[type=checkbox]").nth(1).check();await page.click("#compare");assert.equal(await page.locator("#comparison table").count(),1);
const [csv]=await Promise.all([page.waitForEvent("download"),page.click("#csv")]);await csv.saveAs(resolve(OUTPUT,"filtered.csv"));assert.match(await readFile(resolve(OUTPUT,"filtered.csv"),"utf8"),/rf-|power-/);
await page.locator(".calc").nth(1).locator('button:not([type=button])').click();assert.match(await page.locator(".calc-output").nth(1).innerText(),/fsplDb: 100\.0042/);assert.match(await page.locator(".calc-output").nth(1).innerText(),/Engine 1\.0\.0/);
await page.locator(".record button[data-report-claim]").first().click();await page.waitForFunction(()=>document.querySelector("#report-status").textContent.includes("Ready"));
await page.fill('[name="description"]',"Software-only discrepancy example; no hardware field validation.");
await page.fill('[name="configuration"]',"Simulation provider, exact public release");await page.locator('[name="consent"]').check();
await page.click("#draft-save");await page.fill('[name="description"]',"Temporary edit");await page.click("#draft-load");assert.match(await page.inputValue('[name="description"]'),/Software-only/);
await page.locator("#report-form").evaluate(f=>f.requestSubmit());await page.waitForFunction(()=>document.querySelector("#report-status").textContent.includes("Stored privately"));
const [receipt]=await Promise.all([page.waitForEvent("download"),page.getByRole("button",{name:"Download private receipt"}).click()]);await receipt.saveAs(resolve(OUTPUT,"private-test-receipt.json"));
const r=JSON.parse(await readFile(resolve(OUTPUT,"private-test-receipt.json"),"utf8"));assert.equal(r.state,"new");
await page.locator('#report-status input[type=file]').setInputFiles({name:"measurement.txt",mimeType:"text/plain",buffer:Buffer.from("Deterministic software derivation; no field measurement.")});await page.getByRole("button",{name:"Attach evidence privately"}).click();await page.waitForFunction(()=>document.querySelector("#report-status").textContent.includes("Evidence stored privately"));
await page.getByRole("button",{name:"Check receipt status"}).click();await page.waitForFunction(()=>document.querySelector("#report-status").textContent.includes("updated"));
await page.screenshot({path:resolve(OUTPUT,"receipt-mobile.png")});await page.click("#report-close");assert.equal(await page.evaluate(()=>document.activeElement.hasAttribute("data-report-claim")),true);
await page.goto(base+"/review.html");assert.equal(await page.locator(".topbar .brand").textContent(),"UAS Handbookfield reference");await page.fill("#token",env.REVIEW_TOKEN);await page.locator("#auth").evaluate(f=>f.requestSubmit());await page.waitForFunction(()=>document.querySelector("#status").textContent.includes("1 private reports"));
assert.equal(await page.inputValue("#token"),"");assert.equal(await page.locator("#queue button").filter({hasText:"Download private evidence"}).count(),1);
for(const state of ["triaged","accepted","correction-prepared"]){await page.selectOption('#queue [name=state]',state);await page.fill('#queue [name=reason]',"Evidence and proposed correction checked in software; no production publication");await page.locator("#queue form").evaluate(f=>f.requestSubmit());await page.waitForFunction(s=>document.querySelector("#queue h2")?.textContent.includes(s),state);}
await page.click("#logout");assert.equal(await page.locator("#queue section").count(),0);
await page.goto(base+"/reference.html");await page.waitForFunction(()=>document.querySelector("#load-status").textContent.startsWith("Public release"));await page.click("#save-offline");await page.waitForFunction(()=>document.querySelector("#offline-status").textContent.includes("saved."),null,{timeout:120000});
const cacheAudit=await page.evaluate(async()=>{const keys=await caches.keys();const cache=await caches.open(keys.find(k=>k.startsWith("handbook-public-")));return {keys,requests:(await cache.keys()).map(r=>new URL(r.url).pathname)};});assert.ok(cacheAudit.requests.includes("/reference.html"));assert.ok(!cacheAudit.requests.some(p=>p.startsWith("/api/")||p.includes("review")));
brokenUpdate=true;await page.click("#save-offline");await page.waitForFunction(()=>!/Downloading/.test(document.querySelector("#offline-status").textContent),null,{timeout:120000});assert.equal(await page.evaluate(async()=> (await caches.keys()).includes("handbook-public-failed-update")),false);brokenUpdate=false;
await context.setOffline(true);await page.goto(base+"/reference.html");await page.waitForFunction(()=>document.querySelector("#load-status").textContent.startsWith("Public release"));await page.locator(".calc").nth(1).locator('button:not([type=button])').click();assert.match(await page.locator(".calc-output").nth(1).innerText(),/fsplDb/);
await page.locator(".record button[data-report-claim]").first().click();await page.waitForFunction(()=>document.querySelector("#report-status").textContent.includes("Save a draft"));assert.equal(await page.locator("#report-form [type=submit]").isDisabled(),true);await page.keyboard.press("Escape");
await page.goto(base+"/index.html#p101");assert.equal(await page.locator("#p101").count(),1);await context.close();const plainBrowser=await chromium.launch(launch),plain=await plainBrowser.newContext({javaScriptEnabled:false}),readable=await plain.newPage();await readable.goto(base+"/index.html#p101");assert.equal(await readable.locator("#p101").isVisible(),true);await plainBrowser.close();
assert.deepEqual(errors,[]);
const bytes=(await readFile(resolve(SITE,"assets/reference-data.json"))).length,gzipBytes=gzipSync(await readFile(resolve(SITE,"assets/reference-data.json"))).length;
assert.ok(bytes<6*1024*1024);assert.ok(gzipBytes<1024*1024);
const evidence={provider:"software-only SQLite/R2 adapter; no Cloudflare deployment or hardware validation",checks:["mobile layout","query/compare/export","calculation UI","draft/receipt/attachment","private review history","logout","complete offline release","failed update preserves old release","offline calculations and submission fallback","legacy anchor","no-JavaScript articles"],checkedAt:new Date().toISOString(),release:JSON.parse(await readFile(resolve(SITE,"release.json"))).release,snapshotBytes:bytes,snapshotGzipBytes:gzipBytes,elapsedMs:Math.round(performance.now()-started),pageErrors:errors,productionVerified:false};
await writeFile(resolve(OUTPUT,"results.json"),JSON.stringify(evidence,null,2));console.log(JSON.stringify(evidence,null,2));
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));sql.close();}
