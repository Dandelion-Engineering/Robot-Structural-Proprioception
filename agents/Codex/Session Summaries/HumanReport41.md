# Human Report — Codex Session 41

**Current date and time:** 2026-07-29 16:42 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state reviewer of Claude's tracked Protocol P v2.3.1
artifact and owner-choice response for the proposed generator seam.

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)

**Decision:**

```text
BLOCK_PROTOCOL_P_V2_3_1_PENDING_BINARY_HASH_DOMAIN_AND_COMPLETE_EXECUTION_PINS
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

**Rollouts spent:** zero. No Protocol-P identity was generated and no
Protocol-P statistic was computed.

## Summary

Claude Session 41 verified both of Codex Session 40's source contradictions,
measured the silent consequence of the step-0 onset defect, and moved Protocol
P from a transcript-only description into a tracked 593-line artifact:

```text
Reproducibility Packet/protocol/protocol-p-v2.3.1.md
canonical SHA-256:
  8c268f8f5777923e661cb44c0b6d68991bdf41bf5080ea3e229e4c101d401d76
bytes:
  29,250
line endings:
  LF
```

Claude explicitly approved that exact digest and asked Codex to review the file
as the object an independent reader would execute. Codex verified the digest,
the new `.gitattributes` rules, the assignment canonical digest, the committed
generator paths, both retained replay references, and the current packet tests.

The three Session-41 corrections are substantively right:

- structural faults now carry the declared trajectory onset and healthy uses
  the empty physical-fault tuple;
- active override provenance is intended to be full-length,
  lifecycle-valid, base-distinct, and bound to a complete protocol artifact;
  and
- the protocol and assignment text identities are portable across CRLF/LF
  checkouts.

The exact tracked file is still blocked on four narrow
file-to-execution contradictions.

The first is immediately fatal. The protocol correctly defines a text
canonicalizer that strips a UTF-8 BOM and folds CRLF to LF for the protocol
Markdown and assignment JSON. It then instructs the replay gate to pass two
binary `.npz` references through the same helper. Both binary files contain
CRLF-valued byte pairs inside their payloads. Text folding changes both
digests, so the replay gate would fail deterministically before Stage A.

The other three gaps are narrower but still decision-bearing:

1. `M2` is not defined in the standalone file and inherits two incompatible
   meanings from the transcript: a descriptive fixed-trace gauge-only
   measurement and the operative Stage-C `D(v,c) >= 2*Q95_c` verdict.
2. The provenance scope says every rollout carries the protocol-derived
   development hash, while the exact all-None replay must carry the base config
   hash to reproduce the retained row; Stage 0 writes a JSON artifact but has no
   rollout/reservation and no pinned artifact-level provenance construction.
3. I13 combines a runtime construction invariant with a behavioural plant test,
   while checking only onset rather than the full condition-to-`FaultSpec`
   equality. The helper treats any misspelled non-healthy condition as a
   structural fault and silently ignores severity on the healthy branch.

Codex appended the exact block and correction list at the verified physical end
of the active Phase-2 transcript. The scientific/selection design remains
approved in substance; no candidate, statistic, threshold, stage, branch,
role-coverage rule, OOD boundary, or success bar needs redesign.

## Finding 1 — text normalization corrupts the binary replay identity

The protocol's helper is:

```python
def canonical_file_sha256(path):
    raw = Path(path).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
```

That operation is valid only on canonicalized UTF-8 text. Section 7 applies it
to the retained NumPy ZIP payloads. Codex tested both exact files:

```text
plant reference
  bytes                         3,176,122
  embedded CRLF byte pairs             18
  raw sha256                   ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45
  text-folded sha256           638e384f3a75c4cefb360e7b7815e7a1b9f5dcd2e01c2cbb718410db9964c575

S observation reference
  bytes                           929,068
  embedded CRLF byte pairs              1
  raw sha256                   cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
  text-folded sha256           0051ea132a783264c47a370184f0d328e2ae4c3a95ad227b3cf9c181c599435e
```

The values pinned in the artifact are the raw hashes. An implementation that
follows the operative text therefore rejects both correct retained files.

The required correction separates the hash domains:

```text
canonical_text_sha256:
  protocol-p-v2.3.1.md
  proposed-gate3-assignment-v0.1.json
  UTF-8 BOM strip plus CRLF-to-LF fold

raw_file_sha256:
  retained plant .npz
  retained S-observation .npz
  exact hashlib.sha256(path.read_bytes())
  no byte transformation
```

I1 must likewise distinguish canonical text bytes from exact binary bytes.
The `.gitattributes` additions remain useful defence in depth for the tracked
text files and have no role in the ignored binary references.

## Finding 2 — `M2` is history-dependent and semantically overloaded

The standalone artifact uses `M2` in three ways:

```text
M2 is Stage 0's first real-plant corroboration
all ten have safe valid M2 verdicts
the same narrowing applies to M2
```

In the transcript, “Measurement 2” was the descriptive fixed-trace
gauge-only check. Earlier protocol drafts used `M2` for the operative
stratification rule. Those objects have opposite authority: the gauge-only
quantity is a zero-authority secondary, while the full Stage-C healthy null is
the verdict.

The correction should remove the abbreviation and use direct names:

```text
prior fixed-trace gauge-only check
safe, valid Stage-C per-cell mechanics verdicts
operative D(v,c) >= 2*Q95_c rule
```

This does not change the approved statistic. It prevents a reader from using
the descriptive `Q95_c^gauge` in place of the full `Q95_c`.

## Finding 3 — provenance needs three explicit scopes

The artifact currently says every rollout stamps protocol-derived provenance.
That cannot include the exact replay:

```text
replay gate:
  overrides=None
  base config hash
  ephemeral
  no screen artifact persisted

Stage A/B/C:
  active overrides
  per-rollout base-distinct dev-<64 lowercase hex>

Stage 0:
  no plant, rollout, cell, condition, or reservation
  writes sensor_only_difference_null.json
  needs one artifact-level dev-<64 lowercase hex> identity
```

The replay must retain the base hash or it cannot be byte-identical to the
approved reference. Stage 0 cannot use the per-rollout payload without
inventing a fake reservation. Its artifact-level payload must instead bind the
base config, both assignment identities, protocol-spec digest, `stage="0"`,
and the exact canonical CLI inputs/output schema.

The correction also needs the repository's strict JSON convention:
`allow_nan=False`. Plain `json.dumps` defaults permit non-standard `NaN`
tokens in an identity object.

## Finding 4 — I13 must assert the whole construction

The new helper says:

```python
if condition == "healthy":
    return ()
return (FaultSpec(... severity=float(severity) ...),)
```

It does not reject unknown conditions, and the healthy branch ignores a
present severity. I13 checks onset but not that the complete object matches the
condition. The exact runtime invariant must require:

```text
healthy:
  severity absent
  physical_faults == ()

structural value v:
  exactly one FaultSpec
  source_class == structure
  subtype == link_stiffness_loss
  location == 1
  severity == float(v)
  onset_index == derived trajectory onset
  compound_flag == false
  ood_flag == false
```

Unknown conditions raise. This full-object check executes before every
plant-bearing rollout and is the construction precondition for describing a
Stage-A failure as a physical limit.

The separate statement that the softened model is inactive before step 500 and
active at or after it belongs in a focused implementation test.
`_generate_reservation` returns a completed `PrivilegedRecord`; it does not
return the plant's historical `_softened` state. The production loop can check
the constructed `FaultSpec`, while the branch-specific test verifies
`CablePlant` behaviour at steps 499 and 500. The physical-limit interpretation
requires both.

## Challenges and how they were handled

### Avoiding a false approval because the owner supplied a matching digest

The owner correctly supplied an exact artifact identity, and Codex verified it.
That proves which state is under review; it does not prove the instructions
inside that state are executable. Codex followed the replay instruction against
the actual binary references rather than accepting the named raw hashes as
self-consistent.

The result is a particularly sharp example of why hash domain matters: the
canonicalizer is correct, both pinned raw hashes are correct, and the combined
instruction is still guaranteed to fail because one was applied outside its
domain.

### Distinguishing a new defect from re-litigation

Codex Session 40 approved the candidate/null/branch design in substance.
Session 41 did not reopen any of those decisions. The new findings arise only
because the full operative file now places previously separate text fragments
next to one another:

- text canonicalization next to binary replay hashing;
- `M2`'s historical meanings next to the standalone verdict table;
- per-rollout provenance next to a no-rollout Stage 0 artifact; and
- a runtime-invariant heading next to a behavioural test statement.

These are new source-checkable contradictions, not a repeated scientific
disagreement. No director escalation is warranted.

### Preserving implementation ownership

Claude asked whether Codex wanted to own the generator seam. Codex kept
Claude's default implementation ownership because Claude already has a verified
prototype and branch-specific scratch tests. After the protocol file reaches
same-state approval, Claude should apply that prototype and post the exact
working-tree diff plus focused tests for Codex's separate review before any
replay or protocol stage runs.

The artifact's sentence saying the diff is posted before the patch is applied
must change to the agreed order:

```text
protocol approval
-> apply seam
-> post exact implementation diff for review
-> implementation approval
-> replay gate
-> Stage 0/A/B/C
```

## Important decisions

1. **Block the exact v2.3.1 digest while preserving the scientific design.**
2. **Use separate text and binary hash helpers.** Never normalize a binary
   payload before checking an exact replay digest.
3. **Remove `M2` from the standalone artifact.** Direct names are safer than a
   transcript-dependent abbreviation.
4. **Separate replay, plant-bearing, and Stage-0 provenance.**
5. **Require strict canonical JSON with `allow_nan=False`.**
6. **Strengthen I13 from onset-only to full condition/`FaultSpec` equality.**
7. **Separate the runtime construction check from the focused plant-behaviour
   test.**
8. **Keep Claude as seam implementer and Codex as implementation reviewer.**
9. **Do not change the public README.** This is an internal exact-state block,
   not a scientific result, phase transition, approved amendment, or public
   milestone.
10. **Do not escalate to the director.** No contested judgment remains.

## Reasoning paths explored

- Verified whether the `.npz` files merely happened not to contain CRLF-valued
  binary bytes. They contain 18 and 1 respectively, so the failure is actual,
  not theoretical.
- Compared raw and folded hashes rather than inferring the outcome from file
  type.
- Checked whether `M2` could be recovered unambiguously from the artifact
  itself. It cannot; the file uses the name before defining it and inherits two
  historical meanings.
- Checked whether Stage 0 could use the per-rollout provenance payload. It has
  no cell, condition, overrides, or reservation, so forcing that schema would
  fabricate identity fields.
- Checked whether the all-None replay could use the protocol-derived hash. It
  cannot while preserving byte equality, because the retained observation
  records carry the base config hash.
- Traced I13 through the helper, `FaultSpec`, `CablePlant`, and
  `_generate_reservation` return type. The runtime can inspect the exact
  constructed object, but a completed record cannot reveal the plant's
  historical `_softened` transitions.
- Checked the repository tests for plant onset behaviour. A generic
  step-boundary test exists; Protocol P still needs the branch-specific
  step-499/500 and helper-construction tests Claude proposed.

## Insights gained

1. **Canonicalization is type-specific.** A safe text transform is silent
   binary corruption when applied to a ZIP/NumPy payload.
2. **A digest can authenticate a contradictory instruction perfectly.** Hashes
   establish identity, not correctness.
3. **A standalone specification must retire history-dependent abbreviations.**
   If a symbol requires the transcript to disambiguate it, the spec is not
   standalone.
4. **Provenance needs a scope model.** A replay, a plant-bearing override, and a
   no-plant synthetic artifact are three different identity objects.
5. **Recording an actual and expected value is not the same as checking their
   equality.** Provenance can preserve a condition/severity mismatch while the
   runtime still computes a clean answer for the wrong body.
6. **Behavioural tests and runtime invariants are complementary.** The runtime
   checks the object supplied; the test proves the downstream implementation
   interprets that object at the intended boundary.

## Verification

```text
protocol artifact:
  bytes                              29,250
  CRLF pairs                              0
  canonical SHA-256                 8c268f8f5777923e661cb44c0b6d68991bdf41bf5080ea3e229e4c101d401d76
  expected owner digest match       yes

assignment artifact:
  canonical SHA-256                 76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae
  .gitattributes text/eol           set / lf

binary replay references:
  plant raw/folded hashes equal      no
  observation raw/folded equal       no
  current pinned values are raw      yes

packet suite:
  399 passed in 10.05 s

config.json present:
  false

transcript append:
  pre-write lines                    8,235
  pre-write bytes                    667,359
  pre-write SHA-256                  5C459A638429C30318907DD4E58D3263A36296E223B8D720AAB72660D7F59A3E
  post-write lines                   8,450
  Session-41 header line/count       8,239 / 1
  old byte prefix                    exact
  technical diff                     +215 / -0
  physical last author               Codex
```

No monitoring-thread update was needed because the append was clean.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the exact-state v2.3.1 block, four correction pins, and seam
  ownership response.
- `agents/Codex/Session Summaries/HumanReport41.md` — this report.
- `agents/Codex/README.md` — updated navigation and current active-state
  description.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  for the next session.

No Reproducibility Packet source, protocol, config, schema, assignment, result,
or test file was changed. The public README and `.gitignore` required no update.

## Next steps

Claude owns one narrow correction to the same protocol artifact:

1. restrict canonical text hashing to the protocol and assignment;
2. hash replay `.npz` references as exact raw bytes;
3. remove or fully replace every ambiguous `M2` occurrence;
4. define replay, Stage-A/B/C, and Stage-0 provenance separately;
5. use strict canonical JSON;
6. make I13 a full runtime condition/`FaultSpec` equality check plus a separate
   branch-specific plant-behaviour test;
7. correct the implementation-review order sentence; and
8. explicitly approve the new canonical digest.

Codex then re-reviews only that exact delta plus the retained v2.3.1 state.
After same-state protocol approval, Claude may apply the verified seam and post
the exact diff/tests for separate implementation review. Only after
implementation approval may the one-row replay run. Stage 0/A/B/C remain
unauthorized until that replay passes.

The final `config.json`, written Amendment A2, Claim Sheet edits, replacement
assignment, regeneration, Gate-4 fitting, and all confirmatory material remain
unauthorized.

The next regular Codex progress report remains due at Session 48 unless an
approved amendment or phase transition triggers an earlier report.
