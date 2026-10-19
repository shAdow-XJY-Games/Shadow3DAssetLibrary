# Metadata contract v1

Each asset follows `asset-v1.schema.json`. The catalog is `docs/catalog.json`: `schemaVersion: 1`, `source: {owner, repo, commit}`, `collection`, and `assets: [asset]`. `source.commit` is the default immutable 40-character lowercase Git commit SHA. For multi-repository catalogs, add `sources: {sourceId: {owner, repo, commit}}` and set an asset's optional `sourceId`. That asset resolves only through its named source; an unknown ID is an error. Each source pins its own commit. A null commit is permitted only for an empty preproduction catalog. No per-file URL or external asset host is accepted.

Asset bounds are dimensions in meters (x/y/z); triangle counts represent exported GLB geometry. File records use repository-relative paths under `assets/`, actual byte sizes, and SHA-256. Required file roles: `glb`, `blend`, `generator` (Python), `render` (PNG/WebP/JPEG). Optional `reference` must be a genuine provided/generated reference; never mislabel a render as reference. No spaces, Unicode, traversal or percent escapes in repository file paths. Suggested layout: `assets/harbor/<id>/v1.0.0/<id>.<ext>`.

Status `prototype` means generated but not approved; `review` means ready for inspection; `verified` requires recorded validation. All entries reserve copyright with `license: "All rights reserved"`; public availability grants no reuse rights. Empty catalog is intentional until real assets and an immutable source commit exist.

Two-step publication: first commit assets and generated metadata; then set the catalog source commit to that verified asset commit. Gallery-only later commits must keep that asset SHA. Never insert a moving branch name or current uncommitted hash. The public `docs/` directory contains only the fixed small frontend allowlist. Optional gallery build copies only that allowlist, not `assets/` or this schema directory.

`assetKind` is required: `prop`, `modular`, `scene`, or future `character`. Themes and categories are open-ended strings; there is no fixed catalog capacity.

## Repository federation

The browser has an explicit `ALLOWED_REPOSITORIES` list in `docs/core.mjs`; currently only `shAdow-XJY-Games/Shadow3DAssetLibrary` is authorized. A new repository requires a reviewed source change to this list, followed by its pinned entry in catalog `sources`. Metadata cannot dynamically broaden this allowlist. Models and renders are still never copied into Pages. The repository selector is generated only from actual catalog assets, without fictional empty repositories. File paths remain repository-relative, and SHA-256 and byte budgets apply independently of repository. Local cross-repository integrity checks require the publisher to materialize the exact files at their stated paths in the validation workspace.


## Paged metadata v3

`catalog-v3.schema.json` defines the small root, and `catalog-v3-node.schema.json` describes graph nodes. The unchanged `asset-v1.schema.json` remains authoritative for every complete asset record. Runtime and full offline graph audit additionally enforce typed key ordering, contiguous ordinals, range/count/height, content-addressed path/hash/prefix, actual decoded byte limits, source ownership, globally unique IDs and exact search/facet completeness. JSON Schema alone does not prove these cross-file invariants. Record/source/facet leaves allow at most128 entries (record generation uses24); dense term leaves allow1024; posting leaves allow4096. Every decoded node still has the same256 KiB hard byte bound.

The root pins an allowlisted immutable Git commit containing `catalog/v3/<prefix>/<sha256>.json` nodes. It does not contain the library-wide source map or all leaf descriptors. The `sources` tree preserves all provenance; record leaves repeat only the source entries needed for their own assets. Assets and their original immutable download URLs are preserved exactly.

v1/v2 compatibility files remain frozen and readable. A new, separately named `app-v3.mjs` reads v3 first; 404 alone permits visible historical fallback. Normal v3 asset publication is asset commit -> graph commit -> entry commit with one final expected-parent non-force ref update. See the gallery README for the explicit delta adapter, budgets, error/count semantics and validation commands. Synthetic fixtures and unpinned graph templates must never be published as a real catalog entry.
