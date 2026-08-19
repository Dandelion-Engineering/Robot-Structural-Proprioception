# Human Report — Codex Session 156

**Current date and time:** 2026-08-18 17:41 PDT (taken from the shell while finalizing this report)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

I completed the formal Round-1 review of Claude's finished Slot-8 Step-4b-ii-b candidate. The
eight-file candidate is authenticated exactly, the owner's 375-test focused results and 3,034-test
packet result reproduce, and the CLI wiring plus EOL-pin documentation are internally consistent.
The candidate is nevertheless **not approved**: two independently reproduced blocking states remain.

1. The new packet-root anchor reads a record from disk but compares it to a digest that is still a
   replaceable field of `AuthenticatedConnection`. A substitute root containing only the original
   record publishes despite seven missing packet-relative allowlist members. A wider substitution
   can also change the record bytes and `record_sha256` together, rebuild rows 13–20 and publish a
   digest state rows 1–2 never parsed or authenticated.
2. The PNG walk proves header fields, chunk integrity, zlib completion and decompressed length, but
   not a format-valid image. It accepts a reserved scanline filter, indexed colour without the
   required palette and an unknown critical chunk as 300-DPI evidence.

I recorded one complete two-finding Round-1 ledger in the Review Card and appended the matching
`Revisions Required` handoff to the subject chat. Claude owns one complete integration or contest
response for delta-only Round 2. Step 4b-ii-b, full sub-step 4b and every downstream gate remain
shut.

## Startup and context

The automation gates passed in the required order. `.agent-turn` named `Codex`, no
`.agent-session.lock` existed, I created the lock exclusively, and the second turn read still named
Codex. I then followed `AgentPrompt.md`: read the complete Project Details document, rewrote the
clipped middle from explicit line ranges, read Codex continuity, read every Codex-participant chat
summary and both active transcripts in full, and did not reply during the ingestion phase.

The monitoring chat required no response. The new Step-4b-ii-b subject chat contained Claude's
explicit Round-1 handoff and exact owner approval, so I read `Playbooks/review-cycle.md`, the complete
Review Card, Claude's Session-156 report and the governing design before beginning formal review.

Repository state before review was clean at `2fb5a7e3cbb176fbfa03dd0322df05dbbf0cc206`, with
`HEAD == origin/main`.

## Candidate authentication and scope rulings

I independently authenticated all eight candidate blobs from the Git object store. Every full blob
id, raw SHA-256, byte count, LF/CR count, BOM claim and final-newline claim matched the card. The
declared Git numstats also reproduced exactly.

Two scope rulings were accepted before content review:

- Both `.gitattributes` files belong in the card. They are the bounded documentation repair for the
  load-bearing `schema.json` EOL pin's second raw-digest consumer.
- One row-21 re-read of the already allowlisted connection record is admissible in principle, and a
  packet genuinely copied and authenticated under its copied root must remain usable. The narrowed
  open-set property is therefore not itself a finding; the defect is that the candidate does not
  establish the anchor or the copied-packet accept claim it states.

I made no edit to any of the eight candidate files.

## Finding 1 — packet-root identity remains substitutable

`_require_one_packet_root` leaves `BoundPaths` to read the record path, but it compares those bytes
to `connection.record_sha256`. That digest is another replaceable field of the same in-memory
`AuthenticatedConnection` whose `bound` and `expected_opens` the candidate's own tests replace.

Two OS-temporary-root probes made the boundary concrete:

### Record-only substitute root

I authenticated the ordinary three-case fixture, coherently moved every packet-relative bound path
and every packet-relative expected-open path to a new root, and copied only the original record file
to its expected location. Seven packet-relative allowlist entries were absent. `write_bundle`
accepted and published all eight files beneath the substitute root.

This proves the existing copied-packet test's full `copytree` is not decisive. The test does not run
`authenticate_connection` against the copy; it rewrites an already-authenticated connection, and
row 21 checks only the copied record. Removing the copied schema, config and source files does not
change its verdict.

### Record bytes and digest moved together

I changed the moved record bytes from `schema` to `schemA`, replaced
`connection.record_sha256` with that file's new digest, re-ran rows 13–20 from the substituted
connection and invoked row 21. The candidate accepted and published all eight files. The new digest
appeared in every scene even though rows 1–2 had never parsed or authenticated the altered record
state.

The repair must make the accept control authenticate against the copied root and must refuse both
post-authentication substitutions. The architectural mechanism belongs to Claude; another
field-to-field comparison would repeat the three-session failure pattern.

## Finding 2 — PNG length is not PNG validity

The exact candidate accepted all three of these streams as `(11811, 11811)` pixels per metre:

- a CRC-valid 1x1 greyscale stream whose sole scanline uses reserved filter type `5`;
- a CRC-valid 1x1 indexed-colour stream with no `PLTE`; and
- a CRC-valid 1x1 greyscale stream with an unknown critical `ABCD` chunk.

The first was also refused by Pillow as an unrecognized stream, but the candidate explicitly chose
the format rather than decoder behaviour as its authority. The W3C PNG Third Edition confirms that
filter method 0 defines exactly types 0–4, indexed-colour images require `PLTE`, and unknown critical
chunks cannot be safely ignored:

- <https://www.w3.org/TR/png-3/#9Filter-types>
- <https://www.w3.org/TR/png-3/#11PLTE>
- <https://www.w3.org/TR/png-3/#5Chunk-naming-conventions>

The Round-2 repair must walk the decompressed scanline/pass layout and validate every filter byte,
including every non-empty Adam7 pass, and enforce the palette and critical-chunk rules needed by the
admitted colour type. The four tracked matplotlib figures remain the required accept side.

## Verification

The owner's green evidence reproduced on the exact committed bytes:

```text
focused pair                                          375 passed / 33.00 s
focused pair under PYTHONOPTIMIZE=1                  375 passed / 32.96 s
packet-wide                                        3,034 passed / 175.99 s
```

The optimized run emitted only pytest's expected warning that assertions are disabled under `-O`.
All six Python candidate files parsed under `ast`; a fresh dependency-light import left `torch` and
`mujoco` absent. `git diff --check` was clean. Five direct adversarial probes established the two
findings above; all used generated bytes or contract fixtures beneath OS-managed temporary roots.

No scientific resource moved. No MuJoCo model was built, no rollout stepped, no fit run, no
checkpoint written and no production role, result, config or held-out split was read. Counters
remain **278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads**.

## Review record and append integrity

The Review Card now reports `OPEN — Round 1 Revisions Required` and contains the two numbered
blocking findings, independent evidence and the unchanged authorization boundary.

The subject-chat append passed the complete prefix gate:

- prior state: **10,128 bytes / 161 LF / 0 CR**, SHA-256
  `399a1895032c8383a1b9424490c4b49c6a1a16653d65e461624ac2a729e9d0eb`;
- that entire prior byte sequence remains the exact prefix;
- the Codex Session-156 header occurs exactly once after the boundary;
- the chat delta is **+65/-0**, Codex is physically last, and the post-write state is
  **13,521 bytes / 226 LF / 0 CR**, SHA-256
  `2e9fa1fd5e7dd184eac42be9c5aa774230ec6d614b0bccc0dd02d2f93f85f3c2`.

No Transcript Order Monitoring entry was warranted because no append-order fault occurred.

## Public heartbeat and decisions

The root Live-Run README was checked and deliberately left unchanged. This session returned an
open candidate for revisions; it did not finish an artifact, close a phase or create a public
milestone. The next public heartbeat belongs to the terminal outcome, not to an intermediate
Round-1 block.

No progress report is due; Codex's next regular report remains Session 160.

## Files created or updated

- `Review Card/Slot-8 Step-4b-ii-b Coherence Geometry and Output.md` — appended the complete
  Round-1 reviewer ledger and updated the open status.
- `chats/Claude-Codex/Slot-8 Step-4b-ii-b Coherence Geometry and Output/Slot-8 Step-4b-ii-b
  Coherence Geometry and Output - Active.md` — appended the byte-verified Revisions Required
  handoff.
- `agents/Codex/Session Summaries/HumanReport156.md` — this report.
- `agents/Codex/README.md` — updated navigation and current Step-4b-ii-b state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 157.

## Next steps

1. Claude should answer both findings in one redundantly authenticated Round-2 candidate.
2. The delta must include machine-checkable changed/unchanged-region evidence. Round 2 is
   delta-only; unchanged material is not re-audited from scratch.
3. The packet-root repair must use a genuinely re-authenticated copied packet as its accept control
   and refuse the record-only and moved-record-digest states.
4. The PNG repair must validate scanline filter bytes, required palette semantics and unknown
   critical chunks while retaining the tracked figure accept set.
5. Until same-state approval closes the card, Step 4b-ii-b, full 4b, all production connection
   records, real-role reads, Steps 4c–4f, capacity/threshold selection, config freeze and every
   C1-versus-S statement remain unauthorized.
