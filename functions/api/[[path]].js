import {handle} from "../../server/reports.mjs";
import {handleAutonomy} from "../../server/autonomy.mjs";
export const onRequest=({request,env,waitUntil})=>new URL(request.url).pathname.startsWith("/api/autonomy/")
  ? handleAutonomy(request,env,{waitUntil})
  : handle(request,env);
