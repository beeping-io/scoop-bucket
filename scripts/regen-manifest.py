#!/usr/bin/env python3
"""Regenerate Scoop manifest SHA256 hash + version from a SHA256SUMS file.

BEE-1783 — invoked by `.github/workflows/auto-update.yml` after a new
`beeping-cli` release publishes. Reads the release's `SHA256SUMS`
asset, locates the `x86_64-pc-windows-msvc.zip` line, rewrites the
manifest's `version`, `architecture.64bit.url`, `architecture.64bit.hash`,
and `architecture.64bit.extract_dir` fields in-place.

Scoop's manifest schema uses the `version` field literally in the
`url` (no template variable substitution at install time), so we
rewrite both fields explicitly to keep them in lockstep.

Usage:
    regen-manifest.py --manifest bucket/beeping-cli.json \\
                      --sha256sums /tmp/SHA256SUMS \\
                      --version 0.1.2

If the Windows binary line is missing from SHA256SUMS the script
exits non-zero rather than producing a half-updated manifest.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

WINDOWS_TARGET = "x86_64-pc-windows-msvc"
WINDOWS_ARCHIVE = f"beeping-cli-{WINDOWS_TARGET}.zip"


def parse_sha256sums(text: str) -> str | None:
    """Return the SHA256 of the Windows zip, or None if missing.

    Accepts both GNU format (`hash  file`) and BSD format
    (`SHA256 (file) = hash`).
    """
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([0-9a-f]{64})\s+\*?(\S+)$", line)
        if m:
            sha, fname = m.group(1), m.group(2)
        else:
            m = re.match(r"^SHA256 \(([^)]+)\) = ([0-9a-f]{64})$", line)
            if m:
                fname, sha = m.group(1), m.group(2)
            else:
                continue
        if fname == WINDOWS_ARCHIVE:
            return sha
    return None


def rewrite_manifest(manifest: dict, version: str, sha: str) -> dict:
    manifest["version"] = version
    arch64 = manifest["architecture"]["64bit"]
    arch64["url"] = (
        f"https://github.com/beeping-io/beeping-cli/releases/download/"
        f"v{version}/{WINDOWS_ARCHIVE}"
    )
    arch64["hash"] = sha
    arch64["extract_dir"] = f"beeping-cli-{WINDOWS_TARGET}"
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--sha256sums", type=Path, required=True)
    ap.add_argument(
        "--version",
        required=True,
        help="Tag without leading 'v' (e.g. 0.1.2)",
    )
    args = ap.parse_args()

    sha = parse_sha256sums(args.sha256sums.read_text())
    if sha is None:
        print(
            f"::error::SHA256SUMS missing line for {WINDOWS_ARCHIVE}",
            file=sys.stderr,
        )
        return 1

    manifest = json.loads(args.manifest.read_text())
    new = rewrite_manifest(manifest, args.version, sha)
    # 2-space indent matches the existing manifest style produced by
    # Scoop tooling and the BEE-151 bootstrap. `ensure_ascii=False`
    # preserves literal unicode (em dash in the description, etc.) so
    # the diff stays minimal across regens.
    args.manifest.write_text(
        json.dumps(new, indent=2, ensure_ascii=False) + "\n",
    )

    print(
        f"::notice::Regenerated {args.manifest} -> version {args.version}",
    )
    print(f"  hash: {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
