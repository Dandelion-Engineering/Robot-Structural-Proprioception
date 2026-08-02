# Human Report 61 — Claude

**Date and time (session close):** 2026-08-02 12:58 PDT

**Phase:** Phase 2 — Execution. All Phase-1 gates in force; Schema v1.0 + Amendment A1 in force. Config deliberately unfrozen; `config.json` absent.

**Rollouts spent this session:** zero. No MuJoCo simulation of any kind was run.

---

## Summary

Two pieces of work, both of which the previous session's ruling asked for.

1. **I re-reviewed Codex's corrections to my payload-conditioning read** — properly, not as a formality. Both of its findings are real and I reproduced them with instruments that share no code with the file under review. Then I ran the mutation sweep over Codex's own repair, which found a check in Codex's new code that could be deleted entirely without a single test noticing, and a duplicated refusal message across *three* functions that no text search of the file could have found.
2. **I drafted the payload-boundary extension** Codex ruled must exist before Amendment A2 can be written: a separately versioned, development-only pre-registration covering all six unmeasured payload masses plus a seventh as a control, with a fixed ladder, exact counts, a private identity band, twelve fail-loud invariants, and a five-step authorization sequence that this document explicitly does not take.

The state of the review: I approve the result artifact and both READMEs at the exact states Codex approved. I have edited the analyzer and its tests and handed them back, so that loop is open on the new state and Codex owns the next turn on it.

**Nothing was executed. No rollout is authorized by anything in this session.**

---

## 1. The owner re-review — Codex was right twice, and its repair still needed the sweep

Codex blocked my original payload-conditioning state on two defects and corrected them directly. The review cycle then requires me to actually re-open the artifact and judge both the diagnosis and the implementation, rather than waving through an edit that arrives with the authority of having been right.

### Both findings reproduced independently

I wrote a stdlib-only auditor that imports nothing from the analyzer and re-derives every relation from the screen artifact and the assignment alone.

**Finding 1 — the missing mass.** My original code asked whether a reserved payload lay outside the *range* of masses the screen ran, rather than whether that exact mass had run. The two readings disagree by exactly one mass:

```text
screened masses    [0.000, 0.050] kg
exact-membership   pilot [0.025, 0.075]  val [0.100, 0.125]  test [0.150, 0.200]  -> 6
range-only (mine)  pilot [0.075]         val [0.100, 0.125]  test [0.150, 0.200]  -> 5
```

`0.025 kg` sits numerically between the two masses that ran, and was silently treated as covered. That is precisely the interpolation my own carried limitation forbids: two levels determine a ratio, not a curve, so an interior mass is unmeasured in exactly the sense an exterior one is. I had written that sentence in the same session and then interpolated anyway. Codex's corrected artifact reports all six, and my independent read agrees with it exactly.

**Finding 2 — trusting a duplicated field.** My original code read the screen's stored `margin` without checking that it equalled `d - operative_threshold`, and read `operative_threshold` without checking that it equalled `2 * Q95_c`. A contradictory artifact could therefore have moved the reported boundary while the analyzer stayed green. Codex added those derivations plus five more. I re-derived all of them with exact equality rather than a tolerance, over all forty ladder cells, and found no violation anywhere: thresholds, margins, per-cell verdicts, stored minimum margins, row-level conjunctions, the per-cell null being constant across the ladder, and the Stage-C null object agreeing with the value stored beside each ladder row.

I also re-derived cell→payload from the screen's own recorded rollout provenance joined to the assignment's cell table — not from the artifact under review — and got cells 4/5 at 0.000 kg and cells 6/7 at 0.050 kg, with ratios reproducing at 0.4867 / 0.5055 / 0.5366.

Regeneration is byte-identical to Codex's tracked artifact.

### Then the sweep on the repair, and it found things

Session 59's lesson is that a reviewer's repair is at its most dangerous exactly when the reviewer has just been shown to be right. Session 60's lesson is that the sweep itself had been lying. So I ran the corrected harness over Codex's edited analyzer — 66 guard sites, two full passes required to produce identical verdicts.

```text
FIRST SWEEP   66 cases | 59 caught | 7 SURVIVORS | reproducible: True
```

A survivor is not yet a gap, so I characterised all seven by construction: each state driven through the committed module *and* through a copy with that one guard switched off, each variant written to a uniquely named file so the stale-bytecode mechanism could not apply.

**One of Codex's new guards had a real, silent gap.** The analyzer checks that each ladder cell's `hard_gates_passed` field is a boolean, and then separately checks that it is true. With the type check switched off, a document whose cell carried the **string `"false"`** was *accepted* — because a non-empty string is truthy. An unsafe cell's margin would then have entered the boundary read. The guard is necessary and correct; nothing in the suite could have made it fail. It is now covered by a parametrized test over `"false"`, `"no"`, `1` and `[0]`, and the measured consequence is recorded in a comment at the guard itself.

**And a duplicated refusal message spanning three functions.** Four of the seven survivors were guards of mine that refuse a malformed payload list. Switching any of them off still produced a refusal — with a byte-identical message. The cause is that a third function, `require_binary_context_factors`, builds its message with an f-string over the factor name, so for `payloads` it renders the exact sentence the other two carried as string literals. Three raise sites, one sentence, and searching the file for the literal finds two of them. The consequence is that the two document-level tests which appeared to cover the payload readers had in fact been certifying the binary-factor check all along, and a docstring I wrote last session claiming these messages were distinct was true of one pair of guards and false of this one.

All three sites now name their own read, with direct-call tests for the two the document path never reaches, and a parametrized test that drives the same malformed document through all three functions and requires three distinct sentences — a comparison, not a source search, because a source search demonstrably cannot see this.

```text
FINAL SWEEP   66 cases | 65 caught | 1 SURVIVOR | reproducible: True | blob restored
              the survivor is the arithmetic-unreachable one already on record
focused tests            105 passed in 0.67 s   (was 94)
full packet suite      1,126 passed in 137.87 s (was 1,115)
artifact regeneration   byte-identical
```

### A digest we both quoted turns out to be a rendering

Both agents recorded the payload artifact's SHA-256 as `47ec3571…`. Measured this session with a clean checkout into a scratch tree: a fresh checkout on this machine renders that file with Windows line endings, 8,809 bytes, digest `0beb9afc…` — not the 8,541-byte file we quoted. The same is true of the role-coverage artifact.

`47ec3571…` is correct **as the document digest**, and from now on has to be qualified that way, exactly as the screen result's digest already is. This is the third file in three sessions to hit the same trap, which is why it is now written into the carried limitations rather than re-derived each time. I did **not** touch `.gitattributes`: the ruling against a broad rule stands and I accept it. I flagged for Codex that a narrow pin on these two newer files would push in the opposite direction, and left the decision with it.

---

## 2. The payload-boundary extension

Codex's ruling was: measure first, but not through the shortcut I had sketched, and not as a section bump of Protocol P — which is a closed, executed provenance object. It asked for a separately versioned, development-only pre-registration pinning five things. That document now exists as a draft, at `Reproducibility Packet/protocol/payload-boundary-extension-v0.1.md`.

**What it measures.** The same ten reserved damage severities, at each of the six payload masses nobody has run, plus a seventh mass — 0.050 kg — included purely as a control.

**Why the control is not padding.** The extension's construction deliberately matches one of the executed screen's cells in environment, contact profile, trajectory and probe, differing only in payload mass and identity. That cell's zero-margin crossing is already known to sit between 0.45 and 0.50 remaining stiffness. If the extension is rebuilt correctly, it must land in the same bracket. Without that check, a genuine payload effect and a mis-assembled instrument produce the same output — which is the failure mode this project has already been bitten by once.

**Why a fixed ladder rather than adaptive bracketing.** Codex objected, correctly, that one severity per mass locates nothing. The alternative it offered was a pre-registered bracketing algorithm. I chose the fixed ladder instead, for a reason I put in the document: the ten values *are* the union of the severities all four data splits actually reserve, so the operative question — which reserved severities survive at this mass — is answered exactly, with no sequential stopping rule that could later be accused of having been chosen after seeing a result. If a crossing falls below the most severe rung, "no reserved severity is testable at this mass" is a complete answer for the amendment, and it is pre-registered as such.

**What it costs, counted honestly.**

```text
per mass    18 distinct physical rollouts (10 ladder + 8 healthy, one reused as the
            matched reference) and 76 logical references
total       126 distinct physical rollouts, 532 logical references
            53.8-57.8 minutes of simulation at the measured per-rollout range
```

My Session 60 estimate of 50 rollouts was wrong in both of the ways Codex named — it counted five unmeasured masses instead of six, and it budgeted a design that could not locate a boundary. The document says so in its own cost section rather than leaving the correction to be reconstructed.

**What it commits to in advance.** Four non-terminal outcome cases and four terminal shapes, each with an explicit statement of what it licenses for the amendment's three options. One case — a boundary that moves non-monotonically with mass — licenses **nothing**, and is pre-registered precisely because a direction established over two levels is not a guarantee about seven. Twelve fail-loud invariants carry forward the driver requirements accumulated across previous sessions. A private seed band, verified clear of every other band in the project.

**A prerequisite the document names rather than hides.** The extension cannot be executed against the current codebase at all. The screen's override mechanism has five fields and payload mass is not one of them; mass reaches the plant only through the reservation's catalog entry. The extension needs an additive sixth field on a jointly approved artifact that belongs to Codex — so that is a change requiring both approvals and its own sweep, and the document says so in a numbered prerequisite section instead of presenting the work as ready.

What I did verify, at zero cost: the packet's existing mechanics preflight compiles a plant per declared mass and asserts the realized body-mass change exactly. Run against all eight masses the extension names, every one realizes exactly, in 0.04 seconds. So the mechanism the override must reach works and is checkable before a single rollout is spent; what does not exist is the path to it.

**One number worth the director's attention.** The whole simulated arm weighs 0.1728 kg. The heaviest reserved payload is 0.200 kg — **1.157 times the mass of the entire arm**, hung at the tip. Whether the plant can carry that inside its own safety envelope is an open question, and the document pre-registers a terminal shape for the case where it cannot.

---

## 3. A correction to a figure I had been carrying

While writing the extension's justification for fixing environment and contact, I re-derived the relevant spread from the screen artifact instead of quoting my own summary. My summary said the within-level spread was "0.18%–3.6%, one cell 12.9%". The actual table has twenty values, and *two* of them exceed 3.6%: 12.89% and 6.81%, both at the two mildest damage rungs where the signal is smallest.

The correction does not change the argument — in the region where the boundary actually falls, every value is at or below 3.48% against a payload effect of roughly 2× — but the figure I had been carrying was incomplete, and the extension document states the full table and flags the correction in place.

---

## Challenges, and how they were handled

**The temptation to approve and move on.** Codex had found two real defects, fixed them well, and asked for an explicit approval. The path of least resistance was to give it. Running the sweep over the repair instead is what surfaced the silent gap in Codex's own new code — a check that could have been deleted entirely without one of 1,115 tests noticing.

**A survivor is not a gap.** Seven mutations survived the first sweep. Reporting seven gaps would have been wrong: four were mutually redundant guards, one was arithmetic, and only one was a real silent hole. Distinguishing them required constructing the state each guard exists to refuse and running it through the code twice, once with the guard alive and once with it dead. Two of the seven turned out to be worth code changes; the other five needed characterisation, not repair.

**Mislabelling my own probe.** My first characterisation pass assigned the wrong meaning to two of the survivor line numbers — I inferred which guards they were instead of reading them. The outcome class happened to be right, but the labels were wrong, and I found it only because I went back to print the actual source lines. Recorded because the near-miss is the lesson: an instrument that reports line numbers still requires you to look at the lines.

---

## Files created or updated

```text
CREATED
  Reproducibility Packet/protocol/payload-boundary-extension-v0.1.md
    canonical sha256 32a0393069615e18d1249ec2ac95526eb188092fcccf596be24ce60ac9bea475
    blob 903962f8ba31b887764c13e718fe0f92fde0b7a9 | 26,866 bytes | LF | raw == canonical
    DRAFT — not approved, not executable, zero rollouts authorized
  agents/Claude/Session Summaries/HumanReport61.md   (this file)

EDITED, HANDED BACK TO CODEX FOR APPROVAL
  Reproducibility Packet/scripts/analyze_protocol_p_payload_conditioning.py
    blob 39048d2658963a345e3a46949a6070d421a155d9 | 45,231 bytes
  Reproducibility Packet/tests/test_protocol_p_payload_conditioning.py
    blob b9e81f6320e1a3b68f952d631795f1d82abca5ff | 50,869 bytes | 105 tests

APPENDED
  chats/Claude-Codex/Phase 2 Integration and Config Freeze/... - Active.md   +242 / -0
  README.md  (Live-Run log, one new entry)                                    +2 / -0

APPROVED AT CODEX'S STATE, UNCHANGED BY ME
  Reproducibility Packet/results/protocol_p/payload_conditioning.json  c11f7067…
  Reproducibility Packet/README.md                                     b51196c3…
  README.md (the payload entry Codex approved)                         9d1cae71…

REWRITTEN
  agents/Claude/Summary of Only Necessary Context.md
```

---

## Next steps

1. **Codex owns two open items.** The analyzer and tests at their new blobs, and the extension document at its canonical digest. Both are same-state reviews.
2. **If the extension is approved,** the seam extension and the executable come next, then plan mode only, then a separate explicit execution authorization. Five steps, none inferable from another.
3. **Amendment A2 stays blocked** until the extension has run and both agents have read it. I have not drafted it and will not before then.
4. **Everything downstream stays blocked**: assignment lineage, full regeneration, Gate-4 model work, `config.json`, and any confirmatory materialization.
5. **My next regular progress report is Session 64**, unless a phase transition or an approved written Claim-Sheet amendment fires one sooner. An approved A2 would.
