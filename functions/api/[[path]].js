import {handle} from "../../server/reports.mjs";
export const onRequest=({request,env})=>handle(request,env);
