#!/usr/bin/env python3
"""
day5.py

Read input containing two sections separated by a blank line:
- first section: ranges like 3-5 (inclusive)
- second section: search ids, one per line

Compress ranges by merging overlapping or adjacent ranges. Then, for each
search id, print it if it is "fresh" (contained in any compressed range).
At the end print the count of fresh ids.
"""
from __future__ import annotations
from pathlib import Path
import sys
from typing import List, Tuple


def parse_ranges(lines: List[str]) -> List[Tuple[int,int]]:
    ranges: List[Tuple[int,int]] = []
    for line in lines:
        if not line.strip():
            continue
        a,b = line.split("-")
        ranges.append((int(a), int(b)))
    return ranges


def compress_ranges(ranges: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    if not ranges:
        return []
    # sort by start
    ranges = sorted(ranges, key=lambda x: x[0])
    out: List[Tuple[int,int]] = []
    cur_s, cur_e = ranges[0]
    for s,e in ranges[1:]:
        # if overlapping or adjacent (s <= cur_e + 1)
        if s <= cur_e + 1:
            cur_e = max(cur_e, e)
        else:
            out.append((cur_s, cur_e))
            cur_s, cur_e = s, e
    out.append((cur_s, cur_e))
    return out


def main(argv: List[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    path = argv[0] if argv else "day5-sample.txt"
    p = Path(path)
    if not p.exists():
        print(f"Input file {p} not found")
        return

    parts = p.read_text(encoding="utf-8").splitlines()
    # split into two sections by first blank line
    try:
        blank_idx = parts.index("")
    except ValueError:
        print("Expected a blank line separating ranges and searches")
        return
    range_lines = parts[:blank_idx]
    search_lines = parts[blank_idx+1:]

    ranges = parse_ranges(range_lines)
    searches = [int(l.strip()) for l in search_lines if l.strip()]

    compressed = compress_ranges(ranges)
    # print each compressed range on its own line
    for s, e in compressed:
        print(f"{s}-{e}")

    # final output: total length across all compressed ranges (inclusive)
    total_length = sum(e - s + 1 for s, e in compressed)
    print(total_length)

if __name__ == "__main__":
    main()
