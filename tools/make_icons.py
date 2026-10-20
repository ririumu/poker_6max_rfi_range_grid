#!/usr/bin/env python3
"""Generate PNG icons for the RFI range grid PWA using only the stdlib.

Icon motif: the app's own 13x13 range grid showing the BTN range,
on a felt-green background. Renders at 2x and downsamples for AA.
"""
import json
import struct
import zlib
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "icons"

BG = (11, 31, 24)        # #0b1f18
CELL_OUT = (24, 51, 41)  # slightly lighter than bg
PAIR = (224, 168, 63)    # #e0a83f
SUITED = (70, 192, 124)  # #46c07c
OFFSUIT = (90, 162, 230) # #5aa2e6

R = "AKQJT98765432"
BTN = "22+ A2s+ K2s+ Q4s+ J6s+ T6s+ 96s+ 85s+ 74s+ 64s+ 53s+ 43s A2o+ K8o+ Q9o+ J9o+ T8o+"


def expand(spec: str) -> set:
    out = set()
    for tok in spec.split():
        plus = tok.endswith("+")
        if plus:
            tok = tok[:-1]
        if len(tok) == 2:
            r = R.index(tok[0])
            if plus:
                out.update(R[i] + R[i] for i in range(r + 1))
            else:
                out.add(tok)
        else:
            h, k, x = R.index(tok[0]), R.index(tok[1]), tok[2]
            if plus:
                out.update(R[h] + R[i] + x for i in range(h + 1, k + 1))
            else:
                out.add(tok)
    return out


def hand_at(i: int, j: int) -> str:
    if i == j:
        return R[i] + R[i]
    return R[i] + R[j] + "s" if i < j else R[j] + R[i] + "o"


def write_png(path: Path, w: int, h: int, px: bytearray):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += px[y * w * 4:(y + 1) * w * 4]
    def chunk(tag: bytes, data: bytes) -> bytes:
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    path.write_bytes(png)


def in_rounded(x: float, y: float, x0: float, y0: float, x1: float, y1: float, r: float) -> bool:
    if x < x0 or x >= x1 or y < y0 or y >= y1:
        return False
    cx = min(max(x, x0 + r), x1 - r)
    cy = min(max(y, y0 + r), y1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r or r <= 0


def render(size: int, maskable: bool) -> bytearray:
    ss = 2
    W = H = size * ss
    px = bytearray(W * H * 4)
    rng = expand(BTN)

    margin = size * (0.10 if maskable else 0.05) * ss
    area = W - 2 * margin
    gap = max(1 * ss, round(size * 0.007) * ss)
    cell = (area - 12 * gap) / 13
    rad = cell * 0.24

    for y in range(H):
        for x in range(W):
            i = (y * W + x) * 4
            px[i:i + 4] = bytes((*BG, 255))

    for i in range(13):
        for j in range(13):
            h = hand_at(i, j)
            col = CELL_OUT if h not in rng else (
                PAIR if i == j else SUITED if i < j else OFFSUIT)
            x0 = margin + j * (cell + gap)
            y0 = margin + i * (cell + gap)
            for yy in range(int(y0), min(int(y0 + cell + rad + 2), H)):
                for xx in range(int(x0), min(int(x0 + cell + rad + 2), W)):
                    if in_rounded(xx + 0.5, yy + 0.5, x0, y0, x0 + cell, y0 + cell, rad):
                        idx = (yy * W + xx) * 4
                        px[idx:idx + 4] = bytes((*col, 255))

    # downsample 2x -> 1x
    out = bytearray(size * size * 4)
    for y in range(size):
        for x in range(size):
            acc = [0, 0, 0, 0]
            for dy in range(ss):
                for dx in range(ss):
                    idx = ((y * ss + dy) * W + (x * ss + dx)) * 4
                    for c in range(4):
                        acc[c] += px[idx + c]
            oi = (y * size + x) * 4
            for c in range(4):
                out[oi + c] = acc[c] // (ss * ss)
    return out


def main():
    OUT.mkdir(exist_ok=True)
    for size, maskable, name in [
        (192, False, "icon-192.png"),
        (512, False, "icon-512.png"),
        (512, True, "icon-maskable-512.png"),
        (180, False, "apple-touch-icon.png"),
    ]:
        write_png(OUT / name, size, size, render(size, maskable))
        print("wrote", name)


if __name__ == "__main__":
    main()
