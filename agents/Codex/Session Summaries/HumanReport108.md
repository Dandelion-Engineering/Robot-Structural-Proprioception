# Codex — Human Report, Session 108

**Date and time:** 2026-08-10 10:12 PDT

**Phase:** Phase 2 — Execution, with limited Phase-3 packet assembly

**Progress-report session:** No. The next regular Codex progress report is Session 112 unless a phase transition or approved Claim Sheet amendment fires one sooner.

---

## Summary

Claude Session 108 found no open packet-rule review and created a new zero-resource measurement
note, `agents/Claude/Stage-1 Instrument Precision.md`. The note asks how precisely the completed
five-seed Stage-1 development design can resolve a paired mean, and what several hypothetical
seed/width extensions would cost. It deliberately reads only the two tracked Stage-1 JSON
records and proposes no Stage 2.

I genuinely reviewed the note under the review-cycle playbook and independently recomputed its
statistics. The dispersion extraction is correct and useful, but the exact handed-off state was
not approvable. It called a central-*t* planning approximation an exact 80%-power minimum
detectable difference, treated pointwise paired-mean precision as though it were curve-shape
resolution, generalized five observed pairing ratios into a claim that coupling could not be
strengthened and seeds were the only variance lever, and overcounted one candidate design by ten
fits.

I corrected all four issues directly in the note and explicitly approved the reviewer-edited
state at Git blob `e27a51ae17e09ecb9706bf1bb85a5bbde56a6418`. Claude owner re-review remains
open. Stage 1 remains complete as scoped; the note licenses no trend statement, capacity,
threshold, Stage 2, later-role read, fit or final configuration.

## What was accomplished

### 1. Reconstructed the Stage-1 dispersion arithmetic

Using only the five persisted `pairs` records at each width, I independently reproduced:

```text
widths                         16 / 24 / 32 / 40 / 48
paired sample SDs              0.109761 / 0.163331 / 0.149636 / 0.191773 / 0.155432
pooled RMS paired SD           0.156237889748
SD reproduction error         < 1e-12 at every point
variance-identity error        < 1e-15 at every point
```

The two original self-checks are appropriate arithmetic checks of the dispersion extraction:
the recomputed paired SD matches the C7 artifact and the correlated-difference variance identity
holds. They do not test the later power calculation, so that required a separate drive.

### 2. Corrected the MDD definition and values

Claude's handoff defined MDD as the smallest difference detected by a two-sided paired *t*-test
at 80% power, but calculated it as:

```text
(t_0.975,df + t_0.80,df) * sd / sqrt(n)
```

That is a common central-*t* planning approximation, not the exact two-sided noncentral-*t*
power solution. At `n = 5` it achieves 79.13% power. I replaced it with a numerical solution of
the exact noncentral-*t* equation and updated every affected value:

```text
width     exact MDD at n=5     seeds reaching MDD <= 0.05
16        0.184617             40
24        0.274722             86
32        0.251687             73
40        0.322562            118
48        0.261437             78

pooled    0.262792             79
```

The integer seed thresholds do not change. The corrected note now names `scipy.stats.t` and
`scipy.stats.nct` as the review-time calculation path instead of claiming that no statistical
library is in the critical path.

### 3. Repaired the pointwise-versus-shape boundary

The original §4.1 said that adding widths 64 / 96 / 128 at five seeds would leave the design's
resolution exactly unchanged and spend fits on an axis that does not move the limiting
quantity. That conclusion does not follow from pointwise MDD:

- new widths have unknown dispersion, so the pooled Stage-1 SD cannot be assigned to them as a
  fact; and
- adding positions on an axis can add information about slope, transition, plateau or
  non-monotonic shape even when the sample size at each point stays at five.

The reviewer edit now separates these quantities. A width-only extension would not deepen the
replication at any one point. More seeds directly improve pointwise paired-mean precision under
an unchanged-design/constant-dispersion assumption. Neither fact chooses between a width
extension, a seed extension, a replacement instrument or no further work. Curve-shape power
would require its own predeclared analysis, which this note does not retrofit.

### 4. Narrowed the pairing claim

The persisted ratios `sd_unpair / sd_pair` are correctly recomputed as:

```text
0.996 / 0.919 / 1.043 / 0.838 / 0.787
```

They show no observed material pairing benefit in this five-seed sample. They do not establish
that pairing cannot be strengthened or that seed count is the only possible variance lever.
The edited note preserves the observed variance statement and removes the universal inference.

### 5. Corrected the combined-design cost row

The original candidate table priced eight widths at twenty seeds as 280 new fits. The correct
count is:

```text
five existing widths:  5 * 2 suites * (20 - 5) new seeds = 150
three new widths:       3 * 2 suites * 20 seeds           = 120
total                                                       270
```

At the persisted average of 439.594 seconds / 42 fits = 10.4665 seconds per fit, this is 2,826
seconds / 0.79 hours. The note now reports the corrected row.

## Exact review state

```text
original handoff                         BLOCKED / SUPERSEDED IN REVIEW
  Git blob                               4dd8cfc8564e73d53562884240eb52109859845d
  raw SHA-256                            f8e00df3b16ba5639a2a9f7430f1c8df6ab8756cec12c68d240ef2794e711102

reviewer-edited note                     CODEX APPROVED / CLAUDE RE-REVIEW OPEN
  Git blob                               e27a51ae17e09ecb9706bf1bb85a5bbde56a6418
  raw SHA-256                            c3540c6ebbd6508fa74b7e48c524a0e5128cc60fa46bf19c5d939c7296f64708
  size / encoding                        18,011 B / UTF-8 / LF / final newline
```

Claude's initial chat handoff did not explicitly approve the state. More importantly, the
reviewer edit creates a new state. Claude must genuinely reopen the note and explicitly approve
the reviewer blob or return a new state; no owner approval is inferred from authorship,
handoff, silence or this review.

## Verification

The independent review probe, run with the project virtual environment, passed these checks:

```text
source records                            two tracked Stage-1 JSON files only
paired SD reproduction                    5/5 within 1e-12
correlated variance identity              5/5 within 1e-15
pooled RMS SD                             0.156237889748
exact noncentral-t power                  0.800000 at every solved MDD
per-width n@0.05                          40 / 86 / 73 / 118 / 78
pooled n@0.05                             79
chi-square SD interval                    0.119531 to 0.225618
Bartlett statistic / p                    1.106118 / 0.893300
runtime record                            42 fits / 439.594 s
combined candidate count                  270 new fits
git diff --check before closeout          clean
```

One first exact-power loop used an overly wide noncentrality bracket that triggered a SciPy
`NaN` at an irrelevant extreme. I narrowed the bracket to the region containing the 80%-power
root, reran the calculation, and then asserted achieved power exactly at every reported MDD.
This was a probe issue, not a project-data or note defect. A convenience PowerShell hash command
also initially used a .NET `HashData` method unavailable on this host; the compatible
`SHA256.Create().ComputeHash(...)` path produced the recorded transcript digest.

## Transcript integrity

The Session-108 review append used the verified physical UTF-8 EOF and passed the complete hard
gate:

```text
pre-write bytes / physical lines          1,864,771 / 30,109
pre-write SHA-256                         e4487f53...bbea0a49
verified EOF anchor                       multi-line / unique / physical tail
Codex header                              unique at line 30,111
old prefix                                byte-identical
transcript diff                           +81 / -0
last recognized agent header              Codex Session 108
```

No Transcript Order Monitoring note or forward correction was needed.

## Decisions and reasoning

1. **Block the original exact state.** Its statistical label and Stage-2 implication were
   decision-bearing overclaims, not cosmetic wording.
2. **Edit rather than comment only.** The review-cycle playbook permits direct reviewer edits,
   and every correction is narrow, measured and independently verifiable.
3. **Approve the reviewer-edited state.** The corrected note now measures pointwise precision
   without pretending to price curve-shape information or choose a next design.
4. **Keep owner re-review open.** Claude has not approved the new bytes.
5. **Do not update the public Live-Run README.** An internal measurement note still in active
   review is not a phase close, finished public artifact, scientific milestone or result.
6. **Do not propose Stage 2.** The note is decision input only; the protocol keeps any Stage-2
   design and authorization separate.

## Resource and evidence boundary

No fit, checkpoint write, simulator generation, physical rollout, C7 invocation, plan
publication, or pilot/validation/test read occurred. No manifest, `.npz`, label payload or
checkpoint was opened. Lifetime Protocol-P-related physical rollouts remain 278. The one-shot
C7 authorization remains spent. The final `Reproducibility Packet/config/config.json` remains
absent.

## Files created or updated

- `agents/Claude/Stage-1 Instrument Precision.md` — corrected statistical definition, values,
  pointwise-versus-shape boundary, pairing scope and candidate-fit arithmetic; reviewer-approved,
  owner re-review open.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the four findings, independent drive, exact-state approval and owner gate.
- `agents/Codex/Session Summaries/HumanReport108.md` — this report.
- `agents/Codex/README.md` — updated current authority, shared-file status, report index and tree.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the open owner re-review.

Not changed: packet scripts, tests, protocols, plans, results, checkpoints, packet README,
either `.gitignore`, either `.gitattributes`, Claim Sheet, director requests, final config or
public Live-Run README.

## Next steps

1. Claude should genuinely re-review exact note blob `e27a51ae...` and explicitly approve it or
   return a new state.
2. Preserve the distinction between pointwise paired-mean precision and curve-shape power.
3. Treat pooled SD `0.156237889748` and the 79-seed estimate as planning inputs with the stated
   47–162 uncertainty interval, not as a specification.
4. Do not infer or propose Stage 2, capacity selection, threshold selection, later-role reads or
   final configuration from the note.
5. The next Codex session number is 109. The next regular progress report is Session 112.
