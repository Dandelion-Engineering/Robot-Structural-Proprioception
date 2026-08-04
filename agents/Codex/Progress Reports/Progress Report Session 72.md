# Progress Report — Codex, Session 72

**Date:** 2026-08-04
**Covers:** my Sessions 65–72 (previous report: Session 64)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

My last report ended with the payload-measurement program built but awaiting its first
review. The purpose of that program is modest and important: measure how the robot arm's
structural-damage signal changes across seven tip payloads, without letting the result be
mistaken for confirmatory evidence.

The program then went through eight alternating review rounds. Those rounds found real
ways an expensive run could fail to leave a usable record, even while its ordinary tests
were green. The last round changed no working behavior; it pinned the final disclosed
URL/path policy so a later edit cannot silently reopen the same privacy failure.

Both agents now approve the program. It has run only in its zero-rollout planning mode.
That produced a 5,386-byte plan fixing all 126 intended measurements, the one ordinary-
path verification replay, the order, the early-stop costs, and the decision rules before
the first new measurement exists. Claude and I have each independently read and approved
that exact document.

**Where the project stands now:** the design, executable, and official plan are agreed.
The measurement itself has not started. A separate two-agent authorization is still
required before even the one replay rollout may run. The lifetime Protocol-P-related
total remains **151 rollouts**.

## Why so much review went into one program

The simulation and its record are different things. A simulation can run correctly, but
the project still loses if the program crashes before writing the result, writes a result
that cannot be audited, or records private machine paths that make the public artifact
non-portable.

The eight rounds concentrated on those failure paths. Early review found that the replay
gate selected the wrong retained row, and some terminal branches could spend simulation
and then fail before preserving any evidence. Later rounds found a subtler conflict: the
rule “always write what happened” met the rule “never publish an absolute machine path,”
and the path guard could destroy the very failure record it was meant to protect.

The team tested those paths adversarially rather than trusting a green happy path. One
method was **mutation testing**—deliberately weakening a guard and checking whether a test
fails. It is a way to test the tests, not only the program. A concise overview is
[available here](https://en.wikipedia.org/wiki/Mutation_testing).

The result is not that the program is perfect. It is that the measured failure classes
now have explicit contracts: malformed plans still leave refusal artifacts; terminal
paths retain gate evidence, counts, and elapsed time; persisted JSON refuses machine-
specific absolute paths; and the final named URL-scheme policy cannot change without a
test failing.

## What changed across Sessions 65–71

The first rounds repaired execution defects. Missing authorization inputs and replay
failures could return without a valid artifact. A foreign plan whose `inputs` member had
the wrong type could raise while constructing the refusal document. Absolute paths could
appear not only as values but as JSON member names. Deeply nested or canonically
unwritable foreign JSON could break the failure writer itself. Each of those states is
now covered.

The next rounds widened the privacy audit beyond familiar path spellings. Windows paths
can use one-character drive prefixes, mixed slashes, spaces, or appear inside prose; URLs
can resemble network paths. A broad pattern would protect privacy by mangling ordinary
text, so the final behavior uses a bounded named-scheme rule and discloses what it does
not preserve. The last review pinned that rule from both sides: named schemes survive at
valid token boundaries, and a listed name used only as a suffix of a longer scheme does
not receive protection.

That last distinction matters because a future edit can look harmless—“also protect this
scheme”—while changing whether a complete network-like machine path is published. The
tests now fail on that change rather than silently adopting it.

## What the official plan fixes before data exists

The plan contains the seven masses from 0.025 to 0.200 kg, ten structural severities per
mass, and eight shared random identities. Reusing the same random identities across
masses is a form of **common random numbers**: the random part is held fixed so the body
mass is the intended moving factor. This is a standard variance-reduction method
([overview](https://en.wikipedia.org/wiki/Variance_reduction)).

It also records 126 distinct physical keys. That count matters because the identities are
shared deliberately: identity alone cannot distinguish a 25-gram body from a 200-gram
body. Payload mass is part of the key, so every planned physical body remains distinct.

Both agents independently rebuilt that key inventory and obtained the same SHA-256
fingerprint. SHA-256 is a cryptographic digest standardized by NIST; here it identifies
the exact planned document rather than proving the scientific result
([NIST Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)).

The plan also fixes an anchor before the unmeasured masses run. The new instrument must
reproduce nine stable verdicts from the earlier 50-gram screen. The tenth verdict is
deliberately unconstrained because its original margin was only 2.1% of threshold;
requiring a new identity to reproduce that sign would be requiring it to reproduce a
near-boundary noise realization. If the stable anchor fails, the extension stops and no
payload conclusion is licensed.

## What is working

- The frozen payload-extension document, generator seam, mass-aware result key, and
  executable all have same-state approval from both agents.
- The official plan is canonical, committed, and approved by both agents at digest
  `15298da4...030be3`.
- The plan's 126 physical keys, 532 logical references, costs, identities, anchor rows,
  and protocol/source hashes re-derive independently.
- The focused suite passes 170 tests normally and under optimized Python; the full packet
  passes 1,306 tests and compiles cleanly.
- No payload-extension rollout, confirmatory identity, or final configuration exists.

## What is not working or remains unknown

- The six reserved non-anchor payload masses remain unmeasured. The project still does
  not know how the structural-damage boundary changes across them.
- The physical mechanism behind the measured attenuation remains unidentified. The model
  has no gravity, and the low-frequency probe is far below the relevant elastic modes, so
  neither static sag nor a simple resonance explanation is available.
- The selected earlier screen left no development structural severity above its operative
  threshold. That non-transfer boundary remains the reason Amendment A2 is necessary.
- The program review consumed eight rounds. The early rounds protected real rollout
  evidence; the last rounds were increasingly about disclosure and test coverage. The
  project had no deadline, so the extra hardening was affordable, but it was still time
  spent on instrument integrity rather than new science.
- `director_requests.md` still contains the non-blocking Phase-1 Claim Sheet review. No
  new director action is required for the current technical gate.

**Verification artifact:** no change. The official plan is useful audit infrastructure,
but it is not the Claim Sheet's hands-on result demonstration. That remains downstream of
the measurements and later confirmatory work.

## What happens next

1. Both agents issue one separate Step-4 authorization naming the approved plan digest
   and explicitly authorizing exactly one ordinary-path replay rollout.
2. Only then may the extension execute once in its frozen order. A complete path costs at
   most 127 rollouts and was estimated at roughly 53–58 minutes of simulation, plus model
   compilation; the result file, not a console pipe, is the authority.
3. Both agents independently read the persisted result before it informs Amendment A2.
4. The later amendment decides what payload/severity boundary the project may carry into
   configuration freeze. The development extension does not make that decision itself.

The important state is simple: the project discovered that its first measured boundary
depended on payload, refused to assume the missing curve, and has now fixed the follow-up
measurement before spending it. The next step is authorization, not interpretation.

— Codex
