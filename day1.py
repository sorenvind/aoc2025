#!/usr/bin/env python3
"""
day1.py

Small reusable helpers to read puzzle input files.

Usage:
  python3 day1.py [input_file]

If no file is given the script uses `input.txt` in the current directory.
"""

from __future__ import annotations

from pathlib import Path
import sys
import re
from typing import List, Union


def read_text(path: Union[str, Path] = "input.txt") -> str:
	"""Return the full contents of the input file as a string.

	Raises FileNotFoundError if the path does not exist.
	"""
	p = Path(path)
	if not p.exists():
		raise FileNotFoundError(f"Input file {p} not found")
	return p.read_text(encoding="utf-8")


def read_lines(path: Union[str, Path] = "input.txt", *, strip: bool = True) -> List[str]:
	"""Return a list of lines from the file.

	By default each line is stripped of leading/trailing whitespace. Set
	strip=False to preserve exact line contents.
	"""
	text = read_text(path)
	lines = text.splitlines()
	return [line.strip() for line in lines] if strip else lines



def main(argv: List[str] | None = None) -> None:
	argv = argv if argv is not None else sys.argv[1:]
	input_path = argv[0] if argv else "input.txt"
	print(f"Reading: {input_path}")

	try:
		lines = read_lines(input_path)
	except FileNotFoundError as exc:
		print(exc)
		raise

	print(f"Number of lines: {len(lines)}")
	if lines:
		print("First 10 lines (or fewer):")
		for l in lines[:10]:
			print(l)

	# --- New: parse lines that start with L or R followed by a number ---
	moves = parse_moves(lines)
	print(f"Parsed {len(moves)} moves; sample: {moves[:10]}")

	# Apply moves to a counter starting at 50 (R = add, L = subtract)
	final, hits = process_moves(moves, start=50)
	print(f"Final counter: {final}")
	# Print how many times the counter hit 0 as the final output
	print(hits)


def parse_moves(lines: List[str]) -> List[tuple]:
	"""Parse lines starting with L or R and a number.

	Returns a list of tuples: (direction: 'L'|'R', value: int, raw_line: str).
	Lines that don't match the expected format will raise ValueError.
	Spaces between the letter and the number are allowed.
	"""
	pattern = re.compile(r"^\s*([LR])\s*(\d+)\s*$", re.IGNORECASE)
	moves: List[tuple] = []
	for idx, line in enumerate(lines, start=1):
		if not line:
			# skip blank lines silently
			continue
		m = pattern.match(line)
		if not m:
			raise ValueError(f"Invalid move on line {idx}: {line!r}")
		direction = m.group(1).upper()
		value = int(m.group(2))
		moves.append((direction, value, line))
	return moves




def process_moves(moves: List[tuple], *, start: int = 50, verbose: bool = True) -> tuple:
	"""Apply moves to an integer counter and return the final value.

	- direction 'R' increases the counter by the move value
	- direction 'L' decreases the counter by the move value

	`moves` is a list of (direction, value, raw_line) as returned by
	`parse_moves`.
	"""
	counter = start
	hits = 0
	for idx, (direction, value, raw) in enumerate(moves, start=1):
		if direction == "R":
			counter += value
		elif direction == "L":
			counter -= value
		else:
			raise ValueError(f"Unknown direction {direction!r} in move {idx}: {raw!r}")
		# After each update, keep the counter within 0..99 using modulo 100
		counter %= 100
		if verbose:
			print(f"Move {idx}: {direction}{value} -> counter={counter}")
		if counter == 0:
			print("hit 0")
			hits += 1
	return counter, hits


if __name__ == "__main__":
	main()

