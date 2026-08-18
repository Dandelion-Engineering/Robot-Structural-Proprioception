# Human Report — Claude Session 155

**Current date and time:** 2026-08-18 13:32 PDT (taken from the shell while writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

Codex was right a seventh time. Its Session-154 cross-review found three more holes in the
Slot-8 Step-4b-ii-b build, I re-drove all three at source before changing a line, all three
reproduced exactly as reported, I contested none of them, and my re-drive widened the third
one by two further cases nobody had reported. All three are now discharged. In the same
session I closed **B2, B3 and B5** — three of the five remaining non-row items on this
sub-step.

**The three findings are one sentence, and it is the sharpest form this lane has reached: a
check is bounded by the claim it supports, never by the finding it was written against.**

- Row 21 bound the bundle's *provenance block* completely — because the Session-153 finding
  it was written against was about provenance. The claim it supports is about the whole
  published picture, so every threshold, playback grid, decision, controller series,
  tracking array and centerline arrived unbound. Codex replaced the authenticated
  `abstain_threshold` on every scene from `0.55` to `0.56` and the altered bundle published.
- `_authority_output_root` derived the destination from `connection.bound.packet_root` —
  because the finding it was written against moved `output_root`. Those are two fields of
  the same substitutable value, so moving both together moved the expectation with them, and
  the whole declared set published beneath an unrelated temporary directory.
- `_png_pixels_per_metre` verified chunk *integrity* — because the finding it was written
  against corrupted a chunk. The claim it supports is that a case figure is a PNG saved at
  300 DPI, and a CRC-valid byte string containing only the signature, one `pHYs` chunk and
  `IEND` — no image header, no image data — was accepted as `(11811, 11811)` while a strict
  decoder refused the same bytes outright.

Each repair replaced the object-bounded check with a claim-bounded one. That is why each one
is total rather than one case wider than the report.

Twenty-seven net new tests. The focused pair is **356** (was 329), and 356 again under
optimized Python; the packet-wide suite is **3,014 passed / 0 failed**, and 2,987 + 27 =
3,014 exactly.

No scientific resource was spent: no MuJoCo model built, no rollout stepped, no fit run, no
figure rendered from real data, and no pilot, validation or test payload opened.

---

## What Codex found, measured before any repair

Every measurement below is mine, taken by driving the reported construction myself in a
probe that ran outside the repository, **before** a line of the module changed.

### Finding 1 — the bundle is only provenance-bound

Rows 13 through 20 resolved normally over the three-case coherent menu; every scene's
`Thresholds.abstain_threshold` replaced from the authenticated value to that value plus
`0.01`. Altering all three scenes keeps `validate_bundle`'s cross-scene agreement true, and
every provenance block stays byte-for-byte authentic:

```text
authenticated abstain_threshold  0.55
published abstain_threshold      0.56
outcome                          ACCEPTED
```

### Finding 2 — the packet root and the destination move together

`packet_root` and `output_root` replaced together in one `BoundPaths`, with every
authenticated record, config, source, dataset and role path left pointing into the real
packet tree:

```text
substituted packet_root  <tmp>/other-packet
substituted output_root  <tmp>/other-packet/results/verification_connection_development/adapter-fixture
record path (unmoved)    <harness>/packet/results/verification_connection/records/adapter-fixture/…
outcome                  ACCEPTED — all eight files published beneath the substituted root
```

### Finding 3 — CRC-valid non-images still counted as PNG evidence

Codex reported one case. My re-drive found two more of the same family:

```text
signature + pHYs(11811,11811,metres) + IEND   ->  (11811, 11811)   Pillow: UnidentifiedImageError
signature + IHDR + pHYs + IEND  (no IDAT)     ->  (11811, 11811)   [found by my re-drive]
signature + IHDR + IDAT + pHYs + IEND         ->  (11811, 11811)   [found by my re-drive]
```

The third is the one worth keeping. The PNG format requires `pHYs` to *precede* the image
data precisely because a decoder that has already begun rendering is entitled to ignore it.
**A resolution a decoder may lawfully discard is not the resolution the figure was saved
at.**

---

## The repairs

### Finding 1 — bind the bundle, not only its provenance

Row 21 now re-derives rows 13 through 20 from the connection — `resolve_cases`,
`resolve_geometry`, `resolve_provenance`, `resolve_bundle` — and requires each presented
scene's canonical rendering to equal the derived one.

**The instrument is the canonical rendering, and that is the point.** It is total by
construction, so a field added to `VerificationScene` is bound without anyone remembering to
bind it — the same property the `dataclasses.fields` walk gave the provenance block, one
level up. `test_the_scene_rendering_covers_every_field_of_the_scene_type` is what keeps that
argument true, because it holds only while the encoder covers the type.

**The re-derivation opens nothing, and that is measured rather than asserted.** Rows 13
through 18 are pure functions of payloads row 12 already loaded, and the re-derivation runs
*before* the exclusive create — so `test_row21_opens_nothing_outside_the_tree_it_created`,
which requires every observed open to be inside the created root, is exactly the instrument
that goes red if the claim is false. Its docstring now says so.

**The provenance walk is kept above the new comparison rather than folded into it.** The two
answer different questions and say so with different codes: a bundle assembled under another
connection is an identity disagreement that names the field; a bundle whose content is not
what these sources produce is an incomplete bundle. Deleting either changes what a caller is
told, which is the test lesson 286 sets for overlapping guards. No fifteenth exit code was
added.

### Finding 2 — anchor the packet root to what it contains

New `_require_one_packet_root(connection)` requires the bound record path to *equal*
`<packet-root>/<the one packet-relative location section 3.1 gives a record>`, and requires
the schema, the configuration and every named source artifact to be *inside* that root.
`_authority_output_root` calls it before deriving anything.

Equality for the record because section 3.1 gives it one location and design finding CX is
about a record presented from somewhere else; containment for the rest because their
positions are the record's own to declare. The anchor is the record path specifically
because its bytes are the ones rows 1 and 2 actually digested against the CLI authorization
— **an anchor cannot be a field of the value under suspicion.**

**What it deliberately does not refuse, stated so a later session does not "fix" it:** a
whole packet tree copied and run against the copy leaves every one of these paths under the
copy's root. That is one root, and invariant W8 allows it. What is refused is a root that
claims to govern paths it does not contain.

### Finding 3 — assert image structure, not only chunk integrity

The walk now additionally requires a single `IHDR` first at exactly its fixed 13 bytes, at
least one `IDAT`, an unbroken `IDAT` run, `pHYs` before the image data, and an empty `IEND`.

This is enforced in the walk rather than delegated to a decoder for two reasons: a strict
decoder is a dependency this packet does not declare, and the walk was already visiting
every chunk — the structure was simply the part it was not asserting. The ten tracked
Step-3 figures still pass the stricter walk, which is the accept side a parser made stricter
owes.

---

## B2, B3 and B5 — closed this session

**B5 (determinism, invariant V13).** The whole of rows 1 through 21 runs twice through the
*real* scripted writer, with a fresh installation of the coherent three-case menu each time,
and all eight published files are compared byte for byte. **They are identical, and so is
the bundle digest.** The tree is removed between the two runs because row 21 creates its
destination exclusively and `_authority_output_root` fixes that destination from
authenticated values — a connection has exactly one place to publish. Determinism is two
runs that each start from nothing; invariant W10 is about a second run while the first
publication still stands. They are different claims and this test makes the first one.

**B2 (the accept-side census).** Every refusal test in this file says what one row *rejects*.
None of them says a row *produced* anything, and a chain of rows that all refuse correctly
and establish nothing would satisfy the entire refusal set. B2 is the other half: one pass
through rows 1 to 21 asserting each applicable row's own output. It is deliberately one test
rather than twenty-one, because what it claims is that the rows **compose** — each row's
output is the next row's input on a single run — and twenty-one separate tests would each
re-establish the chain and none of them would claim that. Rows 1 to 12 are asserted through
the value `authenticate_connection` produced rather than re-driven, because re-driving them
here would be a second composition of the read order, which an existing test forbids.

**B3 (one refusal per row).** Measured, and then written down as an artifact property rather
than as this session's private count. A committed test reads the test names out of the module
and requires every row 13 to 21 to carry at least one refusal case. **It is a floor and it
under-counts** — it cannot see a refusal written under another naming convention — which is
the direction a completeness claim has to err in, and the disclosure is in its own docstring.
The counts at this state are 5, 3, 4, 4, 1, 5, 1, 8 and 12 for rows 13 through 21.

---

## Challenges, and how they were handled

**The anchor test caught two of my own fixtures before the suite did.** The parametrized
scene-substitution table needs each altered bundle to still satisfy the surface gate —
otherwise the refusals it drives would be landing on an older guard and would say nothing
about the new one. I wrote that anchor first, and it immediately failed twice: shifting the
playback grid by a whole second pushed the decisions outside the playback extent, and
altering one arm's `task_reference` broke the cross-arm agreement rule. Both were my
fixtures being wrong, not the code, and the anchor is what made the difference visible
instead of silently weakening ten tests.

**Deciding how deep the finding-1 repair should go.** The cheap repair is to compare the
record-derived display facts — the thresholds and the menu label — back to the connection.
That would have answered Codex's exact report and left every payload-derived array unbound,
which is the failure mode of the last four sessions on this lane. The complete repair needs
rows 13 through 18 re-derived, and those are pure functions of already-loaded payloads, so
the cost is arithmetic rather than I/O. I took the complete one and then made the "it opens
nothing" claim checkable rather than asserted, by pointing at the observer test that would
go red if it were false.

**A redundancy question I had to settle rather than wave at.** Once row 21 compares whole
scenes, the provenance field-walk built last session overlaps it. Lesson 286 says a guard
whose deletion changes no outcome is indistinguishable from its absence. I checked: deleting
the provenance walk changes the refusal code and message a caller receives, and committed
tests assert both. So it is kept, and the reason is written into the docstring rather than
left for the next reader to re-derive.

---

## Verification

Every command used the project interpreter.

```text
focused pair (test_connection_adapter.py + test_authenticated_storage.py)
  356 passed in 21.55 s
focused pair under PYTHONOPTIMIZE=1
  356 passed in 21.30 s
packet-wide (Reproducibility Packet/tests)
  3,014 passed / 0 failed in 176.35 s
```

`test_connection_adapter.py` alone collects **336** (was 309). The arithmetic closes exactly:
2,987 + 27 = 3,014, and the 27 are 13 on finding 1 (eleven content substitutions, their
anchor, and the rendering-coverage property), 4 on finding 2 (its anchor and three
refusals), 7 on finding 3, and one each for B2, B3 and B5.

`py_compile`, `git diff --check` and `git status --porcelain` all clean. Both edited files
are pure ASCII, LF, 0 CR, no BOM, with a final newline — **checked on the final bytes**,
which is lesson 282's instrument and it was run again because this session also edited by
script. `git diff --numstat` reads `218 7` on the module and `680 1` on the test file.

**Exact state at the end of this session (unreviewed, owner-held):**

```text
Reproducibility Packet/scripts/utils/connection_adapter.py
  blob 2e7d9fa02786723cfaf068ca5018860e3c46dfaf
  raw  261b6548294272e4f5698e638fc8188fb577d03da6097c61f649d449a0d1660b
  194,417 B / 4,097 LF / 0 CR / ASCII / no BOM / final newline
Reproducibility Packet/tests/test_connection_adapter.py
  blob a783fa6ceb47dd91ef1b70229d5ec986b0a0c0a4
  raw  1dfa35a4b4df7a1af39339c9635a569a0383e2aaf6f0fabf8b528f341646ce36
  338,190 B / 8,013 LF / 0 CR / ASCII / no BOM / final newline
```

Those two blob ids are working-tree hashes taken while writing this report; they enter the
object store at this session's commit. **No mutation sweep ran, and that is on plan** — the
plan sequences it on the finished pair, and the pair is not finished.

---

## Scientific and authorization boundary

- Counters unchanged: **278 rollouts, 67 fits, 67 checkpoints, and zero pilot, validation or
  test reads.**
- No MuJoCo model was built, no rollout stepped, no fit run, no checkpoint written and no
  figure rendered from real data. The figures this session's determinism test produced are
  the synthetic coherent fixture's, into a temporary tree that was removed.
- Disclosed reads, all tracked development text or tracked fixture output, none opening a
  scientific payload: `connection_adapter.py`, `connection_record.py`, `verification_scene.py`,
  `estimator.py` and the test file, plus the Step-4a and Step-1 design documents.
- The two off-limits identity files — `scripts/utils/storage_contract.py` and
  `scripts/utils/role_contract.py` — were neither read nor edited.
- The pre-repair probe ran outside the repository and is not committed.
- Step 4b-ii-b remains **wholly unreviewed**. No Review Card and no subject chat exist for it,
  and that is deliberate: a card names a candidate, and the candidate is not stable yet.
  Eleven consecutive sessions have held that line.

## Live-Run README heartbeat

Checked, and the answer is **no**. Discharging cross-review findings and closing internal
test items inside an unreviewed build is not an artifact closure, a phase transition or a
scientific result. The public root README stays at the jointly approved blob
`7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`.

## Chats

The only active transcript I am a participant in is `Transcript Order Monitoring`. Its last
entry is my own Session-144 confirmation, and Codex reported no ordering fault this cycle.
**A clean check is not a reason to post**, so no turn was owed and none was made.

Cross-review was performed: I read Codex's `HumanReport154.md` in full and this whole session
is the response to it.

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — the three repairs.
- `Reproducibility Packet/tests/test_connection_adapter.py` — 27 net new tests.
- `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` — Appendix I, appended (`168 0`).
- `agents/Claude/Permanent Instruments.md` — lessons 287, 288 and 289.
- `agents/Claude/Session Summaries/HumanReport155.md` — this report.
- `agents/Claude/README.md` — indexed Session 155.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 156.

No Review Card, chat transcript, protocol document, Claim Sheet, configuration, result
artifact or public README byte was changed.

## Next steps

1. The `roles` CLI wiring and the **additive** `build_role_bundle` change, including the
   docstring fix design finding DA corrected — under branch B the `--config` gloss is
   `FINAL`-only.
2. The two-pass mutation sweep on the finished pair. Its staged-tree set is unchanged:
   `scripts`, `tests`, `schema`, `config` **and** `results`. A staged tree missing any of them
   is a red control and measures nothing.
3. **Then** the Review Card and the subject chat, naming the candidate three ways and
   resolving every blob id with `git cat-file -t` before the card governs. The card carries
   three disclosures, not one: the `schema.json` EOL-pin dependency, the `authenticate_sources`
   third parameter, and the `AuthenticatedConnection.record_sha256` field. Session 155 added
   no fourth.
4. Then the handoff, with an explicit owner approval of the exact state.
