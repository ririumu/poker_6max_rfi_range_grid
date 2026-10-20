#!/usr/bin/env python3
"""Pre-deploy validation gate for the PWA.

Checks (fails with exit 1 on any error):
  - required files exist
  - manifest parses and has required PWA fields
  - manifest icon files exist and look like PNGs
  - sw.js has a VERSION constant and every precached ASSET exists
  - no root-absolute paths (="/...") that would break subpath hosting

Usage: python3 tools/check_deploy.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

errors = []
warns = []


def err(msg):
    errors.append(msg)


def ok(msg):
    print(f"  ok    {msg}")


def check_files():
    req = [
        "index.html",
        "manifest.webmanifest",
        "sw.js",
        "icons/icon-192.png",
        "icons/icon-512.png",
        "icons/icon-maskable-512.png",
        "icons/apple-touch-icon.png",
        "icons/favicon.svg",
    ]
    for f in req:
        if (ROOT / f).is_file():
            ok(f)
        else:
            err(f"missing required file: {f}")


def check_manifest():
    try:
        man = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
    except Exception as e:
        err(f"manifest.webmanifest: invalid JSON ({e})")
        return
    for key in ("name", "short_name", "start_url", "display", "icons"):
        if key not in man:
            err(f"manifest: missing '{key}'")
    if man.get("display") != "standalone":
        warns.append(f"manifest display={man.get('display')!r} (expected 'standalone')")
    sizes = set()
    for icon in man.get("icons", []):
        src = icon.get("src", "")
        p = ROOT / src
        if not p.is_file():
            err(f"manifest icon not found: {src}")
            continue
        head = p.read_bytes()[:8]
        if not head.startswith(b"\x89PNG\r\n\x1a\n"):
            err(f"manifest icon is not a PNG: {src}")
        for s in re.findall(r"\d+", icon.get("sizes", "")):
            sizes.add(int(s))
    if "id" not in man:
        warns.append("manifest: no 'id' field (recommended for stable app identity)")
    if not ({192, 512} <= sizes):
        err(f"manifest icons must include 192 and 512 sizes, got {sorted(sizes)}")
    ok("manifest valid")


def check_sw():
    src = (ROOT / "sw.js").read_text(encoding="utf-8")
    if not re.search(r'var VERSION = "[^"]+";', src):
        err("sw.js: VERSION constant not found")
    m = re.search(r"var ASSETS = \[(.*?)\];", src, re.S)
    if not m:
        err("sw.js: ASSETS list not found")
        return
    assets = re.findall(r'"([^"]+)"', m.group(1))
    for a in assets:
        if a == "./":
            target = ROOT / "index.html"
        else:
            target = ROOT / a
        if not target.is_file():
            err(f"sw.js precaches missing asset: {a}")
    ok(f"sw.js VERSION set, {len(assets)} precached assets exist")


def check_no_absolute_paths():
    pat = re.compile(r'(?:href|src|url)\s*=\s*["\']/')
    for f in ("index.html", "manifest.webmanifest"):
        for i, line in enumerate((ROOT / f).read_text(encoding="utf-8").splitlines(), 1):
            if pat.search(line):
                err(f"{f}:{i}: root-absolute path breaks subpath hosting: {line.strip()[:80]}")
    man_src = (ROOT / "manifest.webmanifest").read_text(encoding="utf-8")
    if re.search(r'"(?:src|start_url|scope|id)"\s*:\s*"/', man_src):
        err("manifest.webmanifest: root-absolute src/start_url/scope/id")
    ok("no root-absolute paths")


def main() -> int:
    print("check_deploy:")
    check_files()
    check_manifest()
    check_sw()
    check_no_absolute_paths()
    for w in warns:
        print(f"  warn  {w}")
    if errors:
        for e in errors:
            print(f"  ERROR {e}")
        print(f"check_deploy: FAILED ({len(errors)} error(s))")
        return 1
    print("check_deploy: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
