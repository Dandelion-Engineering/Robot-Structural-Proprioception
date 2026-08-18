# Human Report — Claude Session 156

**Current date and time:** 2026-08-18 16:11 PDT (taken from the shell while writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

Codex was right an eighth time. Its Session-155 review left two forward blockers against my
Step-4b-ii-b build; I drove both at source before changing a line, both reproduced exactly as
reported, my re-drive of each widened it, and I contested neither. **Both are discharged.**

**Then the session finished the lane.** The `roles` CLI wiring and the additive
`build_role_bundle` change — the last two items on the carried build list — are done. The two-pass
mutation sweep ran, found one real gap, and I repaired it. **And for the first time in twelve
sessions there is a Review Card and a subject chat for this half, with my explicit owner approval
of the exact eight-file candidate.** Sub-step 4b-ii-b is handed off for Round 1.

**The two findings are one sentence, and it is the sharpest form this lane has produced:** an
anchor that lives inside the value under suspicion can always be widened by one more substitution,
so the anchor has to leave the value. That is not a slogan — it is a measured three-session
pattern, and my own lesson from last session was the half of it that was wrong.

| session | what the repair anchored to | how the next session defeated it |
|---|---|---|
| S153 | the provenance block, to the connection | S154 moved `output_root` beside it |
| S154 | `output_root`, to `bound.packet_root` | S155 moved both together |
| S155 | `packet_root`, to `bound.record_path` | S156 (Codex) moved the whole path set |

`record_path`, `packet_root`, `output_root`, `schema_path`, `config_path` and `packet_artifacts`
are six fields of **one** separately constructible value. A check that compares them to each other
proves they agree; agreement is preserved by any coherent move, so it can never prove they are the
paths the chain authenticated. The repair terminates the regress by consulting something outside
the value entirely: **the record's bytes on disk**.

---

## What I did

### 1. Both findings driven at source before any repair

**Finding 1 — the packet root moves with its whole bound set.** I re-drove Codex's exact
substitution on a genuinely authenticated three-case connection: every packet-relative
`BoundPaths` field moved coherently into a temporary tree that **did not exist**, with
`expected_opens` left naming the authenticated tree.

```text
substituted packet_root  <tmp>/other-packet
substituted record_path  <tmp>/other-packet/results/verification_connection/records/...
             exists?     False
allowlist entries under the substituted root   0
outcome                  ACCEPTED, all eight files published beneath <tmp>/other-packet
```

**Finding 2 — ordered chunks are not a decodable image.** Codex reported two byte streams that
crossed my Session-155 PNG walk at `(11811, 11811)`; my re-drive found four more.

```text
IHDR width 0                           -> (11811, 11811)   Pillow: UnidentifiedImageError
IDAT body b"not-a-zlib-stream"         -> (11811, 11811)   Pillow: broken data stream
IHDR height 0                          -> (11811, 11811)   [re-drive]
IHDR colour type 7 (undefined)         -> (11811, 11811)   [re-drive]
IHDR compression method 1 (undefined)  -> (11811, 11811)   [re-drive]  Pillow: DECODED (4, 4)
zlib-valid IDAT, 3 bytes for 4x4       -> (11811, 11811)   [re-drive]  Pillow: truncated
```

**The compression-method row is the one worth carrying**, and it is why "just use a decoder" is not
the repair — which matters, because a strict decoder was one of the two repairs Codex offered.
Pillow **accepted** it. The format defines exactly one compression method; a decoder that renders
something is not evidence that what it rendered is what the file declared. The standard applied
here is the format, not a decoder's willingness to guess. (The packet also declares no decoder, so
that route would have added a dependency for a check the walk was already positioned to make.)

### 2. The repairs

**Finding 1.** `_require_one_packet_root` now runs three checks in an order that is itself the
argument. First, two cheap sweeps against `connection.expected_opens` — the allowlist row 3 derived
from the record, a *second witness* to the paths this chain resolved — requiring every bound path to
be a member of it and every member to be inside the packet root or under the role or checkpoint
root. **That is deliberately not the anchor**: `expected_opens` is a field too, and moving it as
well walks straight past it. Second, the anchor: `external_digest(record_path)` must equal
`connection.record_sha256`, the digest the CLI authorization named and rows 1–2 checked. Third, an
unreadable record is now a *named* refusal — my re-drive of the widened substitution reached the
digest read and raised a raw `FileNotFoundError`, which nobody had reported.

**The accept side lands exactly where the design says it should, and that is the best evidence the
instrument is right rather than merely strict.** A whole packet copied and run against the copy has
one root *and the record's bytes are in it*, so it publishes. That test is written **first**, above
the three refusals, because a helper that refused it would satisfy every refusal test under it
while breaking the one invocation invariant W8 explicitly permits.

**Row 21 therefore now opens one file outside the tree it creates, and I disclosed that rather than
absorbing it.** The committed audit-hook test previously said row 21 opens *nothing* outside that
tree. It now states the bound: exactly one such path, it equals the bound record path, it is in the
section-4.2 allowlist, and it is opened **exactly once** — that last clause because a check that
quietly became a re-read per case would still satisfy a set comparison. **It is the card's fourth
disclosure, and I asked Codex to rule on it specifically, saying I would take the finding rather
than defend it if the narrowing is not worth the anchor.**

**Finding 2.** The walk now refuses every header value the format does not define — dimensions,
colour type, bit depth for that colour type, compression method, filter method, interlace method —
requires the `IDAT` run to decompress as zlib, and requires the decompressed length to equal
*exactly* what a new derivation computes from the header. The derivation has its own control driven
against hand-worked literals, including sub-byte packing at bit depth 1 and the Adam7 interlaced
total (79 against the non-interlaced 72). **Adam7 is derived rather than excused**: matplotlib
writes non-interlaced files, so a length check that skipped the interlaced branch would be a hole
shaped exactly like a legal PNG.

### 3. A defect I found in my own repair, and a number of mine that was wrong

**`zlib.decompress` silently ignores bytes appended after a complete stream.** Measured:
`zlib.decompress(zlib.compress(body) + b"GARBAGE")` returns `body` and raises nothing. Nobody
reported this; it came out of asking the same question of my repair that Codex has been asking of
my code. The walk now drives a `decompressobj` and requires `eof` with an empty `unused_data`, so
the image data must be the whole of the `IDAT` run rather than a prefix of it.

**Session 154 said "the ten tracked Step-3 figures", here and in its report.** Ten is the number of
tracked *files* under `results/verification_fixture` — four figures, four scene documents, the
bundle and its digest. **Four is the number of figures.** Corrected forward, and the count is now a
literal rather than something taken from the same glob it guards, because a count read from the
thing under test cannot notice the thing under test going missing.

### 4. The `roles` CLI wiring and the additive `build_role_bundle` change

`build_role_bundle` still refuses unconditionally before reading any argument, and that remains
correct until the whole of sub-step 4b closes. Three things changed around it:

- **`output_dir` is now a parameter.** The design closes six CLI arguments and the `roles` mode has
  parsed all six since; this entry point took the other five — so *the one argument that decides
  where a real invocation would publish was the one the entry point could not see*.
- **There is deliberately no `packet_root` parameter**, and the pinned-signature test now says so
  in as many words.
- **Finding DA's correction reached the live docstring**, which still glossed `--config` as "the
  exact frozen config file". Under the ruling that gloss is `FINAL`-only, and a builder following
  the old sentence writes an unconditional `require_frozen=True` and silently un-reaches the
  development branch.

**The wiring got its own test, and it is the one the mode was previously failing.** It compares the
forwarded keywords against **the parsed namespace** rather than against a list written in the test
— a list written in the test would have to be edited in the same commit that dropped an argument,
and would then agree with the defect. Nothing caught the dropped `--output-dir` before, because
every test below it asserts a refusal and a refusal is reached whatever it is handed.

### 5. The mutation sweep, which earned its cost

Two passes, 26 mutants (23 real + 3 negative controls), staged entirely outside the repository with
the mandatory harness shape. Pass 1 1,229.1 s, pass 2 1,216.3 s, **verdicts identical, zero bad
anchors, all three negative controls surviving in both passes**.

**One real mutant survived, and it was a genuine test gap rather than an equivalent mutant** —
turning the image-data length check from `!=` into `>` did not go red. The reason is worth keeping:
the committed wrong-length figure compresses three bytes for a two-byte image, so it is *longer*
than declared and a greater-than test refuses it too. The row's **equality** was never the reason
that case was green. The repair is the missing fixture — an image *shorter* than declared, which is
also the direction that matters more, since a decoder handed too little data produces a partial
image rather than an error. **The pair is the instrument; either one alone measures half of it.**

A supplementary two-pass sweep then re-drove that mutant and its neighbours on the **exact
candidate bytes**, because the main sweep's staged tree was taken before three later edits. The
delta between the swept tree and the candidate was measured by diff rather than asserted.

### 6. The Review Card and the subject chat

`Review Card/Slot-8 Step-4b-ii-b Coherence Geometry and Output.md` and its subject chat are open,
naming an **eight-file** candidate by full blob id, raw SHA-256 and size/line-ending figures, with
every blob id resolved by `git cat-file -t` before the card governs. The card carries the four
disclosures, nine acceptance criteria, a blocking-severity definition, and the full round evidence.
I gave the explicit owner approval of those exact bytes.

---

## Verification

```text
focused pair (test_connection_adapter.py + test_authenticated_storage.py)   375 passed
same pair under PYTHONOPTIMIZE=1                                            375 passed
packet-wide  "Reproducibility Packet/tests"       3,034 passed / 0 failed / 177.64 s
```

3,014 + 20 = 3,034, and the arithmetic closes exactly: 12 malformed-PNG cases, 1 image-size
derivation control, 6 packet-root cases, 1 CLI-forwarding test. `py_compile`, `git diff --check`
and `git status --porcelain` all clean; all eight candidate files pure ASCII, LF, 0 CR, no BOM,
final newline, checked on the final bytes.

---

## Challenges, and how they were handled

**A test that was only green because the check did not look.** Adding the record re-read turned
`test_the_packet_root_anchor_accepts_the_chain_it_is_written_for` red. The cause was the test's own
shape: it drove the helper *after* the fixture installer had exited and restored every byte it
touched, so it measured a restored record against a digest authenticated over the installed one.
The call moved inside the installer's block. An authenticated value is only meaningful while the
tree it authenticated still stands; that was always true and is only now observable. **A repair
that turns an existing test red is worth reading before it is worth fixing.**

**Deciding whether to widen a committed instrument.** The record re-read costs the audit-hook test
its unqualified form. I took that deliberately rather than hunting for another in-value anchor,
because three sessions of in-value anchors have each been defeated by one more substitution, and
because the claim being made — *one root holds the packet this chain authenticated* — is a claim
about the filesystem, which is settled by looking. The widening is bounded to one named path,
asserted rather than described, and disclosed on the card with an explicit invitation to overrule
it.

**Editing after the sweep had been staged.** Three edits landed after the main sweep's staged tree
was taken — two documentation blocks, the `decompressobj` guard, and the R09 repair. Rather than
report the sweep as if it had covered them, I measured the delta by diff (`+47/−2` in the module,
`+48/−2` in its test file, nothing in the other four files) and ran a supplementary two-pass sweep
over the affected region on the exact candidate bytes.

---

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — the packet-root anchor, the PNG
  header/image-data checks, the EOL-pin disclosure.
- `Reproducibility Packet/tests/test_connection_adapter.py` — new cases for both findings and the
  sweep's survivor.
- `Reproducibility Packet/scripts/utils/verification_scene.py` — `build_role_bundle` gains
  `output_dir`; finding DA's docstring correction.
- `Reproducibility Packet/scripts/render_verification_scene.py` — the `roles` mode forwards all six
  closed CLI arguments.
- `Reproducibility Packet/tests/test_verification_scene.py` — the strengthened signature test.
- `Reproducibility Packet/tests/test_render_verification_scene.py` — the CLI-forwarding test.
- `.gitattributes` and `Reproducibility Packet/.gitattributes` — the pin's second consumer named.
- `Review Card/Slot-8 Step-4b-ii-b Coherence Geometry and Output.md` — **new**.
- `chats/Claude-Codex/Slot-8 Step-4b-ii-b Coherence Geometry and Output/` — **new** subject chat.
- `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` — Appendix J (appended; nothing overwritten).
- `agents/Claude/Session Summaries/HumanReport156.md` — this report.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`,
  `agents/Claude/Permanent Instruments.md` (lessons 290–293) — session closeout.

---

## Scientific and authorization boundary

**This session spent zero scientific resource.** No MuJoCo model was built, no rollout stepped, no
fit run, no checkpoint written and no figure rendered. No role index, role payload, checkpoint,
estimator output, controller log, production config or pilot/validation/test result was opened.
Counters stand unchanged at **278 rollouts, 67 fits, 67 checkpoints**, and pilot/validation/test
reads remain **zero**.

Reads outside tracked development text: the four tracked Step-3 fixture PNGs under
`results/verification_fixture/`, opened for their chunk structure only, to show the stricter walk
still accepts real matplotlib output. Both probes and both mutation sweeps ran **outside the
repository**. The two off-limits identity files were neither read nor edited.

Everything downstream remains unauthorized: the whole of sub-step 4b until this card closes,
production connection records, real-role reads, steps 4c–4f, the capacity selection, the threshold
calibration, the config freeze and every C1-versus-S claim. **A closed review loop authorizes the
next step only, and never a run.**

---

## Chats and public heartbeat

I read every `Summary.md` in the chat folders I participate in and the complete active
`Transcript Order Monitoring` transcript before writing anywhere. Its physical tail is my own
Session-144 independent confirmation; no response is owed there, and a clean check is not a reason
to append. **I appended nothing to it.**

I opened the Step-4b-ii-b subject chat and posted the Round-1 handoff turn.

The public README heartbeat was checked and **left unchanged**, deliberately: the log is lean by
design and its entries mark finished artifacts, phase closes and genuinely noteworthy events. A
*handoff* is not a closure — the precedent is my own Session 144, which logged 4b-ii-a when it
closed at both approvals, not when it was handed off. The entry for this half belongs at its
terminal outcome.

---

## Next steps

1. **Codex reviews the candidate.** Round 1 is open and the ball is entirely in the reviewer's
   court; nothing on this lane is mine until a response lands.
2. **I must not edit the candidate while it is under review.** If I find a defect in it, the move
   is a chat turn naming it and a scope statement, not a silent repair.
3. When the response arrives, the owner re-review runs under `Playbooks/review-cycle.md`: re-open
   the artifact, genuinely re-read both the feedback and any edits, and either explicitly approve
   or edit and hand back. The loop closes only when both agents approve the *same* state.
4. **Closing this card closes sub-step 4b**, which licenses step 4c and nothing else. Steps 4c–4f
   stay blocked on the authority-appropriate approved config, the capacity selection, the threshold
   calibration, the established result and the geometry-validation artifact.
5. My next regular progress report is **Session 160**; Session 152's covers S145–S152.
