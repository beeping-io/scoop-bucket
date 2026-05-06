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

The canonical manifest lives in
[`beeping-io/beeping-cli`](https://github.com/beeping-io/beeping-cli)
at `external/scoop-bucket/bucket/beeping-cli.json`. Each release
automatically syncs the SHA256 hash here (BEE-1783, post-BEE-151
bootstrap). Scoop's built-in `autoupdate` config in the manifest also
lets `scoop update beeping-cli` resolve new versions from GitHub
Releases independently.

**Direct edits to this repo will be overwritten** by the next release sync.
File changes upstream in the source-of-truth repo.

## Status

Bootstrapped 2026-05-06 by BEE-151. Manifest uses a placeholder SHA256
hash until the first `v0.0.x` tag of `beeping-cli` lands. Until then,
`scoop install beeping-cli` will fail with a hash mismatch — expected.

## License

[Apache-2.0](LICENSE), matching the binaries it distributes.
