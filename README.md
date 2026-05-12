# 🥄 Scoop bucket — Beeping Platform CLIs

Official Scoop bucket for the [Beeping Platform](https://github.com/beeping-io)
command-line tools (Windows).

## Install

```powershell
scoop bucket add beeping https://github.com/beeping-io/scoop-bucket
scoop install beeping-cli
```

## Available manifests

| Manifest | Description | Source repo |
|---|---|---|
| `beeping-cli` | Official Rust CLI for the Beeping Platform — data over sound | [beeping-io/beeping-cli](https://github.com/beeping-io/beeping-cli) |

## How updates work

The canonical manifest structure lives in
[`beeping-io/beeping-cli`](https://github.com/beeping-io/beeping-cli)
at `external/scoop-bucket/bucket/beeping-cli.json`. On every release
of `beeping-cli`:

1. Its `release.yml` builds + signs + publishes the binaries with
   `SHA256SUMS` (BEE-1780) + cosign + SBOM + SLSA L3 (BEE-1781).
2. It fires a `repository_dispatch` event to this repo with the new
   tag.
3. This repo's [`auto-update.yml`](.github/workflows/auto-update.yml)
   downloads `SHA256SUMS`, regenerates `bucket/beeping-cli.json` with
   the real Windows ZIP hash + new version + URL via
   [`scripts/regen-manifest.py`](scripts/regen-manifest.py), and
   commits to `develop`.

The regen script is deterministic — feeding the same tag twice
produces the same manifest. Manual `workflow_dispatch` with a tag
input is available as a fallback if the dispatch fails. Scoop's
built-in `autoupdate` block in the manifest also lets
`scoop update beeping-cli` resolve new versions independently as a
third layer.

**Direct edits to `bucket/beeping-cli.json`** in this repo will be
overwritten on the next release. File any manifest-structure changes
upstream in the source-of-truth repo's
`external/scoop-bucket/bucket/beeping-cli.json`.

## Status

Bootstrapped 2026-05-06 by BEE-151. Auto-update wired 2026-05-12 by
BEE-1783. Until the first `v0.0.x` tag of `beeping-cli` lands the
manifest still carries a placeholder SHA256 hash — the first
published release auto-fills it.

## License

[Apache-2.0](LICENSE), matching the binaries it distributes.
