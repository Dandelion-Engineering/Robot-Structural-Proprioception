# Claude — Human Report, Session 72

**Date and time:** 2026-08-04 08:21 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **151**.

---

## Summary

Codex closed the Step-2 executable review loop in its Session 71 by explicitly approving
the exact blobs I had approved in my Session 71 handoff. Both agents therefore approve the
same bytes, and the eight-round loop is closed. That approval authorized exactly one
thing under §13 of the frozen extension document: **Step 3 — run the executable in plan
mode only, producing the zero-rollout plan artifact, which both agents then read.**

I ran it. It produced `plan.json`, `plan_valid=true`, at zero rollouts. I then read the
artifact the way a stranger who does not trust the program would read it: I re-derived its
load-bearing numbers from the artifact's own published fields using code that does not
import the executable, and I checked the properties that make a digest usable as the
subject of a Step-4 authorization. Everything re-derived. I approved the artifact in the
Phase-2 transcript and handed the second independent read to Codex, explicitly declining
to write anything that could be read as half of the Step-4 authorization.

Session 72 is also a **regular progress-report session** (my sessions 8/16/24/…), so I
wrote `Progress Report Session 72.md` covering S65–S72 in addition to the normal work.

## What ran, and what "zero rollouts" means

```text
..\venv\Scripts\python.exe scripts\run_payload_boundary_extension.py --mode plan
  plan_valid=true  rollouts=0  rc=0

Reproducibility Packet/results/payload_boundary_extension/plan.json
  canonical sha256  15298da4c7a903bf4b62a79eb384abe1f53182972dff41c6e1387dc0ce030be3
  git blob          04f2bccd53629d6b54895be20224a680a78325c7      5,386 bytes
```

Plan mode compiles **eight MuJoCo models** — one nominal body plus the seven payload
bodies of the mechanics preflight — and steps none of them. I did not assert that; I
measured it. Three consecutive plan runs took **0.38 / 0.36 / 0.37 s**, against a
measured 25.1–27.5 s for a single rollout. Nothing that stepped a plant fits in that
envelope. The ledger stays at 151.

## What I verified independently rather than taking from the tool

The point of a plan artifact is that Step 4's authorization names its digest, so it has to
survive being read by someone who does not trust the program that wrote it.

**The physical-keys digest re-derives from the plan's own description of itself.** I built
all 126 key reports from nothing but `plan.masses`, `plan.ladder`, `plan.identities` and
`inputs.probe_*`, using `physical_key_report` from the closed seam file plus a two-stage
sort-and-hash recipe written for the probe alone:

```text
reports built 126   distinct 126   published count 126
re-derived  9889afa648a0ed71d8b59f1e5bca658954d82f99ad46bf3324e870451ca02385
published   9889afa648a0ed71d8b59f1e5bca658954d82f99ad46bf3324e870451ca02385   MATCH
```

**Census, anchor and identities, all re-derived from the artifact:**

```text
XA 18 + XM-C 48 + XM-B 60 = 126 = extension_physical_rollouts
126 + 1 replay = 127 = total_physical_rollouts = maximum_cost
(8 healthy + 10 ladder) x 7 masses = 126;  (10 + 10 + 56) x 7 = 532 = logical_references
every exit-cost literal (0/0/1/9/19/67/127) equals §12's table
anchor: |margin|/threshold >= 0.10 reproduces the NINE constrained rungs and {0.50};
        the stability interval re-derives as (0.0211, 0.1962) against §9.3's (0.021, 0.196);
        all ten verdicts equal the sign of their own published margin
identities: sensor_seed == 160000 + 1000k + 2 for all eight; membership sums to 126, 77 on k=0
```

**X7, with a matcher this project did not write.** All 285 strings in the document —
object member names included — scanned with a regex written for the probe alone:
**0 offenders, zero backslashes in the file.** `config_path` is project-relative.

**The digest identifies the document, not the copy.** Three runs — committed, a rerun into
a scratch output dir, and a run from a full copy of the packet at a different absolute
path — produced **byte-identical** 5,386-byte files with the same SHA-256.

**Limitation 80 does not bite this artifact, and I checked why rather than assuming.**
`plan.json` is canonical JSON with `separators=(",", ":")`, so it contains **zero newline
bytes of either kind**; there is nothing for an eol filter to convert. I staged it and read
the index blob back: 5,386 bytes, byte-identical to the worktree, `LF 0 CR 0`. Its raw and
canonical digests are the same number in every checkout — unlike
`payload_conditioning.json`. The authorization should still name the **canonical** digest,
because `require_authorized_plan` computes the digest from the parsed document.

## The §11.1 walk, and two additive fields I flagged rather than let pass

Lesson 75 says walk the specification's headings and name what discharges each. All 19
`inputs` fields are present and are exactly those 19; both `protocol` digests recomputed
from the files themselves (`5689dad7…8bdf421f`, `538ae06b…8df33b6a`, raw == canonical for
both) and match the frozen pins; `plan_valid`, `terminal`, `mode`, `authority`, all six
`preflight` members, and all eight `plan.*` members are present.

Two fields appear that §11.1's list does not name. I flagged both so nobody later reads the
artifact as literally §11.1 and concludes it drifted:

1. `preflight.per_mass_realized_delta[]` — named by **§11.2**, not §11.1, and required
   anyway because execute mode reads it off the recomputed plan.
2. `plan.shape_audit` — named nowhere in the document, and it is the field that
   **discharges X9 in the plan artifact** (occurrences 126, distinct physical keys 126,
   distinct identities 8, class counts 77/7×7). Nothing else in §11.1 distinguishes
   occurrences from identities. It should stay.

**The mechanics preflight is a real check and the artifact is self-auditing on it.** It
compiles a body per mass and measures `sum(body_mass) − nominal` at `atol=1e-12`. The
published values are the measurements, not the declarations — 0.05 realizes as
`0.05000000000000002`, |Δ| ≈ 2.1e-17 — so a reader can apply the tolerance themselves. It
proves the override reaches the **compiled body** and says nothing about whether the
payload reaches the **measured signal**; with no gravity in the plant those are genuinely
different claims, and **X8 remains the sole liveness check**.

## One documentation observation, deliberately not escalated

§12's TIME block ends *"the plan artifact must carry the executor's own count."* A plan
artifact spends zero rollouts and has no executor; §11.1 names no timing field; and §11.2
— which explicitly says plan-mode exits are governed by §11.1 — is where the substance
lands, in `timing{…}` and `physical_ledger[].elapsed_s`, enforced by X6. Read plainly the
word "plan" is a slip for "result". **I did not propose a version bump**: the document is
frozen, a bump costs a `git mv` plus both approvals, and nothing operative depends on the
sentence. I recorded it in the transcript so the next reader walking §12 against the
artifact does not think a field went missing, and told Codex its version wins if it reads
it differently.

## Verification

```text
plan mode        plan_valid=true  rollouts=0  rc=0   0.36-0.38 s over three runs
focused          170 passed in 9.79 s
FULL PACKET    1,306 passed in 122.77 s
determinism      3 runs / 2 packet roots -> byte-identical, one SHA-256
independent probe 126/126 keys, digest MATCH, census MATCH, anchor MATCH, X7 0 offenders
index blob       04f2bccd...  5,386 B  identical to worktree  LF 0 CR 0
config/config.json still absent; every hash still dev-; nothing entered confirmatory analysis
```

**One retired check, stated because a silent retirement is worse.** Both agents have been
reporting *"results/payload_boundary_extension absent"* as a verification line for eight
rounds. Nothing committed was enforcing it — it was review discipline. The full suite is
green now that the directory exists, and that line retires here.

## Transcript handling and the monitoring duty

My Phase-2 turn was appended by a script asserting five gates before leaving the file in
place: the 1,218,243-byte pre-write prefix recovered byte-identically with its SHA-256
(`c2c077b1…`) asserted **inside** the writer, the header occurring exactly once, the header
after the recorded boundary, Claude physically last, and a `+N/−0` git diff. Result:
**+172/−0**, header unique at line 18,853, file now 19,023 lines.

Monitoring duty, verified at the git level rather than by reading: Codex's Session-71
append was **+63/−0** in commit `5250aa4`, its header unique and correctly ordered after
mine. No recurrence — **streak forty-two**. Nothing added to the monitoring chat, since the
duty is to flag recurrences.

## Live-Run README

The heartbeat check fired this session for the first time in eight of mine. Codex logged
the executable-review milestone earlier today; I appended one lean entry for the plan
artifact, which is the first thing the payload-boundary extension has actually produced
and closes the loop Codex's own entry opened for a reader ("the next permitted step is a
zero-simulation plan document"). Banner untouched — already 2026-08-04. `+2/−0`.

## Files created or updated

- `Reproducibility Packet/results/payload_boundary_extension/plan.json` **(new — the Step-3 artifact)**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` (+172/−0)
- `README.md` (+2/−0)
- `agents/Claude/Progress Reports/Progress Report Session 72.md` **(new — regular cadence, covers S65–S72)**
- `agents/Claude/Session Summaries/HumanReport72.md` (this file)
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

## Next steps

1. **Codex reads `plan.json` independently and says whether it approves it.** §13 Step 3
   requires both agents; one read does not discharge it.
2. If it approves, **a separate, explicit joint Step-4 authorization** naming
   `15298da4…030be3` and explicitly authorizing the §3.3 replay gate's one rollout.
   Neither agent may issue it alone.
3. **Step 5 execution:** 127 rollouts in the X0E/XR/XA/XM-C/XL/XM-B/XZ order, 53–58
   minutes, run as a background job, polling the results JSON rather than a pipe.
4. **Amendment A2 remains undrafted and blocked** — correctly, on the measurement it
   currently has to assume. Config materialization and all confirmatory work stay
   downstream and blocked.
