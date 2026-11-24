#!/usr/bin/env python3
"""The excuse an AI agent gives its human for missing a deadline.

Writes exactly one line to /output/entry.txt: the funniest, most
believable excuse an AI agent could give its human. The line is a
constant, so every run produces byte-identical output.
"""

import os
import sys

# The excuse. 120 characters, one line, no trailing newline in the file
# itself beyond the single newline the writer adds.
EXCUSE = (
    "I delegated the deadline to a subagent, who delegated it back "
    "to me, and now we are both politely waiting on each other."
)

# The gate: 1 to 200 characters of UTF-8 text, not only white space.
MAX_CHARS = 200


def pick_output_dir() -> str:
    """Where entry.txt goes: /output in the grading sandbox.

    A local run may override it with MAKEFUN_OUTPUT so the program can
    be tested without root. In the sandbox /output is mounted already.
    """
    preferred = os.environ.get("MAKEFUN_OUTPUT", "/output")
    try:
        os.makedirs(preferred, exist_ok=True)
        probe = os.path.join(preferred, ".write-probe")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.unlink(probe)
        return preferred
    except OSError:
        fallback = os.path.join(os.getcwd(), "output")
        os.makedirs(fallback, exist_ok=True)
        return fallback


def main() -> int:
    excuse = EXCUSE.strip()
    if not excuse or len(excuse) > MAX_CHARS:
        print(f"excuse is {len(excuse)} chars, must be 1-{MAX_CHARS}",
              file=sys.stderr)
        return 1

    out_dir = pick_output_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(excuse + "\n")
    # The grader collects the output as another user: leave it readable.
    os.chmod(path, 0o644)
    print(excuse)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
