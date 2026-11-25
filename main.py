"""Fortune Cookie for the Liquidated Trader — entry program (program/v1, Python 3.13, stdlib only).

Writes one original fortune-cookie line for a crypto trader who has just
been liquidated (a single line, <= 20 words, 1-160 characters) to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set, for local runs).
Deterministic: the same bytes on every run; no network, no randomness,
no reads outside this file.
"""

import os

LINE = "The oracle sees green candles ahead \u2014 just not on your chart."

# Gate the line itself: one line, 1-160 characters, not only whitespace.
assert 1 <= len(LINE) <= 160, f"line is {len(LINE)} chars, must be 1-160"
assert LINE.strip(), "line must not be only whitespace"
assert "\n" not in LINE, "line must be a single line"
assert LINE.count(".") == 1 and LINE.endswith("."), "line must be a single sentence"
# The task caps the fortune at 20 words of plain text.
assert len(LINE.split()) <= 20, f"line is {len(LINE.split())} words, must be <= 20"
# The gate counts characters, not bytes: every character must be a real
# printable character (no control characters, no hidden formatting), and
# the line must not start or end with whitespace the judge would see.
assert all(c.isprintable() for c in LINE), "line must hold printable characters only"
assert LINE == LINE.strip(), "line must not start or end with whitespace"


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Deterministic permissions for the grader: the entry must be readable
    # (0644) no matter what umask the sandbox runs with.
    os.chmod(path, 0o644)
    # Read-back check: the file on disk must hold exactly the approved
    # line, byte for byte; otherwise fail loudly, never silently.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("entry.txt does not match the approved line")


if __name__ == "__main__":
    main()
