#!/usr/bin/env python3
"""
Safe sweep: acd -> acd_ard and CLI acd-* -> acd-ard <subcmd>.
- Runs on selected globs
- Uses word-boundary regexes to avoid accidental hits
- Skips uppercase 'ACD-ARD' branding
- Dry-run by default
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GLOBS = [
    "src/**/*.py",
    "tests/**/*.py",
    "notebooks/**/*.py",
    "scripts/**/*.sh",
    "pyproject.toml",
    ".github/workflows/**/*.yml",
    "README.md",
]

# ordered replacements
REPLACES = [
    # Python imports / dotted refs
    (re.compile(r"\bfrom\s+acd(\s+import\b)"), r"from acd_ard\1"),
    (re.compile(r"\bimport\s+acd(\s+as\s+\w+)?\b"), r"import acd_ard\1"),
    (re.compile(r"\bacd\."), r"acd_ard."),
    # pyproject/toml module paths
    (re.compile(r'"acd\.cli\.'), r'"acd_ard.cli.'),
    (re.compile(r"= 'acd\.cli\."), r"= 'acd_ard.cli."),
    # CLI calls in docs/scripts/tests -> umbrella form
    (re.compile(r"\bacd-manifest\b"), r"acd-ard manifest"),
    (re.compile(r"\bacd-base\b"), r"acd-ard base"),
    (re.compile(r"\bacd-rechunk\b"), r"acd-ard rechunk"),
]


def iter_files():
    for pattern in GLOBS:
        for p in ROOT.glob(pattern):
            if p.is_file():
                yield p


def main(dry_run: bool):
    changed = []
    for p in iter_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        orig = text

        # Do NOT touch uppercase brand "ACD-ARD"
        # (We don't replace 'ACD-ARD' anywhere, so no special casing needed beyond our regexes.)

        for pat, repl in REPLACES:
            text = pat.sub(repl, text)

        if text != orig:
            if dry_run:
                print("would update:", p)
            else:
                p.write_text(text, encoding="utf-8")
                print("updated:", p)
            changed.append(p)
    if not changed:
        print("no changes needed.")
    else:
        print(f"{'would update' if dry_run else 'updated'} {len(changed)} files.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default is dry-run)")
    args = ap.parse_args()
    main(dry_run=not args.apply)
