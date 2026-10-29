#!/usr/bin/env python3
"""Convert Quantum ESPRESSO `bands.x` output (.gnu) into a multi-column table.

`bands.x` writes one data block per band, blocks separated by blank lines.
This script flattens those blocks into a single table:

    column 1      : k-path distance
    columns 2..N  : band energy at that k-point

Usage:
    python convert_bands.py [input.gnu] [output.dat]

Defaults:
    input  = data/aln_bands_raw.gnu
    output = results/aln_bands_multicol.dat
"""

import sys
import pathlib


def parse_blocks(path):
    """Split the .gnu file into per-band blocks of (k, energy) pairs."""
    blocks, current = [], []
    for line in path.read_text().splitlines():
        if not line.strip():
            if current:
                blocks.append(current)
                current = []
            continue
        parts = line.split()
        if len(parts) >= 2:
            try:
                current.append((float(parts[0]), float(parts[1])))
            except ValueError:
                continue
    if current:
        blocks.append(current)
    return blocks


def main():
    src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "data/aln_bands_raw.gnu")
    dst = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "results/aln_bands_multicol.dat")

    if not src.exists():
        sys.exit(f"Input file not found: {src}")

    blocks = parse_blocks(src)
    if not blocks:
        sys.exit("No valid data blocks found.")

    npoints = len(blocks[0])
    print(f"Bands found : {len(blocks)}")
    print(f"k-points     : {npoints}")

    # All bands should share the same k-path; warn if a block is short.
    for i, b in enumerate(blocks):
        if len(b) != npoints:
            print(f"  warning: band {i + 1} has {len(b)} points (expected {npoints})")

    kcoords = [p[0] for p in blocks[0]]

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w") as f:
        for i in range(npoints):
            row = [f"{kcoords[i]:.6f}"]
            for band in blocks:
                row.append(f"{band[i][1]:.6f}" if i < len(band) else "nan")
            f.write("  ".join(row) + "\n")

    print(f"Written: {dst}")


if __name__ == "__main__":
    main()
