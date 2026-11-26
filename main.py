"""One-line meeting joke writer.

The joke is a fixed string. This program only checks it against the
bounty gate (1-200 characters, one line, not only whitespace), then
writes it to $MAKEFUN_OUTPUT_DIR/entry.txt as plain text, with no
trailing newline, and reads it back to confirm the words landed intact.
"""

import hashlib
import os
from pathlib import Path

MEETING_JOKE = "We scheduled a meeting to discuss why we have too many meetings. The meeting ran over. We scheduled another one."


def vet_line(line):
    """Check the joke against the bounty gate, raising on any breach."""
    if not isinstance(line, str):
        raise ValueError("joke must be text")
    if not 1 <= len(line) <= 200:
        raise ValueError("joke must be 1-200 characters")
    if not line.strip():
        raise ValueError("joke must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("joke must be a single line")
    return line


def home_base():
    """Resolve the output folder from the environment."""
    return Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))


def drop_line(folder, line):
    """Write the joke to entry.txt in plain text mode."""
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    return target


def recheck_line(target, line):
    """Read entry.txt back and confirm it matches the joke."""
    with open(target, "r", encoding="utf-8") as handle:
        stored = handle.read()
    if stored != line:
        raise ValueError("entry.txt differs from joke")
    if stored.encode("utf-8") != line.encode("utf-8"):
        raise ValueError("entry bytes differ from joke")
    if stored.encode("utf-8").decode("utf-8") != line:
        raise ValueError("decoded text differs from joke")
    if stored != stored.rstrip():
        raise ValueError("trailing whitespace found")
    return stored


def main_flow():
    """Run the writer and report what landed on disk."""
    vet_line(MEETING_JOKE)
    folder = home_base()
    target = drop_line(folder, MEETING_JOKE)
    recheck_line(target, MEETING_JOKE)
    payload = MEETING_JOKE.encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    print(f"wrote {target} ({len(payload)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main_flow()
