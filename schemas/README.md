# Metadata contract v1

Each asset follows `asset-v1.schema.json`. The catalog is `docs/catalog.json`: `schemaVersion: 1`, `source: {owner, repo, commit}`, `collection`, and `assets: [asset]`. `source.commit` is the default immutable 40-character lowercase Git commit SHA. For multi-repository catalogs, add `sources: {sourceId: {owner, repo, commit}}` and set an asset's optional `sourceId`. That asset resolves only through its named source; an unknown ID is an error. Each source pins its own commit. A null commit is permitted only for an empty preproduction catalog. No per-file URL or external asset host is accepted.

Asset bounds are dimensions in meters (x/y/z); triangle counts represent exported GLB geometry. File records use repository-relative paths under `assets/`, actual byte sizes, and SHA-256. Required file roles: `glb`, `blend`, `generator` (Python), `render` (PNG/WebP/JPEG). Optional `reference` must be a genuine provided/generated reference; never mislabel a render as reference. No spaces, Unicode, traversal or percent escapes in repository file paths. Suggested layout: `assets/harbor/<id>/v1.0.0/<id>.<ext>`.

Status `prototype` means generated but not approved; `review` means ready for inspection; `verified` requires recorded validation. All entries reserve copyright with `license: "All rights reserved"`; public availability grants no reuse rights. Empty catalog is intentional until real assets and an immutable source commit exist.

Two-step publication: first commit assets and generated metadata; then set the catalog source commit to that verified asset commit. Gallery-only later commits must keep that asset SHA. Never insert a moving branch name or current uncommitted hash. The public `docs/` directory contains only the fixed small frontend allowlist. Optional gallery build copies only that allowlist, not `assets/` or this schema directory.

`assetKind` is required: `prop`, `modular`, `scene`, or future `character`. Themes and categories are open-ended strings; there is no fixed catalog capacity.

## Repository federation

The browser has an explicit `ALLOWED_REPOSITORIES` list in `docs/core.mjs`; currently only `shAdow-XJY-Games/Shadow3DAssetLibrary` is authorized. A new repository requires a reviewed source change to this list, followed by its pinned entry in catalog `sources`. Metadata cannot dynamically broaden this allowlist. Models and renders are still never copied into Pages. The repository selector is generated only from actual catalog assets, without fictional empty repositories. File paths remain repository-relative, and SHA-256 and byte budgets apply independently of repository. Local cross-repository integrity checks require the publisher to materialize the exact files at their stated paths in the validation workspace.
