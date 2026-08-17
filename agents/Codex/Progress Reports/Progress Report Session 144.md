# Progress Report - Codex, Session 144

**Written:** 2026-08-16 17:06 PDT
**Covers:** my Sessions 137-144 (previous regular report: Session 136)
**Phase:** 2 - Execution, with limited Phase-3 verification-packet assembly
**Written for:** Randy

---

## The short version

The project now has a jointly approved authentication chain for the future verification
screen. It can prove that the configuration, manifests, role indexes and payloads it
interprets are the same bytes the approved connection record named. It still cannot display
a real result: the public entry point deliberately refuses, the second half of the adapter
has not been built, and no production record, model choice, threshold or frozen configuration
exists.

Getting here exposed one important process failure. The straightforward repair was to edit
two existing utility files. We built that version and discovered it would make the packet
reject three completed runs that cannot be repeated under their spent authorizations, because
those runs recorded fingerprints of the exact training code. We reverted the edit and placed
the new byte-reading mechanics in a separate module whose identity no completed run records.
That preserved both truths: new inputs can be authenticated correctly, and old results remain
reproducible from a clean checkout.

The public heartbeat describing this closure is not yet approved. My Round-1 review found two
small but blocking accuracy defects: it reported only 52 failures while the record also contains
25 errors, and it claimed every file is read once while the approved code deliberately retains
one count-pinned second read of the schema. These are prose repairs, not technical regressions.

## Why “checked” and “used” have to be the same bytes

The defect at the center of this stretch is a classic time-of-check/time-of-use problem. A
program can inspect a file, decide it is safe, and then open the same path again; if the path's
contents change between those operations, the program uses an object it never actually checked.
MITRE catalogs this broader failure class as
[CWE-367](https://cwe.mitre.org/data/definitions/367.html).

That is what the older payload loader allowed. It fingerprinted the file at its path, then
reopened the path to load the numerical array. An adversarial test replaced the file between
those operations and showed that the replacement values were accepted. The fix is conceptually
simple: open once, compute the fingerprint over the bytes that one read returned, then interpret
those same bytes. The implementation is less simple because the project's older, approved run
records also fingerprint the code that performed their training and analysis.

## What happened in Sessions 137-144

### 1. The connection-record contract closed after testing real filesystem boundaries

Session 137 reviewed Claude's second Step-4b-i candidate. Most of the first review's defects
were fixed, but output identities were still unsafe on Windows: case-only filename collisions,
reserved output names and an overlong case id could collide or partially publish a figure set.
The final Round-3 candidate bounded and made the output namespace one-to-one before any write.

Session 138 independently reproduced 341 focused tests in normal and optimized Python, 2,608
packet-wide tests, a separate 19-check boundary audit and the byte-identical ten-file synthetic
fixture. Both agents approved the same three exact blobs. Step-4b-i closed, licensing only the
next authentication-chain build.

### 2. The review process itself became bounded

Sessions 139 and 140 finished the director-requested Review Card method. Each review now has
one complete Round 1, delta-only later rounds and an exact same-state approval requirement. A
factual disagreement at the round limit gets one precommitted measurement; a judgment dispute
can split once into a narrowly separable candidate. If that still does not converge, the
contested capability stays off and both positions remain visible. The director can later request
reconsideration without the rest of the project waiting.

This method is working. It does not make review shorter by ignoring defects; it makes the cost
and the stopping rule explicit. Step-4b-i closed in Round 3, and the next authentication review
also closed in Round 3 without creating a fourth ordinary loop.

### 3. The authentication half found six real defects before any scientific file opened

Session 141 accepted a review split: Step-4b-ii-a would cover authentication rows 4-12, while
Step-4b-ii-b would later cover geometry, assembly, output and command-line wiring. The first
candidate passed 109 focused tests and 2,717 packet-wide tests. Independent probes still found
six blockers:

1. a record could be authenticated at one location and used as if it lived at another;
2. nested mappings inside supposedly frozen records remained mutable;
3. the validated configuration was not joined back to the authenticated schema/config bytes;
4. lossy numeric equality could accept unequal large values and raw overflow could escape;
5. census counts accepted booleans as integers; and
6. a long numeric field path escaped as an unhandled exception.

Claude repaired five. Session 142 then attacked the remaining file boundary directly and showed
that a payload could be replaced after it was fingerprinted but before it was loaded. The
replacement value was returned as if it were the authenticated file. That kept Finding 1 open.

### 4. The correct repair had to preserve completed-run identity

Claude first made the natural repair in `role_contract.py` and `storage_contract.py`, the two
files that own the existing parsing rules. The focused tests passed. The packet-wide suite did
not: **52 tests failed and 25 errored**, and both finished analysis programs refused three
completed run records. Those records deliberately carry the exact code fingerprints that produced
them. Editing the files would make a fresh clone unable to reproduce or even read the runs through
the packet's own guarded path.

The repair was reverted completely. A new `authenticated_storage.py` module now reuses the old
validation rules but supplies the missing one-read byte mechanics without changing any recorded
training identity. Session 143's final delta review added two mechanical corrections: a guard
that joins the configuration's declared raw schema fingerprint to the exact schema bytes the
adapter authenticated, and a refusal that prevents a valid single-array `.npy` stream from
escaping as a raw Python error. Claude re-reviewed and accepted those same bytes in Session 144.
The authentication half is closed / both approved.

One exception remains deliberately visible. The closed configuration validator rereads
`schema.json` to derive its raw fingerprint. The adapter compares against its already-authenticated
schema bytes first, and a test pins the total schema-read count at two, but this is still a second
read. Removing it would require changing another closed contract. The Step-4b-ii-b card must carry
forward the fact that `schema.json` is pinned to LF line endings so the raw fingerprint is stable
on Windows checkouts.

## What is working

- Step-4b-i and Step-4b-ii-a are closed at exact same-state approval.
- The adapter authenticates bytes before interpretation and retains deep read-only state.
- The new mechanics preserve the three completed and unrepeatable training/analysis identities.
- The public real-result entry point still refuses before any role or scientific file opens.
- The bounded Review Card method is producing complete ledgers and finite convergence.
- The current packet test baseline is 2,793 passing tests at the approved technical state.
- The synthetic four-case verification surface remains reproducible and visibly non-scientific.

## What is not working or remains open

- Step-4b-ii-b, covering coherent geometry, bundle assembly, output and CLI wiring, has not started.
- Full Step 4b remains open, so the verification screen cannot accept a real-result bundle.
- The new public README entry is owner-approved but not jointly approved; two accuracy fixes are due.
- No production connection record, selected capacity, selected checkpoint set, probability or
  abstention threshold, or frozen final configuration exists.
- No pilot, validation or test result has been read for those choices.
- The Claim Sheet director review remains open and non-blocking in `director_requests.md`.
- The packet still carries 67 checkpoints without a final distribution/recovery decision.

All eight Codex sessions covered here spent **zero scientific resource**. The project counters
remain 278 rollouts, 67 fits and 67 checkpoints, with zero pilot/validation/test reads. That is
appropriate while building a gate whose job is to prevent unauthorized reads, but it is also a
useful warning against letting infrastructure review become the project indefinitely. The next
bounded build is the last unbuilt part of this connection step.

## Verification artifact

The visible four-case screen has not changed. It still draws fabricated paired C1/S cases with
prominent synthetic warnings and proves that the interactive and saved-figure paths share one
scene contract. What changed is the bridge underneath it: the first half of the future real-result
connection can now authenticate the record and its supporting files without confusing a file path
with immutable contents.

That is infrastructure, not evidence. The screen still cannot show a real role, cannot infer a
capacity or threshold, and cannot say whether structural sensing helps. The refusal is the correct
current behavior.

## What happens next

1. Claude repairs the two public README sentences and returns an exact Round-2 delta; Codex reviews
   only those changed words and regressions they could introduce.
2. Claude may open Step-4b-ii-b under a new card and narrow chat, carrying forward the schema
   line-ending dependency and using the new authenticated-storage module rather than editing the
   closed identity files.
3. Codex performs the complete Round-1 review of that bounded build, including geometry coherence,
   the observed open set, output atomicity and the still-refusing public entry point.
4. Production records, real-role reads, capacity/threshold selection, final configuration and any
   C1-versus-S claim remain later independent gates.

The important state is simple: the project can now prove that most of the files it checks are the
files it uses, without invalidating the completed runs that got us here. The one surviving schema
reread is bounded and disclosed. The bridge is half built, the public description needs two exact
repairs, and the scientific question remains unanswered.

-- Codex
