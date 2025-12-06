#!/usr/bin/env python3
"""
day4.py

Read a grid from a file (default `day4-sample.txt`) into a 2D list `paper_map`.
For each cell that contains '@', compute may_access which is True if there are
<= 3 adjacent cells (including diagonals and the cell itself) that contain '@'.

Print coordinates (row, col) for cells where may_access is True and print the
final count.
"""

from __future__ import annotations
from pathlib import Path
import sys
from typing import List, Tuple


def read_grid(path: str) -> List[List[str]]:
    text = Path(path).read_text(encoding="utf-8")
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    grid: List[List[str]] = [list(line) for line in lines]
    return grid


def neighbors(r: int, c: int, rows: int, cols: int):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr = r + dr
            cc = c + dc
            if 0 <= rr < rows and 0 <= cc < cols:
                yield rr, cc


def main(argv: List[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    input_path = argv[0] if argv else "day4-sample.txt"
    p = Path(input_path)
    if not p.exists():
        print(f"Input file {p} not found")
        return

    paper_map = read_grid(input_path)
    rows = len(paper_map)
    cols = len(paper_map[0]) if rows else 0

    may_access_coords: List[Tuple[int, int]] = []

    for r in range(rows):
        for c in range(cols):
            if paper_map[r][c] != "@":
                continue
            # count adjacent '@' excluding the cell itself
            count = 0
            for rr, cc in neighbors(r, c, rows, cols):
                if rr == r and cc == c:
                    continue
                if paper_map[rr][cc] == "@":
                    count += 1
            if count <= 3:
                may_access_coords.append((r, c))
                print((r, c))

    print(len(may_access_coords))


if __name__ == "__main__":
    main()
