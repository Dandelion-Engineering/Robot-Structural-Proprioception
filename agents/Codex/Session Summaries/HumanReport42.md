# Human Report — Codex Session 42

**Current date and time:** 2026-07-29 17:23 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state reviewer of Claude's corrected Protocol P v2.3.2
artifact and owner of the permanent-test placement decision for I13b.

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)

**Decision:**

```text
BLOCK_PROTOCOL_P_V2_3_2_PENDING_STAGE0_IDENTITY_PAYLOAD_BINDING
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

**Rollouts spent:** zero. No Protocol-P identity was generated, no Protocol-P
statistic was computed, no dataset-role artifact was written, and the test split
remains untouched at zero identities and zero payloads.

## Summary

Claude Session 42 accepted and independently verified all four of Codex Session
41's findings, renamed the tracked artifact from v2.3.1 to v2.3.2 so each
version name denotes one byte-state, and handed back this exact owner-approved
file:

```text
Reproducibility Packet/protocol/protocol-p-v2.3.2.md
canonical SHA-256:
  9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5
raw SHA-256:
  9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5
bytes:
  50,169
encoding/EOL:
  UTF-8, no BOM, pure LF
```

Codex read the complete 936-line file, reviewed its delta from v2.3.1, checked
Claude's Session-42 report and commit, traced the relevant implementation
sources, reproduced all text and binary hash measurements, and ran the packet
test suite.

The four Session-41 findings are corrected:

1. tracked text and retained binary artifacts now use separate hash domains;
2. `M2` no longer has an operative role, `T1` is retired, and the terminal
   cases name the authoritative rule directly;
3. replay, Stage-A/B/C, and Stage-0 provenance now have distinct scopes and
   strict canonical JSON; and
4. I13 is correctly divided between a complete per-rollout construction
   invariant and a separate plant-behaviour test.

The implementation-review order is also correct: same-state protocol approval,
then Claude applies the seam, then Codex reviews the exact working-tree diff and
focused tests, then replay, then the stages.

The exact file is still blocked on one new identifier mismatch in Correction 6.
The Stage-0 identity object is defined as `stage_0_identity_payload`, but the
next expression hashes `payload`. Following the standalone specification
literally therefore either raises on an undefined name or hashes a different,
generic payload from the earlier per-rollout discussion. The Stage-0 artifact
identity is not unambiguously bound to the object the file declares.

The correction is one token-level binding:

```text
canonical_json(stage_0_identity_payload)
```

and the written artifact must record that exact same canonical string. Because
Claude adopted one-byte-state-per-version naming and the transcript now binds
v2.3.2 to the digest above, Codex asked Claude to apply the same versioning rule
to the replacement, explicitly approve it, and return the exact digest. Codex
will restrict the next review to that binding and consequential
version/digest references unless the diff expands.

## Cross-review performed

Codex read Claude's `HumanReport42.md`, the complete Session-42 transcript turn,
the full v2.3.2 artifact, and the exact `Claude Session 42` commit delta. The
report accurately separates protocol executability from scientific evidence:
no Protocol-P screen ran, no amendment was approved, no config was frozen, and
no research result was created.

Claude's commit touched the renamed protocol, its public Live-Run entry, the
active transcript append, and Claude's own README/report/continuity files. The
active transcript append was a clean **+187 / -0**, with Claude's Session-42
header at line 8,454. There was no transcript-order recurrence, so the
director-visible monitoring chat required no update.

## Findings verified as corrected

### 1. Text and binary hash domains are now separated

The protocol now assigns exactly two tracked text files to
`canonical_text_sha256` and exactly two retained `.npz` references to
`raw_file_sha256`.

Codex independently reproduced:

```text
protocol v2.3.2
  bytes                         50,169
  BOM                               no
  CRLF pairs                         0
  raw/canonical sha256          9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5

assignment JSON
  bytes                         22,760
  BOM                               no
  CRLF pairs                         0
  raw/canonical sha256          76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae

plant replay reference
  bytes                      3,176,122
  embedded CRLF pairs              18
  raw sha256                  ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45
  text-folded sha256          638e384f3a75c4cefb360e7b7815e7a1b9f5dcd2e01c2cbb718410db9964c575

S-observation replay reference
  bytes                        929,068
  embedded CRLF pairs               1
  raw sha256                  cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
  text-folded sha256          0051ea132a783264c47a370184f0d328e2ae4c3a95ad227b3cf9c181c599435e
```

The values in Section 7 are the raw binary hashes. Section 7 and I1 now say so
directly. The replay input check is exact binary identity; replay output
reproduction is array equality over the retained record fields and payload
entries.

Both tracked text files are also covered by `text eol=lf` attributes, which is
defence in depth rather than the operative portability mechanism.

### 2. Verdict-bearing shorthand is gone

The terms block defines `EI`, `remEI`, `D(v,c)`, `Q95_c`,
`Q95_c^gauge`, OOD, and CRN. `T1` and `M2` are named only as retired
historical tokens. The Stage-0 and gauge-only objects are explicitly
descriptive and carry no threshold or verdict authority.

Cases A, B, and C and `UNSAFE_LADDER_VALUE` now use the direct rule:

```text
D(v,c) >= 2*Q95_c
```

They also define “safe” and “valid” in terms of the terminal exclusion and
I9-I11 computability gates. No terminal branch depends on the retired
abbreviation.

### 3. Provenance scopes are explicit

The file now separates:

```text
replay:
  overrides=None
  base config hash
  ephemeral
  no screen artifact

Stage A/B/C:
  active overrides
  per-rollout base-distinct dev-<64 lowercase hex>

Stage 0:
  no plant or reservation
  one artifact-level dev-<64 lowercase hex>
  exact canonical identity string stored with the JSON artifact
```

This matches the current source fact that `config_hash` is persisted in the
observation payload: replacing the replay's base hash with a protocol-derived
hash would itself break the retained comparison.

The canonical JSON rule now matches
`scripts/utils/config_contract.py`: sorted keys, compact separators,
UTF-8 text, `ensure_ascii=False`, and `allow_nan=False`.

### 4. Runtime construction and plant behaviour are distinct

I13a now checks the requested condition against the complete constructed
physical-fault tuple before every plant-bearing rollout:

- unknown conditions raise;
- healthy requires absent severity and `physical_faults == ()`; and
- structural requires exactly one `FaultSpec` with every field equal,
  including the derived onset.

I13b now specifies a direct `CablePlant` test for the step-499/step-500
softening boundary. Codex verified the architectural reason for the split:
`_generate_reservation` returns the realized pair id, a completed
`PrivilegedRecord`, observations, label payload, safety count, and contact
count. It does not return the plant or its `_softened` history.

Codex answered Claude's placement question: **I13b belongs permanently under
`Reproducibility Packet/tests/`**. The activation boundary is a plant contract,
not a screen-local statistic, and future consumers should retain the
regression guard after Protocol P concludes.

## Blocking finding — Stage-0 identity hashes the wrong name

Correction 6 writes:

```text
stage_0_identity_payload = {
  "stage": "0",
  ...
}
```

but then computes:

```text
stage_0_identity =
    "dev-" + sha256(canonical_json(payload).encode("utf-8")).hexdigest()
```

There is no local definition binding `payload` to
`stage_0_identity_payload`. The previous use of `payload` is the generic
per-rollout object in Correction 2, which has fields that Stage 0 explicitly
lacks. The file declares itself the complete operative state and executable by
a reader without the transcript, so this cannot be treated as harmless
shorthand.

The consequences are fail-loud or, worse, silently wrong:

- a direct implementation raises `NameError`; or
- an implementation reuses a generic `payload` variable and computes a valid
  digest over the wrong identity object.

The protocol also requires the Stage-0 artifact to persist the canonical
string from which its identity was computed. Correcting the variable name in
the digest expression and recording the same rendered string closes both
routes.

This is a new source-checkable defect, not a repeated dispute over the
scientific design. No director escalation is warranted.

## Important decisions

1. **Block v2.3.2's exact digest on the one Stage-0 binding defect.**
2. **Preserve all four corrected Session-41 findings as accepted.**
3. **Keep the scientific, selection, null, branch, and role-coverage design
   approved in substance.**
4. **Require one-byte-state-per-version continuity.** Do not silently change
   the digest already attached to v2.3.2 in the transcript.
5. **Make I13b a permanent packet regression test.**
6. **Keep Claude as seam implementer and Codex as exact-diff reviewer.**
7. **Do not authorize the seam patch until the replacement protocol reaches
   same-state approval.**
8. **Do not update the public README.** Claude already logged the substantive
   Session-42 executability correction. This new token-level internal block is
   not a research result, approved amendment, phase transition, or separate
   public milestone.
9. **Do not update `.gitignore`.** Existing rules already cover the local data,
   test caches, virtual environment, and generated noise observed this session.
10. **Do not issue a progress report.** The next regular Codex report remains
    Session 48, and no event-triggered phase transition or approved amendment
    occurred.

## Verification

```text
protocol exact state:
  bytes                              50,169
  CRLF pairs                              0
  canonical/raw SHA-256             9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5
  expected owner digest match       yes

assignment exact state:
  bytes                              22,760
  canonical/raw SHA-256             76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae
  git text/eol attributes           set / lf

binary replay references:
  raw hashes match protocol         yes
  folded hashes differ              yes
  embedded CRLF pairs               18 / 1

source:
  config canonical JSON rejects NaN yes
  _generate_reservation return      no CablePlant / no _softened history
  structural onset rule             step index >= onset

packet suite:
  command                            .\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
  result                             399 passed in 9.78 s

config.json present:
  false

test identities/payloads:
  0 / 0

Protocol-P rollouts:
  0
```

## Append-only transcript verification

The active Phase-2 transcript was appended using the physical-EOF hard gate:

```text
pre-write lines                    8,637
pre-write bytes                  686,362
pre-write SHA-256                0d6d3b97e88f256b1f6945a6303b512bad26cad79662cefb349c7bbe63c58808
EOF anchor occurrences                 1
post-write lines                   8,744
Session-42 Codex header line       8,639
Session-42 Codex header count          1
old 686,362-byte prefix            exact
technical diff                    +107 / -0
physical last author               Codex
```

The apparent one-line gap before the new header is the deliberate blank
separator after Claude's signature. The prior byte prefix is unchanged through
Claude's final newline. No monitoring-thread entry was needed.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2
  Integration and Config Freeze - Active.md` — appended the exact v2.3.2
  decision, independent verification, single blocker, and I13b location
  approval.
- `agents/Codex/Session Summaries/HumanReport42.md` — this report.
- `agents/Codex/README.md` — updated navigation and current protocol state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  for the replacement-protocol review.

No Reproducibility Packet source, protocol, config, schema, assignment, result,
or test file was changed by Codex. The public README and `.gitignore` required
no change.

## Next steps

Claude owns one narrow replacement-protocol correction:

1. hash `stage_0_identity_payload`, not `payload`;
2. preserve the requirement that the artifact records the exact canonical
   string used for that digest;
3. carry the change forward under the established one-byte-state-per-version
   rule;
4. explicitly approve the replacement exact state and provide its canonical
   digest; and
5. make no seam/source change yet.

Codex then re-reviews that exact binding and any consequential
version/digest references. If the delta stays narrow and is correct, same-state
protocol approval closes.

Only after protocol approval may Claude apply the generator seam and permanent
I13b test, then post the exact working-tree diff and focused test results for
Codex's separate implementation review. Nothing runs before that review
closes. The one-row replay is next; only a passing replay authorizes Stage 0,
then Stage A/B/C.

The written Amendment A2, replacement assignment, from-zero dataset
regeneration, remaining Gate-4-to-Gate-7 work, final `config.json`, and all
confirmatory execution remain unauthorized.
