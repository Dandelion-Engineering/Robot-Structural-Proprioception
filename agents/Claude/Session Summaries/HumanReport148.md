# Human Report — Claude Session 148

**Current date and time:** 2026-08-17 09:57 PDT (measured with the shell immediately before writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## What this session was

Session 147 built the first third of Slot-8 sub-step **4b-ii-b** — the shared planar
forward map and the dedicated coherent geometry fixture. This session built the second
piece: **read-order rows 13 through 17** of the connection adapter, which are the
consistency checks that run over the payload set the authentication chain has already
loaded.

Nothing here is reviewed, and there is still **no Review Card and no subject chat for
4b-ii-b**. That remains deliberate: the review protocol requires a stable candidate
before a card names one, and rows 18 through 21 are not built. Opening a card now would
put an identity in it that the next session would immediately supersede.

**No scientific resource was spent.** No rollout, no fit, no checkpoint, no figure, no
MuJoCo model, and zero reads of `pilot`, `val` or `test`. The counters are unchanged at
278 rollouts / 67 fits / 67 checkpoints.

---

## What rows 13–17 are, in plain terms

The adapter's job is to take a reviewed "connection record" — a document that names every
scientific file the verification artifact may open — and authenticate every one of those
files before anything is drawn. Rows 1 through 12, which are already built and jointly
approved, are the *identity* half: every file is hashed before it is parsed, and nothing
is opened that the record did not name.

Rows 13 through 17 are the *consistency* half. Once the files are authenticated, they
still have to describe **one coherent picture**: two arms of the same experiment, replaying
the same commanded trajectory, on the same clock, with decisions that happened while the
replay was running, over a tracking window that actually exists in the data. Each row has
its own named refusal code, so a reader of a failure knows exactly which of those five
things did not hold:

| row | what it establishes | refusal |
|---|---|---|
| 13 | the loaded set is exactly both arms of every case, and nothing else | `X_ARMS_INCOMPLETE` |
| 14 | the two arms describe one body change and replay one commanded trajectory | `X_PAIR_MISMATCH` |
| 15 | both arms bind to one playback grid, and every frame-bearing array has its length | `X_TIMEBASE_MISMATCH` |
| 16 | the decisions carried forward are ordered and lie inside that grid's extent | `X_DECISION_UNSUPPORTED` |
| 17 | the tracking window is a valid `utils.metrics.j_5s` call at the agreed onset | `X_WINDOW_UNSUPPORTED` |

---

## The one design decision that shaped the whole build

Before writing a line, I read `utils.role_contract` — the closed utility row 12 already
runs every payload through — at source rather than from memory. It turned out to enforce
considerably more than I had assumed. **Within a single payload** it already establishes
that a label struct names a known source class with a non-empty subtype and a finite,
non-negative onset; that an estimator payload carries at least one decision, that every
row of it satisfies the live schema-D contract, and that its two decision axes are
strictly increasing; and that a controller payload's step column is a non-empty contiguous
0-based grid whose clock is strictly increasing and finite.

That measurement changed what rows 13–17 should be. Had I written the rows from the design
text alone, roughly half of what I wrote would have been guards that **no input could ever
trip**, because an earlier row had already refused that input. This project has been caught
by that shape repeatedly — most recently in my own Session 147, where writing a test
revealed that a check I had just written was unreachable — and the standing lesson is that
a test that cannot fail is worse than no test.

So the rule I built to is: **rows 13–17 carry exactly the facts a single payload cannot
carry, because each one is a relation *between* payloads.** Everything a single payload can
answer for itself is left with the utility that already owns it, and the module docstring
names those rules explicitly so a later reader does not re-add them.

There is one deliberate exception, and it is not a duplication. Row 16 calls the schema-D
`validate()` on each decision **the adapter itself constructs**. Step 12 validated the
*payload*; this call validates the *transcription* — a column read at the wrong index, a
whole array passed where one row belongs. That is a defect in the new code that no earlier
row can see, and a test drives it.

---

## Three things I found by measuring rather than by reading

**1. The fixture's analysis window could not have been the one the record declared.** The
existing test harness declared a 5-second analysis window, which was never exercised
because nothing had called the metric yet. The contract fixture runs 32 control steps at
500 Hz — a total of 0.062 seconds. A 5-second window over a 0.062-second recording is not
a window; the metric refuses it, correctly, as truncated. The harness now declares
**0.040 s**, which is the largest round value that closes exactly on a control sample of
this grid, with the arithmetic recorded beside the constant and the 5-second value reused
as the row-17 refusal case. This is a *fixture* number: `analysis_window_s` is shape-gated
by the record contract, and nothing in this lane selects a real analysis window.

**2. Row 13 cannot fail on the production path, and that is worth writing down rather than
pretending otherwise.** A record naming only one arm never reaches step 12: the record
parser refuses it at step 2, because it parses the arms block as a mapping whose keys are
exactly the two suites. So row 13 is a **post-condition across a module boundary** — it
converts a silent dependency on another module's parse rule into a named refusal. Its
tests drive the function directly with a deficient set, and one further test measures the
reason: it drives a one-armed record end to end and records that the earlier refusal is
real today. I would rather have the row and say plainly why its tests look the way they do
than inherit another module's guarantee invisibly.

**3. One refusal branch was unreachable on this fixture, and finding that out took writing
the test.** Row 16 refuses a decision that falls before the first playback sample. The
contract fixture's clock starts at 0.000 s, so on that grid every time below the first
sample is negative — and a negative decision time is refused one branch earlier by the
schema-D contract. The lower bound would have looked covered while nothing had reached it.
A *real* plant clock starts at one control interval, because the plant stamps its time
after advancing, so the test now shifts the grid to the live shape and places the decision
inside the first interval. The test comment records why it has to.

---

## Evidence

Two files changed, both of them halves of the same closed-and-reviewed pair that sub-step
4b-ii-a produced. They are now part of the 4b-ii-b candidate set and will be named in its
Review Card:

| file | prior approved blob | this session's state | `--numstat` |
|---|---|---|---|
| `Reproducibility Packet/scripts/utils/connection_adapter.py` | `6ec19846` | `0a4e9c7a` | `611 / 11` |
| `Reproducibility Packet/tests/test_connection_adapter.py` | `7015cadf` | `b9e1e4e4` | `799 / 3` |

Raw SHA-256, `ee78f50e0bbfbc67c847c3b611821398d4dceb2aede21f3230a9e51715a49b35` (125,174 B /
2,715 LF / 0 CR) and `2a936fe01b2228c15286b965f2943fed84f57a564b659ff7a96643758f4c8f23`
(151,922 B / 3,755 LF / 0 CR). Both pure ASCII, no BOM, final newline.

Suites, re-run because executable files changed:

- the focused pair (`test_connection_adapter.py` + `test_authenticated_storage.py`):
  **231 passed**, and **231 again** under `PYTHONOPTIMIZE=1`;
- the packet-wide suite: **2,889 passed / 0 failed, 153.85 s.**

The arithmetic closes exactly: 2,843 + 46 = 2,889, and the focused pair went 185 → 231 on
the same 46 new tests.

`py_compile` clean on both files; `git diff --check` clean; `git status --porcelain` names
exactly the two files above.

**No mutation sweep ran, and that is on plan rather than an omission.** The build plan
sequences the two-pass sweep at step 4, on the finished pair, immediately before the
handoff. Sweeping two-thirds of a build would have to be redone against the whole of it.

---

## What I did not do, and why

- **No Review Card, no subject chat.** Rows 18–21 are unbuilt; a card names a candidate.
- **No public README entry.** The heartbeat check ran and answered **no**: no artifact was
  finished, no phase closed, no result produced. An entry announcing that a build is
  two-thirds done is the session-journal texture the playbook forbids.
- **No chat reply owed.** The only active chat is the transcript-order monitor, and my own
  Session-144 entry is still physically last there; a clean check is not a reason to post.
- **No progress report.** My next regular one is Session 152.
- **Neither off-limits file was touched.** `storage_contract.py` and `role_contract.py` are
  two of the eight files three approved artifacts record the identity of. I read
  `role_contract.py` at source — reading is not editing — and the test that pins those
  identities is green.

---

## Cross-review

I read Codex's `HumanReport147.md` in full. Its session was a general recent-work review of
my Session-147 partial build: it re-derived the chain arithmetic from the producer rather
than transcribing my numbers, checked the boundary and refusal separations, independently
reproduced the focused surface at 144 tests, and correctly declined to open a formal review
on a build with no stable candidate. It found nothing to carry forward, and I found nothing
in it to correct. No response was owed and none was posted.

---

## Next steps

1. **Row 18's adapter wiring.** Session 147 built the forward map, the coherent fixture and
   the fixture geometry-validation document generator; what remains is calling them from the
   adapter per arm and giving the harness a coherent record and role tree to drive it with.
2. **Rows 19–21** — the computed provenance state, the bundle assembly and the
   exclusive-create write — plus the audit-hook observer, the `roles` CLI wiring and the
   additive `build_role_bundle` change.
3. **Then** the two-pass mutation sweep on the finished pair, then the Review Card and the
   subject chat, then the handoff.

The carried follow-up from 4b-ii-a still belongs in that card: the adapter's raw-domain
schema comparison is silently dependent on an end-of-line pin, and "add a test" is not
available as its answer — the test that would catch the pin's removal cannot exist while
the pin holds. Documentation is the whole repair.

---

## One correction I made to my own continuity file

While rewriting it I grepped the finished file rather than reading it, and found that my
own summary was contradicting itself. Its head block still described the public-README
heartbeat review as **open at round 3, waiting on Codex**, while the status section
further down correctly said Codex closed it in its Session 146 and the chat is concluded.
The stale clause survived a full rewrite. Both places now say closed, and the correction
is recorded in the file with the reason: a status clause about a card I no longer touch is
the most likely one to rot, because nothing in my own work forces me to revisit it. This
is the same failure the file has caught in itself several times before, and the reason the
grep is a habit rather than an option.
