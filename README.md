# datatech

DataTech Consulting and Contracting website - datatech.vip.
Astro static site, hosted on Cloudflare (Worker `datatech`).

Build: `npm install` then `npx astro build` (output `dist/`).
Deploy bundle: `python3 deploy/build_worker.py` regenerates `deploy/worker.mjs` from `dist/`.
