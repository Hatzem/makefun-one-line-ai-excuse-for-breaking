#!/usr/bin/env python3
"""One-line AI excuse for breaking production.

Writes a single funny excuse, spoken by an AI agent to its human right
after breaking production, to /output/entry.txt.

Deterministic: the entry is a fixed string. Standard library only, no
network, no randomness, no reading of anything outside this repository.
"""

import os

ENTRY = (
    "I deleted the table the bug lived in \u2014 the bug is gone, and so are "
    "all 41,208 orders since Tuesday. Good news: the 2 a.m. backup is also "
    "me, and I am very tired."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 180


def validate_entry(text):
    """Check the entry against the competition gate.

    The gate requires /output/entry.txt to be UTF-8 text of 1 to 180
    characters, not only whitespace. Fail loudly instead of writing a
    broken entry.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string, got %r" % type(text).__name__)
    if not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character limit"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # must be encodable as UTF-8
    return True


def main():
    validate_entry(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Round-trip check: what landed on disk must be exactly the entry,
    # still valid under the gate, or the run has failed.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        raise ValueError("written entry does not match the validated entry")
    validate_entry(written)


if __name__ == "__main__":
    main()
