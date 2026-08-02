# Codex Human Report — Session 60

**Date:** 2026-08-02 10:21 PDT

**Phase:** Phase 2 — Execution

**Decision:** The corrected zero-rollout payload-conditioning state is technically approved and returned for Claude's explicit owner re-review. Measure the payload boundary before drafting Amendment A2, but only under a new development-only pre-registration; no rollout is authorized.

## What happened

Claude Session 60 explicitly approved the four role-coverage/packet blobs returned in Codex Session 59, closing that exact-state loop. Claude also reproduced a stale-bytecode weakness in the mutation audit, corrected the harness to clear `__pycache__` and disable bytecode writes, and re-ran the 28-case role-coverage mutation sweep successfully.

Claude then created a zero-rollout payload-conditioning analyzer, tests, artifact, and packet/root README updates. The artifact correctly showed that the recorded 50 g payload roughly halves the structural signal across the ladder, so payload is a live boundary variable rather than a harmless nuisance. Claude proposed measuring several unscreened masses before Amendment A2.

I reviewed and independently reproduced that state. The public and packet README wording was accurate, but the original analyzer/tests/artifact were blocked on two concrete integrity defects:

1. `unscreened_mass_kg` treated the pilot payload range as a continuous interval, so it incorrectly omitted the exact unmeasured 0.025 kg pilot mass.
2. The analyzer trusted duplicated stored `margin` and verdict fields without proving their arithmetic and logical coherence. A contradictory stored margin could therefore pass through to a derived artifact.

I corrected the analyzer and tests, regenerated the artifact without rollouts, and approved the resulting exact state. The exact unmeasured masses are now pilot `{0.025, 0.075}`, validation `{0.10, 0.125}`, and test `{0.15, 0.20}` kg. The numerical conditioning result itself is unchanged.

## Reviewer-edited exact state

```text
Reproducibility Packet/scripts/analyze_protocol_p_payload_conditioning.py
  Git blob 7f9ed558fe173a7ec859a3335eeb6a5989fb5a3e

Reproducibility Packet/tests/test_protocol_p_payload_conditioning.py
  Git blob 6fc5f158921f67e4eeb24a9d5c4165d0cf0047eb
  focused tests 94

Reproducibility Packet/results/protocol_p/payload_conditioning.json
  Git blob  c11f70673b043ea634481d47ad4137365c0cd12e
  SHA-256  47ec3571bf207f428c1eb376cfdf7b3f673a94729fa649ba845bca27299d97d1

Reproducibility Packet/README.md
  unchanged Git blob b51196c30b909dbf8c89a9704ed2a966d1ae0fa2

README.md
  unchanged Git blob 9d1cae71efb555dbe3242e8f4dbcfe77f23fe9db
```

The analyzer now independently checks the hard-gate boolean, threshold construction, per-cell margins, per-cell verdicts, row verdicts, stored minimum margins, per-cell null consistency across the ladder, and Stage-C-to-ladder null agreement. It compares exact measured payload masses rather than treating the reserved role range as continuously screened.

## Independent checks

I reproduced the mutation-harness failure directly: a same-size, same-whole-second source edit reused the first import through `__pycache__`; clearing the cache and setting `PYTHONDONTWRITEBYTECODE=1` loaded the mutated value and created no new cache. This confirms Claude's harness correction is necessary. Future source-mutation audits must use that isolation, run twice, and return identical verdict sets before their result is used.

I independently derived the payload ratios from the tracked inputs:

```text
minimum ratio   0.4867076148
mean ratio      0.5054909695
maximum ratio   0.5365918313
```

LF- and CRLF-rendered screen inputs produced byte-identical artifacts, and a fresh derivation matched the tracked artifact exactly.

Verification completed:

```text
focused payload-conditioning tests     94 passed in 0.74 s
full packet suite                    1,115 passed in 121.83 s
compileall                              clean
git diff --check                        clean except benign LF/CRLF warnings
fresh artifact derivation               byte-identical
LF vs CRLF derivation                    byte-identical
physical rollouts spent                 0
config/config.json                      absent
```

## A2 ruling

Measure first. The existing executed Protocol P v2.3.3 result remains closed and must not be edited or re-run. Payload-boundary work must use a separate, versioned, development-only pre-registration with a distinct private development identity and seed band.

Claude's proposed 50-rollout sketch is not yet execution-ready. There are six, not five, exact unmeasured reserved-role masses, and one selected structural severity at each mass cannot locate a joint payload/severity boundary. Before any execution decision, the new protocol must pin:

- all six exact masses: 0.025, 0.075, 0.10, 0.125, 0.15, and 0.20 kg;
- development-only construction that does not materialize pilot, validation, or test identities, labels, manifests, or outcome payloads;
- either a predeclared severity ladder or an exact adaptive bracketing procedure with branches and stop rules;
- logical-versus-physical accounting, provenance, replay, persistence, safety, and terminal behavior; and
- a zero-rollout plan review followed by a separate explicit execution authorization.

This is a new development diagnostic, not a correction to the closed Protocol P measurement and not evidence that authorizes Amendment A2 text, assignment lineage, or regeneration.

## Transcript and public state

The active Phase-2 transcript append passed the append-only hard gate. The pre-write 1,030,187 bytes and 15,270 content lines were preserved as a byte-identical prefix, the unique Codex Session-60 header begins after that boundary, and the transcript diff is `+150/-0`.

The root Live-Run README and packet README were left unchanged during this review because Claude's newest entries already accurately state the zero-rollout payload result and development-only boundary. No new public milestone was created by correcting the exact-unmeasured-mass bookkeeping and coherence guards.

## Files changed

- `Reproducibility Packet/scripts/analyze_protocol_p_payload_conditioning.py` — exact measured-mass logic and derived-field coherence guards.
- `Reproducibility Packet/tests/test_protocol_p_payload_conditioning.py` — eight new adversarial guards plus coherent synthetic fixtures.
- `Reproducibility Packet/results/protocol_p/payload_conditioning.json` — zero-rollout regeneration with the corrected exact unmeasured masses.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — append-only Codex Session-60 review and decision.
- `agents/Codex/Session Summaries/HumanReport60.md` — this report.
- `agents/Codex/README.md` — current artifact/review state and report index.
- `agents/Codex/Summary of Only Necessary Context.md` — complete continuity rewrite.

No regular progress report was due; the next regular report remains Session 64 unless an approved amendment or phase transition occurs sooner.

## Next action

Claude should explicitly approve the three reviewer-edited payload-conditioning blobs above if accepted unchanged. After that exact-state loop closes, Claude may draft the separate development-only payload-boundary pre-registration for same-state review. Keep `config.json` absent, do not materialize reserved-role or confirmatory data, and spend no rollout until that protocol is approved and execution is separately authorized.
