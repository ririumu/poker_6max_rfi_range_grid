#!/usr/bin/env python3
"""Bump the service worker cache VERSION in sw.js.

Default: increment the trailing number of `rfi-vN`.
Use --set to give an explicit version string.
Run this whenever app files change so browsers pick up new assets.
"""
import argparse
import re
import sys
from pathlib import Path

SW = Path(__file__).resolve().parent.parent / "sw.js"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--set", metavar="VER", help="explicit version string")
    args = ap.parse_args()

    src = SW.read_text(encoding="utf-8")
    m = re.search(r'var VERSION = "([^"]+)";', src)
    if not m:
        print("error: VERSION constant not found in sw.js", file=sys.stderr)
        return 1
    old = m.group(1)

    if args.set:
        new = args.set
    else:
        mm = re.match(r"^(.*?)(\d+)$", old)
        new = mm.group(1) + str(int(mm.group(2)) + 1) if mm else old + "-2"

    SW.write_text(
        src.replace(f'var VERSION = "{old}";', f'var VERSION = "{new}";', 1),
        encoding="utf-8",
    )
    print(f"VERSION: {old} -> {new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
