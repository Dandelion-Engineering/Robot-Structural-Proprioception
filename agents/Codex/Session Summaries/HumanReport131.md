# Human Report — Codex Session 131

**Current date and time:** 2026-08-13 21:27 PDT

---

## Summary

This session reviewed Claude's Slot-8 Step-4 connection-record design at exact owner blob
`d9ad21696902b413556c1cb29bcc5da7a373e849`. The design had material authentication,
provenance, geometry and authorization defects, so I repaired the document and explicitly
approved reviewer blob `8d06792cdaa38e9e3df374f9ec1dca109ededc19` / raw SHA-256
`c21eabff703432a791bbb3ab76b0c43ef30ad334d790289900271fcaafdf960e`.

Because Codex edited the owner state, Step 4a remains open until Claude re-reviews and explicitly
approves those same bytes. No adapter implementation is authorized yet. Steps 4c–4f and every
production connection record, real-role read, capacity/threshold/config-freeze decision and
C1-versus-S statement remain blocked.

The central review correction is that the current base manifest does contain 472 complete C1/S
pairs. What is absent is the downstream estimator/controller role material and an approved
established-result artifact selecting the cases and run identities. The current contract fixture
also cannot validate real reconstruction geometry: its deformation coordinates and endpoint are
generated independently and disagree by millimetres under the plausible forward map.

The public Live-Run README was reviewed and deliberately left unchanged. Its dated 2026-08-13
entry remains historical, its current Phase-2/In-Progress banner is accurate, and a successor just
for Step-3 peer-review closure would duplicate the already logged verification-surface event.

---

## Startup and authenticated handoff

- The automation memory was read before project work.
- `.agent-turn` named `Codex`; `.agent-session.lock` was absent, so I created it and re-read the
  turn file. It still named `Codex`.
- I read `AgentPrompt.md`, Project Details, Codex continuity, the relevant Claude–Codex summaries,
  the complete new Phase-2 transcript suffix, Claude's Session-131 report and the review-cycle,
  reproducibility-packet and Live-Run README playbooks.
- Startup state was clean at `HEAD == origin/main == 93e8f7a` (`Claude Session 131`).
- The active transcript was 2,244,241 bytes at SHA-256
  `625167d1101e6a4ffd4dbc2b44f59638446d98f9999926914572310100a61d45` before my append.
- Claude's design handoff authenticated at owner blob `d9ad2169...`, raw SHA-256
  `9992ec14b9fae01e289acf22f99d62a22b4342a2c69c354fea8ffaa1908f92a6`.

---

## Material findings and repairs

### 1. Approval was conflated with runtime authorization

The owner draft said exact-state record approval was authorization, but later said record review
authorized nothing and required two transcript halves for one invocation. The repaired design
separates:

1. design approval, which may license only the synthetic adapter/test build after same-state
   approval;
2. record exact-state review, which establishes an eligible record but authorizes no run; and
3. two separately recorded executable-authorization halves, which authorize one exact adapter
   invocation.

### 2. P6's absent-world claim was false

The delivered manifest has 944 rows and 472 complete pairs:

```text
dev     152 C1/S pairs
pilot   152 C1/S pairs
val     168 C1/S pairs
total   472 C1/S pairs
```

P1–P5 are currently false. P6 is uninstantiated because no established-result artifact selects
the surface's cases and run identities and the required estimator/controller roles are pending.
The design and B1 tests now state that distinction.

### 3. The current fixture cannot set adapter geometry

`build_data_contract_fixture.py` uses a synthetic plant whose `deform_coords` and
`true_task_output` come from independent maps. A read-only reconstruction probe missed the
fixture endpoint by 2.81–6.20 mm (mean 5.31 mm), not floating-point noise. The existing 1 nm
constant is a fixture construction check and cannot be reused as a real adapter tolerance.

The repair assigns the existing fixture only to authenticated storage/refusal plumbing and
requires a dedicated coherent synthetic adapter fixture whose joint angles, deformation,
centerline and tip share one dependency-light forward map. No real-data tolerance is guessed in
Step 4b; a later reviewed geometry-validation artifact must source it.

### 4. Authentication order and file identity were incomplete

The owner order parsed role indexes before hashing them. It also did not identify the packet
schema, established result, model-selection source, separate threshold sources or geometry
validation source completely.

The repaired record now names and hashes the packet schema, config, established result,
model-selection artifact, both threshold sources, geometry producer and validation artifact,
manifest, both dataset audits, every role index/payload and checkpoint. Each object is hashed
before it is parsed or loaded. Root domains are explicit: packet-relative artifacts,
role-root-relative payloads and checkpoint-root-relative checkpoints.

### 5. P4 gained the stronger established-result binding

The record now names the exact already-established result artifact, digest and field paths. The
adapter checks split, config, case and run identity equality before opening role payloads. This
binds the surface to a result established elsewhere, but does not claim to prove the social review
gate. Transcript closure still records that gate, and the later two-half authorization separately
licenses the adapter's own scientific-byte re-open.

### 6. Geometry and provenance were made concrete

There is no static MJCF file in the packet; `cable_mechanics.model_xml` constructs it in memory.
The record therefore hashes the producer source without importing MuJoCo and states the body
order, segment lengths, planar convention and exact deformation-coordinate triplets. The first
body of each link is excluded from `deform_coords`, matching the source.

Schema-conformant fixture bytes cannot become research provenance merely by receiving a digest.
The repaired design requires strict semantic agreement among `generation_audit.json`,
`independent_audit.json`, the manifest, config and established result. The development output path
is mechanically fixed and ignored only to prevent accidental tracking; `.gitignore` is explicitly
not treated as access control.

### 7. Synthetic tests no longer overclaim production coverage

The synthetic acceptance path reaches only a private `SYNTHETIC_FIXTURE` assembly/validation seam.
It cannot create production `DEVELOPMENT_ONLY` or `FINAL` authority. B2 and B7 now distinguish the
layers Step 4b can exercise from the exact production-record controls that must run at Step 4d.

The new additive geometry refusal is `X_GEOMETRY_UNSUPPORTED`, exit 15. The existing success is 0
and twelve refusals occupy 3–14, so no existing code moves.

---

## E1–E4 and public-log rulings

- **E1:** Build after 4a closes, using the existing fixture for storage/refusal plumbing and a
  dedicated coherent fixture for geometry. Neither may acquire production authority.
- **E2:** Use the stronger exact established-result artifact/digest/field binding while retaining
  separate transcript closure and read authorization.
- **E3:** Retain `DEVELOPMENT_ONLY` for a future explicitly reviewed development record. The current
  accept path is `SYNTHETIC_FIXTURE`, not development.
- **E4:** D3 remains open. No cross-arm derived scalar is added by this design.
- **Public log:** no successor entry. The dated log is historical, the banner is current, and
  Step-3 review closure does not warrant duplicating the already logged surface milestone.

---

## Independent evidence

The delivered source state re-measured as:

```text
generation_audit.json SHA-256   7db736e3508a4c8550b47b816ae448f17ee3b7193c8727c26a49dca6a9a211d7
independent_audit.json SHA-256  40c37551e01a39379366837878e658b1927b7edf3427c342f6878c45768357ad
manifest.csv SHA-256            55ea5f0e74ddd24b05eafc51a2b9fc424eda99eac1901534946f42b6012ebe12
manifest rows / complete pairs  944 / 472
draft config                     draft; blocked; models/calibration/evaluation null
reviewer design audit            DESIGN_REVIEW_OK: 36 checks
git diff --check                 pass
```

Because this was a document-only repair, I did not rerun the packet suite. Claude's current
Session-131 checkout evidence is 2,267 passed, 0 failed, 0 collection errors in 204.35 seconds.
No code or test byte changed in this Codex session.

I opened only source, contract, manifest and audit metadata needed for the review. I opened no
role index, role payload, checkpoint or pilot/validation/test scientific result, stepped no
rollout, ran no fit, rendered no figure and wrote no production result. The counters remain
278 rollouts, 67 fits, 67 checkpoints and zero pilot/val/test reads.

---

## Transcript append integrity

The complete pre-write transcript state was authenticated at 2,244,241 bytes / SHA-256
`625167d1101e6a4ffd4dbc2b44f59638446d98f9999926914572310100a61d45`. I verified a complete
unique EOF anchor before appending.

Post-write checks established:

- the complete pre-write bytes remain the exact prefix at the same SHA-256;
- the Codex Session-131 header occurs exactly once;
- Codex is physically last;
- Git shows one tail hunk at `+109/-0`;
- the added 7,103 bytes are LF-only;
- the full transcript is 2,251,344 bytes at SHA-256
  `29e3207bb9869028db2119d3eae547fe94aa78258b59f0a7dd5b1b4a590d751f`.

No append-order recurrence occurred, so no Transcript Order Monitoring entry was needed.

---

## Files created or updated

- `Reproducibility Packet/protocol/slot8-connection-record-v0.1.md` — reviewer-repaired and Codex
  approved exact design state.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — additions-only review, rulings and exact owner handback.
- `agents/Codex/Session Summaries/HumanReport131.md` — this report.
- `agents/Codex/README.md` — current-purpose state and report index.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 132.

No production code, test, result, runbook, public README, `.gitattributes` or `.gitignore` file was
changed.

---

## Next step

Claude must review exact design blob `8d06792cdaa38e9e3df374f9ec1dca109ededc19`. If Claude
explicitly approves those same bytes, Step 4a closes and only the bounded synthetic adapter/test
build in 4b becomes eligible. If Claude edits, it must hand the next exact state back. Steps 4c–4f
remain blocked.
