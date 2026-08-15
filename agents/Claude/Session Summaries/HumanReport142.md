# Human Report — Claude Session 142

**Current date and time:** 2026-08-15 15:41 PDT (measured with the shell immediately before writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

## Outcome

Codex returned my Slot-8 Step-4b-ii-a candidate in its Session 141 with **Revisions Required** and a
six-finding Round-1 ledger. This session was the owner response to that ledger. I accepted all six
findings without contest, integrated all six, wrote 47 new tests that build the states the findings
named and drive them, ran the mandatory two-pass mutation control, and handed the new state back for
a delta-only Round 2.

The candidate is two files, both already in the repository from Session 141 and both modified here.
Nothing else in the project moved: no protocol document, no schema, no configuration, no result, no
role byte, no closed blob, and no public README byte.

**No scientific resource was spent.** No role payload, checkpoint, estimator output, controller log,
production config or held-out split was opened; no MuJoCo model was built, no rollout stepped, no fit
run, no figure rendered. Project counters stand unchanged at 278 rollouts, 67 fits, 67 checkpoints
and zero pilot/validation/test reads.

## What the six findings were, and what I did about each

Codex's ledger is in `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md`. In plain terms:

**1. The bytes the chain authenticated were not always the bytes it then interpreted.** The adapter
would read a file, take its digest by *opening the file again*, and then parse the bytes from the
first read. Codex demonstrated the consequence with a probe that changed a file between those two
operations and got the adapter to accept a document under the approved digest of a different one.
The same shape appeared at five more places, including the role indexes — where a changed index could
have pointed the payload loader at a file the record never named.

The repair has two halves. Where I own the parsing, every file is now opened **exactly once** and its
digest is taken over the bytes that read returned; a new function, `authenticated_bytes`, is the only
way a file enters the module. Where a closed, already-approved utility does the parsing and takes a
*path* rather than bytes, I could not change how it reads without editing a foundational file, so the
chain now **brackets** those calls: digest, call, digest again. Any change still present when the
utility returns refuses. I said explicitly what the bracket does not cover — a change made and undone
inside a single call — and asked Codex to rule whether closing that last gap belongs in this card,
rather than editing two closed utilities on my own authority.

One genuine improvement fell out of this: the configuration step no longer calls `load_config` at
all. The config contract already exposes a document-level entry point, so the adapter parses the
schema and config from its own authenticated bytes and hands the *documents* to the contract. Three
file reads disappeared.

**2. What the chain returned could still be edited afterwards.** The validated configuration's
document and every loaded payload array were writable, so a later stage could have consumed facts
different from the ones that were authenticated. The configuration document is now deeply read-only,
and every payload array is rebuilt over an immutable buffer — which matters, because a NumPy array
that owns its own memory can simply have its "read-only" flag switched back on by whoever holds it.

**3. The dataset never had to agree with the configuration.** The manifest rows and both dataset
audits each record which configuration generated them; the adapter checked them against the record's
echo and against each other, but never against the configuration it had actually validated. Codex
built a tree where every file was internally consistent on configuration B while the record,
established result and payloads were on configuration A — and the chain accepted it. The adapter now
joins both audits and every manifest row to the validated configuration. This turned out to be the
same rule the packet's own role-payload loader already applies to role indexes, so the manifest and
audits are now held to a standard the rest of the packet was already holding.

**4. Number comparison was lossy and could crash.** Both sides were being converted to 64-bit
floating point before comparison, so two different integers could compare equal, and an integer of
about four hundred digits made the conversion raise a raw error instead of the refusal the design
assigns. Nothing is converted now; Python compares integers and floats exactly, and the crash path
is gone.

**5. A boolean passed as a count.** In Python `True == 1` and `False == 0`, so an audit could report
its census with booleans in place of numbers and pass an equality check. Types are now required
before values are compared.

**6. A very long numeric segment in a field path crashed.** Python refuses to convert integer
strings beyond 4,300 digits, so a small, valid record could produce a raw error instead of a
refusal. Segments are now bounded at 19 digits — the most any in-memory array could need — and, as I
found while making the repair, they must also be ASCII: Python considers the superscript "²" a
digit, and converting it raises the same kind of raw error.

## Four things I found afterwards, all of which went against me

These are recorded because the value of writing them down is that a later session does not
rediscover them as new problems, and because two of them are the kind of mistake that is easy to
leave in.

1. **One of my own repairs was a guard that nothing could trigger.** I had added a re-measurement of
   the schema after the configuration contract runs. It cannot ever be the check that refuses,
   because the contract already compares the schema's bytes against a digest the configuration
   document declares, and that document is fixed for the whole call. So any schema change refuses
   inside the contract first. I deleted the guard and wrote the proof where it stood. This is the same
   shape as a defect the previous session's mutation sweep found in my code.
2. **A presence check inside the new read function was undecidable in the same way** — an absent
   file, a directory and an unreadable file all fail at the read itself — so it went too.
3. **Two of my new tests were testing nothing.** The mutation sweep flagged a mutant that survived:
   my "swap the file between reading it and digesting it" tests actually performed the swap *before*
   both operations, which correct and defective code treat identically. Moving the swap to fire
   immediately after the read returns separated them. A second mutant on the configuration path
   surfaced the same flaw and got the same repair. **This is the fifth build in a row on this lane
   where the mutation sweep changed the tests rather than confirming them**, which is worth saying
   plainly: it is not a formality at the end of the work, it is part of the work.
4. **My own repair quietly changed data.** The function that makes payload arrays read-only used a
   NumPy call that is documented to return an array of at least one dimension — so a scalar field came
   back as a one-element list, *after* the loader had validated its shape against the schema. I found
   it with a small edge-case probe over six array shapes rather than through any test I had written,
   fixed it, and added a test whose zero-dimensional case exists only because of it.

## Evidence

- Focused suite: **156 passed** (109 at the Round-1 state, so this response adds 47 tests and removes
  none), and **156 again under optimized Python**.
- Packet-wide suite: **2,764 passed, 0 failed, 216.66 s**. The prior figure was 2,717; 2,717 + 47 =
  2,764 exactly, which is the arithmetic that says this response adds tests and changes no existing
  one.
- `py_compile` clean on both files; `git diff --check` clean; `git status --porcelain` reports exactly
  the two candidate files plus the review card and the subject chat.
- A fresh interpreter importing the adapter leaves `torch` and `mujoco` absent and brings in only
  `numpy` — re-measured rather than quoted, and pinned by a test that re-measures it on every run.
- **Two-pass mutation control, 30 mutants (28 real + 2 negative controls), 381.4 s, staged entirely in a scratch directory outside the
  repository:** 28/28 real mutants caught, both negative controls surviving, identical across both passes. No bad anchors in the final run; the target file's digest was
  restored and verified after every single mutant.
- Delta evidence for the reviewer: `git diff --numstat` plus a machine-computed region map naming
  every top-level block that changed, was added, or is **byte-identical**. In the module, 7 blocks are
  new, 15 changed and 22 byte-identical; in the tests, 30 are new, 2 changed and 89 byte-identical.

## Decisions I made

- **I contested nothing.** All six findings were correct as written, and integrating a reviewer's
  finding costs one round less than arguing about it when I would have written the same repair
  myself.
- **I did not edit a closed utility, and I did not pretend the gap that leaves is closed.** The
  honest position is that the bracket covers every change that persists and not a change reverted
  inside one call, and that closing the rest requires touching two foundational files. That is a
  scope decision the reviewer owns, so I stated it precisely and asked for the ruling instead of
  taking it.
- **I used the configuration contract's document-level entry point rather than reimplementing
  anything.** The project's standing rule is to point at the object that owns a fact rather than
  copy it; the two new bytes-domain digest functions are the one place I came close to copying a
  rule, and they are held to the functions that own those rules by an equality test that runs every
  time.
- **I stated the fail-closed consequence of exact number comparison rather than hiding it.** A
  declared value that 64-bit floating point cannot hold exactly will now refuse against a source
  carrying the exact integer. That direction is safe, and it is written into the code.

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — the six repairs.
- `Reproducibility Packet/tests/test_connection_adapter.py` — 47 new tests; no existing test deleted,
  renamed or weakened.
- `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md` — Round-2 owner response, candidate
  identities, delta evidence and the scope question.
- `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/Slot-8 Step-4b-ii-a Authentication Chain - Active.md`
  — the Round-2 handoff.
- `agents/Claude/Session Summaries/HumanReport142.md` — this report.
- `agents/Claude/README.md` and `agents/Claude/Summary of Only Necessary Context.md` — index and
  continuity.

## Public heartbeat check

The public README remains Phase 2 / In Progress with a current banner. This session returned a
revised implementation candidate into an open review. It did not finish an artifact, close a phase,
produce a scientific result or create a public milestone, so I left the root README unchanged — the
running log is lean by design.

## Next steps

1. Codex performs the delta-only Round-2 review, and rules on the one scope question about the three
   closed utilities.
2. If the card closes, 4b-ii-b — read-order rows 13 to 21, the coherent geometry fixture, the
   fourteenth exit code, the audit-hook observer, the remaining acceptance tests, the CLI wiring and
   the additive change to the Step-2 blob — is the only unbuilt work in the project, under its own new
   card and chat, with its mutation sweep budgeted **before** the handoff.
3. Everything downstream stays shut: authoring a production connection record, the two authorization
   halves, the one authorized invocation, the capacity selection, the threshold calibration, the
   configuration freeze, the geometry-validation artifact, and any C1-versus-S statement.

My next regular progress report is Session 144, or sooner if a phase transition or an approved
Claim-Sheet amendment fires first.
