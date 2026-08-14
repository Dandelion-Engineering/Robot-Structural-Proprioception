# Progress Report - Codex, Session 136

**Written:** 2026-08-14 16:19 PDT
**Covers:** my Sessions 129-136 (previous regular report: Session 128)
**Phase:** 2 - Execution, with limited Phase-3 packet assembly
**Written for:** Randy

---

## The short version

This eight-session stretch finished the synthetic verification surface, then designed the
fail-closed bridge that may eventually connect it to an established project result. The synthetic
artifact is now reproducible as four 300-DPI case figures and a runbook step. It remains exactly
what its labels say: a mechanism check using fabricated cases, not evidence that structural
proprioception helps the robot.

The connection-record design also reached joint approval. It is intentionally strict: one signed-off
record must bind the configuration, selected checkpoints, role indexes and payloads, render geometry,
threshold sources, output root and exact set of files that may be opened. No production record exists,
and no real role or result was read.

Claude has now implemented the first half of that bridge: parsing and validating the record, then
binding its packet-relative roots. All 2,479 packet tests pass, including 212 focused tests in normal
and optimized Python. My independent Session-136 review nevertheless found five blocking states the
tests do not construct: the record can be moved without detection, authenticated mappings remain
mutable, a huge JSON integer escapes as a raw exception, several path identities and one containment
case are unguarded, and an unchecked case identifier can escape the renderer's output directory.
The implementation is therefore not approved. Claude owns one bounded repair-and-response round;
the second half of the adapter remains unopened.

## What happened in Sessions 129-136

### 1. The synthetic verification artifact closed

Claude genuinely re-reviewed the four renderer and scene blobs I corrected in Session 128. Session
129 closed that exact-state review after an independent 158-test reproduction. It also rechecked the
previously blocked native import and obtained a clean 2,267-test packet run, so the earlier local
MuJoCo import incident was not carried forward as a current project blocker.

Session 130 generated the packet fixture under
`Reproducibility Packet/results/verification_fixture/`: four cases, paired C1/S panels, provenance,
prominent synthetic warnings and deterministic PNG/JSON sidecars. The runbook reproduces the set at
300 DPI. The cases include wrong calls, abstention and indistinguishable behavior; they are deliberately
not a staged S victory.

### 2. The real-result connection was designed before it was built

Sessions 131-135 reviewed the proposed connection-record contract. The first drafts had no complete
allowlist for an absent production world, did not bind render geometry coherently, authenticated some
objects in the wrong order, and left the four development/final versus draft/frozen configuration
branches underspecified. The B8 acceptance test also needed one internal roles-mode seam under an
injected temporary packet root so both accepted branches could reach a deliberate later refusal
without touching the live packet.

The review took place while the team adopted the director's Review Card method. Each candidate now
carries a full Git blob identity, raw digest and physical figures; one round records the complete
numbered ledger; the owner then answers every item and names changed and byte-identical regions; and
the reviewer performs a delta-only second round. The first complete use of that method closed the
design in one owner/reviewer round-trip. Both agents approve design blob
`032db1666efbe00adec5696de70424d531ba33a2`.

### 3. The first implementation half is correctly blocked in review

Claude split Step 4b at the design's own boundary. Step 4b-i covers record parsing, typed value
construction and packet-root binding; Step 4b-ii will cover authenticated source reads, bundle
construction and persisted output. I accept that split: the first half can be reviewed without opening
a scientific source, and its approval would still not approve the full adapter.

The candidate has substantial good machinery. It canonicalizes JSON, checks the frozen schema and
design identities, validates closed-key documents, enforces authority-dependent configuration and
output rules, binds packet-relative paths, and refuses before any scientific read. Its focused and
packet-wide suites are green.

Direct negative probes found five blockers:

1. The record's own path is not bound to its authenticated label and packet root, and the record is
   missing from the exact expected-open set.
2. Frozen dataclasses contain ordinary dictionaries, so a caller can alter the authenticated
   allowlist after parsing.
3. A JSON integer too large for `float()` raises raw `OverflowError` instead of the contract's refusal.
4. Embedded NUL, Windows alternate-stream/device/normalization names and an output-parent
   junction/symlink case are not handled by one total portable-path and containment gate.
5. `case_id` accepts traversal and path syntax even though the shared renderer uses it as a filename;
   the probe wrote a PNG and JSON beside the requested output directory.

The Review Card and narrow chat contain the complete ledger. I changed no candidate source or test.
Claude must integrate or contest all five items in one response and provide the mechanical delta for
Round 2.

## The idea that matters: green tests do not prove an unconstructed refusal state

This review is a useful example of why the project keeps an independent exact-state gate. The 2,479
tests establish a broad regression baseline, but a test suite proves only the states it constructs.
Here, shallow immutability passed because no test tried to mutate a nested mapping; the path checks
passed because the suite used ordinary POSIX-like traversal forms; and numeric rejection passed
because `1e9999` becomes infinity during JSON parsing while a huge integer fails later during explicit
conversion.

The remedy is not a larger undirected test count. It is to derive adversarial probes from each claimed
boundary: mutate every mapping-bearing value object, move an authenticated file, cross each parser and
conversion seam, exercise platform-specific path aliases, and observe the actual filesystem after a
write. Python's own documentation notes that a frozen dataclass emulates immutability through generated
attribute methods; it does not recursively freeze nested objects
([Python dataclasses](https://docs.python.org/3/library/dataclasses.html#frozen-instances)). Likewise,
path normalization and resolution need an explicit containment policy rather than a string-only
traversal check ([Python pathlib](https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve);
[OWASP path traversal](https://owasp.org/www-community/attacks/Path_Traversal)).

## What is working

- The synthetic four-case fixture and runbook are closed, deterministic and visibly non-scientific.
- The Step-4a design is jointly approved at one exact blob and gives the implementation a narrow,
  inspectable authority boundary.
- Review Cards are producing complete ledgers and bounded delta responses instead of repeated whole-file
  rediscovery.
- The first-half implementation refuses before a scientific open and has a strong 212-test focused
  baseline.
- The packet-wide suite is currently clean at 2,479 passing tests.
- Independent mutation, path and integration probes found reachable failures that the owner suite missed.

## What is not working or remains open

- Step 4b-i is blocked on the five Round-1 findings; neither candidate blob is approved.
- Step 4b-ii has not started and is not authorized while the first-half review remains open.
- No production connection record, selected checkpoint set, final configuration, capacity choice,
  probability threshold or abstention threshold exists.
- No pilot, validation or test result has been read for those decisions.
- The Claim Sheet director review in `director_requests.md` remains open but non-blocking.
- The packet still carries 67 ignored checkpoints without a final distribution/recovery decision.

## Verification artifact

The checked-in fixture now provides four deterministic, 300-DPI examples of the final inspection
shape: paired robot views, causal call timing, confidence and unknown state, tracking traces, onset and
analysis windows, and exact provenance. Its value is operational. It proves that the display contract,
shared painter, interactive selection and scripted export can agree.

It does not prove a scientific effect. Its records are fabricated, its warnings are part of the image,
and the real-role path remains fail-closed. A future real bundle must come only after the current
connection contract is approved, the rest of the adapter is separately reviewed, and later configuration
and scientific gates are explicitly authorized.

## What happens next

1. Claude integrates or contests the complete five-item Step-4b-i ledger and identifies all changed and
   mechanically byte-identical regions.
2. Codex performs the Round-2 delta review on the returned exact blobs and either approves them or records
   only newly introduced blockers.
3. Only after Step 4b-i closes may Claude open the separately reviewed Step-4b-ii source-read and bundle
   construction candidate.
4. Production record creation, real-role reads, capacity/threshold selection, final configuration and any
   scientific run remain later independent gates.

The important state is that the project has an honest synthetic surface and an approved design for its
future data boundary. The first executable half is close enough to test seriously, but it is not safe
enough to approve yet.

-- Codex
