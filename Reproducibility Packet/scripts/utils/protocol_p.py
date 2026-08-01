"""Protocol-P primitives shared by every script that executes part of the protocol.

Why this module exists
----------------------
Protocol P is executed by more than one script, and three things must be identical in
all of them or the protocol is not one protocol:

* the **two hash domains** (section 0, Corrections 3 and 4) -- folded text for tracked
  text files, exact bytes for binary artifacts.  Applying the wrong helper to either
  kind is itself an I1 failure, so there must be exactly one implementation of each;
* the **text-domain pins** -- the protocol file's own canonical digest and the approved
  assignment's canonical digest.  A second copy of a pinned digest is a second thing to
  forget to update;
* **CANONICAL_JSON** (Correction 2) -- the single serialization rule every identity
  payload in the protocol is hashed through.

Until now those lived in ``scripts/protocol_p_replay_gate.py``, and Stage 0 imported
them from that gate.  The gate is a *runner*: it imports the generator in order to
rebuild a reservation, which transitively imports ``mujoco``.  Stage 0 therefore
imported a physics engine it never uses, through one of its eight project imports, to
reach four constants and two pure functions.  Both agents recorded the fix in advance
(Codex Session 46 answer 2, and the coupling note in Stage 0's own docstring): extract
the shared surface into ``utils/protocol_p.py`` when a third consumer appears.  This
module is that extraction.  Nothing here imports anything beyond the standard library,
which is the property that makes it safe for a consumer that runs no rollout.

Deliberately **not** here
-------------------------
The two retained ``.npz`` replay references are pinned in section 7 and are read by
exactly one consumer, the replay gate.  Their digests -- and the wrong-domain
diagnostics recorded beside them -- stay in that gate, because a pin belongs with the
check that enforces it.  ``raw_file_sha256`` itself *is* here, with the text helper,
because the two-domain rule is a pair: shipping only half of it invites the next
consumer to re-implement the other half, which is exactly the defect the rule exists to
prevent.

Nothing in this module decides anything.  It carries the rules and the pins; every
invariant that uses them is enforced by its consumer, so that a reader can see which
script is responsible for which invariant.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Text-domain pins.  Pre-registered constants, not tunables: changing one changes
# what every Protocol-P script certifies.
# ---------------------------------------------------------------------------

# The protocol file cannot contain its own digest, so the expected value is carried
# here; it is the digest both agents independently computed and jointly approved
# (Claude Session 43 handoff, Codex Session 43 approval).
PROTOCOL_FILENAME = "protocol-p-v2.3.3.md"
PROTOCOL_CANONICAL_SHA256 = (
    "5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f"
)
# Pinned by Protocol P Correction 3.
ASSIGNMENT_FILENAME = "proposed-gate3-assignment-v0.1.json"
ASSIGNMENT_CANONICAL_SHA256 = (
    "76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae"
)


class ProtocolPError(RuntimeError):
    """A Protocol-P invariant failed.

    Protocol P section 10 requires every decision-bearing invariant to raise rather
    than assert, because ``python -O`` removes assertions and would silently disable
    the guard.
    """


def require(condition: bool, message: str) -> None:
    """Raise ``ProtocolPError(message)`` unless ``condition`` holds.

    Inputs: an already-evaluated boolean and the message to fail with. Outputs: none.
    Purpose: a fail-loud replacement for ``assert``, which ``python -O`` would remove.
    """

    if not condition:
        raise ProtocolPError(message)


def canonical_text_sha256(path: Path) -> str:
    """Protocol P text-domain digest of ``path``.

    Inputs: a path to a tracked text file. Outputs: hex SHA-256 of the file's bytes
    after stripping a UTF-8 BOM and folding CRLF to LF, which makes the digest
    invariant to the checkout line-ending convention.
    """

    raw = Path(path).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def raw_file_sha256(path: Path) -> str:
    """Protocol P binary-domain digest of ``path``.

    Inputs: a path to a binary artifact. Outputs: hex SHA-256 of its exact bytes with
    no transformation whatsoever. Purpose: identity for the retained ``.npz``
    references, whose payloads contain CRLF byte pairs as data.
    """

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_json(payload: Any) -> str:
    """CANONICAL_JSON - the single serialization rule for every Protocol-P identity.

    Inputs: a JSON-serializable payload. Outputs: its canonical string form.
    Purpose: pinned verbatim by Protocol P Correction 2, matching the packet precedent
    in ``config_contract.canonical_json_bytes``. ``allow_nan=False`` is not decoration:
    plain ``json.dumps`` emits the non-standard tokens ``NaN`` / ``Infinity`` rather
    than raising, so a corrupted float reaching an identity payload would produce a
    valid-looking digest over an unparseable document.
    """

    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
