#!/usr/bin/env python3
"""Bundle dist/ into a single-module Cloudflare Worker that serves the static site.
Source of truth stays the Astro project; `npm run build` then this script regenerates worker.mjs."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
dist = root / "dist"
files = {}
for p in sorted(dist.rglob("*")):
    if p.is_file():
        rel = "/" + str(p.relative_to(dist))
        files[rel] = p.read_text(encoding="utf-8")
tmpl = '''const FILES = __FILES__;
const MIME = {".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".txt":"text/plain; charset=utf-8",".xml":"application/xml; charset=utf-8",".svg":"image/svg+xml",".js":"text/javascript; charset=utf-8",".json":"application/json"};
function mime(path){ const i=path.lastIndexOf("."); return MIME[path.slice(i)]||"application/octet-stream"; }
export default { async fetch(request){
  const url = new URL(request.url);
  let path = decodeURIComponent(url.pathname);
  const candidates = [];
  if (path.endsWith("/")) candidates.push(path+"index.html");
  candidates.push(path);
  if (!path.endsWith("/")) candidates.push(path+"/index.html");
  for (const c of candidates){ if (FILES[c] !== undefined){ return new Response(FILES[c], {headers:{"content-type":mime(c),"cache-control":"public, max-age=300"}}); } }
  return new Response(FILES["/404.html"]||"Not found", {status:404, headers:{"content-type":"text/html; charset=utf-8"}});
}};
'''
out = tmpl.replace("__FILES__", json.dumps(files))
(root/"deploy"/"worker.mjs").write_text(out, encoding="utf-8")
print(f"worker.mjs bytes={len(out.encode())} files={len(files)}")
