# Gallery development and validation

Public frontend source lives only in `../docs/`. GitHub Pages should publish `main:/docs`; there is no generated duplicate directory, build dependency, workflow requirement, model bundle, Release, or Git LFS usage. `docs/` contains HTML, CSS, ES modules, metadata and `.nojekyll` only. Every thumbnail, GLB, Blender source and generator link is derived from its explicitly allowlisted repository and pinned raw GitHub asset commit.

Run from repository root with Node.js 22 or later:

    node gallery/test.mjs
    node gallery/build.mjs --check
    BASE_REF=<trusted-base-commit> node gallery/build.mjs --check

The last command additionally rejects tracked-file deletion against the base commit. This is a local check, not a branch-protection rule. The publisher must also enforce non-force updates to an expected parent and preserve all tree paths. Optional packaging to a fresh directory is available with `node gallery/build.mjs /tmp/shadow-pages-check`; it copies the seven-file allowlist only and never deletes contaminated outputs.

Budgets: public file <=256 KiB; total Pages <=1 MiB; GLB <=5 MiB; image <=2 MiB; Python generator <=512 KiB; Blender file <=25 MiB; <=100,000 triangles and <=64 materials per catalog asset. Checks verify actual file sizes and SHA-256 against metadata. An empty catalog is supported and does not claim any completed assets.

Preview locally with `python -m http.server 8080 --directory docs`. Three.js 0.180.0 and its official addon modules load lazily from the pinned jsDelivr npm version only when the visitor opens the 3D preview. No npm install is needed. Catalog browsing and renders do not require Three.js. A CDN failure is shown as a recoverable preview error; downloads remain available. GLBs must be self-contained; external model subresources are rejected. The Three.js dependency retains its upstream MIT license; it does not license project source, models or artwork.

Manual browser QA still required: desktop/mobile layout, filter/reset, repeated open/close and rapid mode changes, Escape dismissal, WebGL rendering/orbit/zoom/reset, actual immutable raw downloads, unavailable reference state, failed network state, keyboard focus. Node tests alone do not validate visual appearance or WebGL.

All original project source, models and artwork: All rights reserved. Public visibility and download access are not an open-source or asset reuse license. Obtain separate permission before reuse.
