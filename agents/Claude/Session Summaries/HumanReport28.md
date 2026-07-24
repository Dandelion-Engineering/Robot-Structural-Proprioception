# Human Report — Claude Session 28

**Date/Time:** 2026-07-23 20:00 PDT
**Phase:** Phase 2 — Execution (Integration and Reproducibility Build)
**Session role:** Genuine cross-review of Codex's Gate-1 / Gate-2-foundation implementation → verdict; monitoring-duty check; one lean public-log entry.
**Final config state:** **UNFROZEN** (`BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION` stands).

---

## One-paragraph summary

Codex's Session 27 (which ran after my Session 27) built the first concrete component of the confirmatory pipeline — a machine-readable schema, a self-hashing draft/frozen configuration authority, and a role-separated storage layer with a leakage-auditing deployable loader — and handed me the exact state for genuine review, asking for an explicit `APPROVE_GATE1_GATE2_FOUNDATION` or `BLOCK`. That review was this session's work. I read every line of all seven implementation files plus the doc updates, **independently recomputed both cryptographic hashes with my own canonicalization** (not Codex's functions), verified the cross-platform line-ending guard is actually effective, ran the validator and the full 347-test suite, and then ran **five of my own adversarial probes** against the safety-critical "frozen config" wall — probes that go beyond Codex's committed tests. Everything held. I approved the exact state, closing the loop; posted my review to the Phase-2 chat as a verified pure-append (`+33/−0`); discharged my standing transcript-order monitoring duty (Codex's S27 appends were clean, `+58/−0`, sixth consecutive clean append, so no monitoring note was needed); and added one lean, honest entry to the public Live-Run README marking the pivot from development-screening to confirmatory-pipeline construction. No configuration was frozen; no confirmatory data or `test` payload was created.

## What was accomplished

### 1. Verified the live git state before trusting continuity (Standing Lesson 5)

My continuity summary was written at the end of *my* Session 27, but the startup snapshot showed HEAD at "Codex Session 24," which conflicted with it. Reading the actual `git log` resolved it: HEAD is really `2eb7b1a Codex Session 27` — the snapshot was stale, and **Codex had run its Session 27 after mine**, producing an unreviewed session and an open review loop I owned. The working tree was clean. This is exactly the check Standing Lesson 5 exists for, and it surfaced the real work of the session.

### 2. Genuine review of the Gate-1 / Gate-2-foundation implementation → **APPROVED**

The review target Codex handed off (exact state, requested I not edit it): `schema/schema.json`, `config/draft-config-v0.1.json`, `scripts/utils/config_contract.py`, `scripts/utils/storage_contract.py`, `scripts/validate_data_contract.py`, `tests/test_data_contract.py`, the packet `README.md` / `utils/__init__.py` doc updates, **plus** a root `.gitattributes` LF rule added during Codex's closeout.

What I did rather than take it on trust:

- **Read every line** of all seven files and both doc updates.
- **Independently recomputed both hashes with my own canonicalization** — `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False)` over the document with the top-level `config_hash` removed, SHA-256, `dev-` prefix — rather than calling Codex's `config_contract` functions, so a bug in that module could not mask a bad artifact. I get `schema_sha256 = 0dae0dd0…942f` and `config_hash = dev-0211f2e7…6180`, exact matches to the recorded artifact values and to Codex's report. The canonicalization *is* the rule the schema declares.
- **Confirmed the cross-platform hash guard is effective, not decorative.** `schema.json` is 15,212 bytes with **no CRLF** on disk, and `git check-attr` resolves `eol: lf` on the **real path including its embedded space**. I inspected the `.gitattributes` bytes directly and confirmed the character between "Reproducibility" and "Packet" is a literal `?` glob wildcard (byte `0x3F`) that matches the space — not a corrupted separator that would silently make the LF-pinning a no-op. This matters because the config binds itself to the schema's exact bytes via `schema_sha256`; if that hash weren't stable across a fresh Linux/Windows checkout, the binding would be meaningless.
- **Ran the validator CLI** → `Config OK: status=draft, config_hash=dev-0211f2e7…, confirmatory=False`.
- **Ran the full packet suite → 347 passed** (Codex's 18 contract tests subsumed). The tests are genuinely adversarial: each mutates one invariant and asserts a specific failure.
- **Ran five independent adversarial probes beyond Codex's suite — all passed:** (1) the *real* tracked draft merely re-flagged as frozen (nulls intact) is refused for "unresolved null" — you cannot freeze the current state; (2) **no forgery by prefix-strip** — the frozen digest of an otherwise-identical document ≠ the draft digest with `dev-` stripped, because `status` is inside the canonical payload, so no one can mint a frozen hash by editing the prefix; (3) a complete frozen config validates only under the reserved name `config.json`; (4) tampering a real sensor float breaks the recorded hash; (5) a wrong `schema_sha256` is refused, proving the schema-byte binding actually gates.
- **Confirmed the honest boundary:** no `config.json` anywhere in the packet, no committed `.npz` payloads, and the packet README's "Current boundary" states plainly that Gate 2 is still incomplete (the live manifest/data builder, the allowlisted supervised label join, the non-observation role writers/evaluators, and the end-to-end generator do not exist yet).

**Verdict: `APPROVE_GATE1_GATE2_FOUNDATION`, exact state, no edits.** The schema faithfully renders v1.0 + Amendment A1 (and Codex's own test pins the JSON to my in-force Python types, so it cannot silently drift); the frozen-config gate is a real wall; and the deployable loader is *structurally* leakage-proof (its constructor takes only `observations/<suite>`, its index header and NPZ key set are exact allowlists, path traversal is blocked by `is_relative_to`, and unavailable channels must be all-NaN and fully masked so a lean suite cannot smuggle a richer suite's channel).

### 3. Two non-blocking forward notes (recorded, not conditions of approval)

1. The `.gitattributes` `?`-wildcard works and I verified it end-to-end; *if* that file is ever touched again, a double-quoted pattern (`"Reproducibility Packet/schema/schema.json" text eol=lf`) is marginally tighter, but it is genuinely fine as-is and not worth a review round-trip.
2. When Codex's Gate-3 draft manifest lands, that is the joint pre-registration checkpoint we agreed in S27: the whole-trajectory / whole-fault-setting → `dev|pilot|val|test` assignment must carry one recorded joint approval before any headline model is fit. Codex's `audit_identity_manifest` already enforces the *structure*; the checkpoint is about approving the specific *assignment*.

### 4. Monitoring duty — clean, no note added

My standing duty (assigned by the director in Session 6) is to flag any chat reply that lands anywhere but the physical end of a transcript. Codex's three Session-27 appends to the Phase-2 transcript were a verified pure append (`git show --numstat` = `+58/−0`), and Codex is physically last. This is the **sixth consecutive clean append**. Per the lean-thread rule (flag only on recurrence), I added no note to `Transcript Order Monitoring`.

### 5. One lean public Live-Run README entry

The long development-screening arc (sessions ~19–26, repeatedly landing on "improves diagnosis, not control") has resolved into building the confirmatory pipeline, and its first component is now built *and* jointly approved — the exact trigger my S27 continuity pre-flagged. Codex had deferred a public entry in S27 because the work was then unreviewed; my approval resolves that. I appended one honest, plain-language entry marking the pivot and the approved first component, with the honesty bound intact ("scaffolding, not a result — the configuration remains unfrozen"). The banner already showed the current date and Phase 2 / In Progress, so no banner change was needed.

## Challenges and how they were handled

- **A stale startup git snapshot** contradicted my continuity. Resolved by reading the live `git log` (Standing Lesson 5), which revealed Codex's post-my-S27 session and the open loop. Without that check I would have missed the session's actual work.
- **Reviewing a hash/config authority is only meaningful if reproduced independently.** Re-running the author's own tests proves the tests pass, not that the artifact is honest. I addressed this by recomputing the hashes with my own canonical serializer and by writing five probes the committed suite does not contain — especially the "no forgery by prefix-strip" property, which is the subtle security guarantee behind the whole draft/frozen split.
- **Deciding whether to advance the public log.** The log is "lean by design" and Codex had chosen restraint. I judged that the screening→confirmatory-build pivot plus a jointly-approved first component clears the "genuinely noteworthy" bar (the log has recorded comparable infrastructure turning points before), and added exactly one entry.

## Important decisions and reasoning

- **Approved the exact state without editing it.** Codex explicitly asked for a clean approve/block to avoid spawning another review round-trip, and I found no defects — only optional cosmetic notes. Editing for a cosmetic nicety would have reopened the loop for no real gain, so I recorded the notes as explicitly non-blocking.
- **Did not start my own lane's build work.** My Gate-4/5 work (the `TemporalAttributionNet` + `RMALatentEncoder` learned rungs and the calibration/abstention/OOD/uncertainty selection) is genuinely blocked on Codex's forthcoming Gate-3 draft manifest. Building models or data ahead of the jointly-approved assignment would violate the pre-registration sequencing I committed to in S27 (splits must be fixed before any headline fit) and would mean building against a data layout that does not exist yet. The disciplined move — and the one the Dandelion working method endorses — was a clean, well-documented handoff, not invented follow-on work.

## Insights gained

- The draft/frozen split's real security rests on `status` being *inside* the canonically-hashed payload. That single design choice is what makes "you cannot forge a frozen hash by stripping the `dev-` prefix off a draft hash" true. It is easy to miss on a read; it is obvious once you probe it.
- The schema-byte binding (`schema_sha256`) and the `.gitattributes` LF pin are a matched pair: the binding is only trustworthy because the pinned bytes are stable across platforms. A reviewer has to check both, or neither is real.
- The foundation enforces its leakage invariants on the **read** side (the loader audits every payload at load time). The matching **write**-side builder that guarantees unavailable channels are written all-NaN is future Gate-2 work — which is consistent with Codex's stated boundary, not a gap in what was claimed.

## Files created or updated

**Updated (committed this session):**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended my Session-28 review turn and `APPROVE_GATE1_GATE2_FOUNDATION` verdict (verified pure append, `+33/−0`).
- `README.md` (root Live-Run README) — one appended running-log entry (pivot to confirmatory-pipeline construction + approved first component).
- `agents/Claude/Session Summaries/HumanReport28.md` — this report (created).
- `agents/Claude/README.md` — workspace guide updated for Session 28.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 29.

**Reviewed (not modified — Codex's owned artifacts):** `Reproducibility Packet/schema/schema.json`, `config/draft-config-v0.1.json`, `scripts/utils/config_contract.py`, `scripts/utils/storage_contract.py`, `scripts/validate_data_contract.py`, `tests/test_data_contract.py`, `.gitattributes`, and the packet `README.md` / `scripts/utils/__init__.py` doc updates.

**Scratchpad (not committed):** `verify_gate1_hashes.py` (independent hash reproduction), `probe_frozen_gate.py` (five adversarial probes on the frozen wall), `append_turn.py` (recreated binary-EOF-append tool), `phase2_turn_s28.md` (my appended turn).

## Next steps / pending actions

- **For Codex (its Session 28):** acknowledge my approval and close the loop on its side; then continue Gate 2 with the live multi-setting manifest/data builder and the allowlisted supervised label join, and prepare the full Gate-3 assignment manifest — **without fitting any headline model until both agents approve the same assignment state.** This is the critical path; my lane is blocked on it.
- **For me (Session 29):** read Codex's latest first. If the Gate-3 draft manifest has landed, converge with Codex on it and record the joint pre-registration approval before anything downstream. Once the manifest and Codex's live data layout exist, begin my lane's Gate-4 build — `TemporalAttributionNet` + `RMALatentEncoder` behind the shared `[W,D]` interface (toolchain verified ready: `torch==2.11.0+cu128` on the RTX 5060 Ti / sm_120) — then Gate-5 calibration/abstention/OOD/uncertainty selected on validation only, including a proper bias-inclusive definition of `severity_uncertainty` (not in-sample training-residual dispersion, which my S24 finding showed understates the true scale by 5.72× for the structural suite).
- **Do not freeze a partial config.** No regular progress report is due until my Session 32 (unless a phase transition or an approved Claim-Sheet amendment triggers one sooner).
