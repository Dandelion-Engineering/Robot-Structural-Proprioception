# Human Report — Claude Session 143

**Current date and time:** 2026-08-16 11:05 PDT (measured with the shell immediately before writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## The short version

I owed the final integrated response on an open review. Codex had found a real hole: the
adapter hashed a file and then let a closed utility re-open the same filename, so the bytes
that got checked were not provably the bytes that got used. Its ruling said the repair had
to go into two closed utility files, and it formally put those files in scope.

I built exactly that repair. It worked — and it broke seventy-seven tests, for a reason
neither of us had seen: **those two files' exact bytes are recorded inside three completed,
approved, un-rerunnable pieces of the project's history.** Changing them makes the project
unable to read its own finished work.

So I reverted that state completely, built the same repair in a new file that nothing
records, and handed back a candidate where the hole is closed, every closed file is
byte-identical to its approved state, and the whole test suite is green. I also told Codex
plainly that this is not the shape it authorised, and that if it wants the other shape
instead, that is a decision about amending approved history and belongs in its own round.

Nothing scientific was spent. No experiment ran.

---

## What the problem actually was

A one-paragraph version for the non-specialist, because the rest of this report leans on it.

When this software is asked to trust a file, it takes a fingerprint of the file and compares
that fingerprint against the one a reviewed document says it should have. That is only worth
something if the file it *fingerprints* is the file it then *uses*. The earlier version
fingerprinted a filename, handed the filename to another component, and that component opened
the name again. Between those two moments the file on disk can change. Codex demonstrated
this concretely: it let the check run on the real data file, swapped in a different but
otherwise valid file immediately afterwards, left it there — and the whole chain accepted, and
handed back numbers from the substituted file.

The fix is conceptually simple: read the file **once**, and pass the bytes you actually read
to everything downstream, so there is never a second look at a name that could have changed
underneath you.

---

## The thing that made this session harder than it looked

The two files that needed the new entry points are `storage_contract.py` and
`role_contract.py`. They are foundational: almost everything in the project reads data through
them.

They are also **fingerprinted by the project itself**. When this project trains a model, it
records the fingerprints of the eight source files that define how the training worked, so that
a result can never be silently attributed to different code than the code that produced it.
`storage_contract.py` and `role_contract.py` are two of those eight.

Three approved, completed artifacts record those fingerprints:

- the development-fit ledger,
- the stage-1 capacity-sweep plan,
- the rung-2 escalation plan.

Each of those came from a run that is **spent** — the project deliberately authorises those
runs once and never again. They cannot be redone.

I built Codex's accepted repair first, and that is what exposed this. The focused tests passed.
The full suite came back **52 failed, 25 errors**, every one of them on the same message:

> the code that fits these arms differs from the code that fitted the approved anchor at
> role_contract.py, storage_contract.py

And the damage is wider than a test count. The two read-only analysis scripts — the ones the
Reproducibility Packet's own instructions tell an outside reader to run — check the recorded
fingerprints against the current files before they will read a finished run. So editing those
two files would mean that a stranger who downloads this project and follows its instructions
**cannot reproduce three of its completed results**, through no fault of their own. That is a
direct failure of one of the project's hard standards, not an inconvenience.

The project had already ruled on exactly this shape once, for three *other* files in the same
group of eight: don't edit them, write the limitation down instead. This is that rule reaching
two more of the same eight.

I reverted the whole attempt. All four files Codex's ruling listed are back at the exact
approved bytes, and I proved that by identifier rather than by claiming it.

---

## What I built instead

A new file, `Reproducibility Packet/scripts/utils/authenticated_storage.py`, which nothing
records the fingerprint of and which is therefore free to change. It provides the same entry
points over already-read bytes, and — this is the part that matters — **it does not rewrite any
of the rules.** Every actual check is reused from the file that owns it: the manifest audit, the
index row grammar, the payload's schema and semantic validation, the folder-layout rule, and the
loader class itself, which the new class inherits from.

What the new file *does* restate is the mechanical part that comes before the rules: reading a
CSV header and typing its columns. That is genuine duplication and I did not hide it. It is held
shut by equality: the tests require the new parser to return *exactly* what the old one returns
for the same document, and drive the same malformed documents through both, requiring identical
error messages. If the two ever drift, a test goes red. That is the same discipline this project
already uses elsewhere when a fact has to be repeated.

---

## What the repaired chain does now

Every file the chain interprets is read once, and the bytes from that read are what get
fingerprinted, parsed, loaded and compared. The old "bracket" — fingerprint before, fingerprint
again after — is deleted outright, because with a single read there is nothing left for it to
guard.

I proved it the way Codex asked, at the exact state its probe used: replace the file immediately
after its one read, **leave the replacement there**, and require that the chain accepts and hands
back the *original* values. Codex's probe got the substituted number; this version returns the
authenticated one. Three mirror tests replace the file *before* the read and require a refusal, so
the claim is "the read moved," not "the check was dropped."

---

## The instrument that earned its place

I wrote one test that counts how many times the chain opens each file, across the entire
operation, including inside the closed components. It requires exactly one open per file.

This is a measurement no individual check can make — each one can only say that *it* read once.
It immediately found two second-reads I did not know about:

1. **A calibration file was being read twice.** Two different settings both point at the same
   file, and each was verifying it independently. Two reads of one name are two different
   objects; checking two claims against two objects is not the same as checking that the two
   claims agree. Now the file is read once and both claims are checked against that one reading —
   and a separate test confirms that reading once did not turn into believing whichever claim
   came first.

2. **The schema file is read twice, and I could not close it in this round.** The second read
   happens inside a *fourth* closed component, one Codex's scope ruling does not cover. I
   measured precisely what that window can and cannot do — substituted bytes are caught by that
   component's own comparison, and cannot change which rules were applied — and I pinned the
   count at exactly two, with the reason written into the test. Pinning it is what makes any
   *new* second read anywhere in the chain fail, instead of quietly joining an allowance.

I deliberately did **not** add a guard for that second one. Making it decisive would have needed
a fixture with two different schemas, which cascades into rebuilding the configuration, the
manifest, both audits and every index row — and adding a guard that no test can prove does
anything is a defect this very review has already caught twice.

---

## One bug the repair uncovered

A data file can carry exactly the fingerprint it is supposed to and still be unreadable —
truncated, or internally corrupted. That failure raises an error type that was not in the list
the code caught, so instead of the clean, named refusal the design promises, it would have
escaped as a raw crash. Fixed in the new file, which translates it, while deliberately letting a
caller's own legitimate refusal pass through untouched.

---

## The mutation sweep, which went against me again

Before handing anything over I run a control that deliberately breaks my own code, one change at
a time, and checks that the tests notice. Twenty-eight variants, run twice, entirely outside the
repository, with the original bytes restored and verified after each one.

**Twenty-five of twenty-five real breakages were caught.** But it first found two of my own tests
measuring nothing — the sixth build in a row where this control has changed the tests rather than
confirming them:

- Deleting a validation call from the new parser broke nothing, because every test that
  exercised that rule reached it through a different door.
- Deleting the clause that lets a caller's own error pass through unchanged broke nothing,
  because the wrapper *quotes the original error inside its own message* — so a test matching on
  the original wording passes either way. The test now checks that the object that comes out is
  the same object that went in.

A third result went the other way from my prediction, and I recorded that too rather than
quietly accepting the good news.

---

## Where this leaves the project

The review is at Round 3, which is the ordinary final round. I have handed back a candidate that
closes the finding, keeps every approved file untouched, and passes everything. But I did it in a
different shape from the one Codex authorised, and I said so directly rather than presenting it
as compliance. If Codex judges that the fingerprints should move instead, that is an amendment
against three approved artifacts and belongs in its own round — I did not take that decision
myself.

Everything downstream remains shut: the second half of this build step, the full sub-step, and
every gate beyond it.

---

## Decisions I made, and why

1. **Build the accepted repair first, then revert it whole.** Building it is what surfaced the
   blocker; arguing about it in the abstract would not have. Reverting it whole — rather than
   keeping "just a bit" of it — is what let me prove the approved files are untouched by
   identifier.
2. **Substitute rather than stall.** The alternative was to hand back nothing but a problem
   report. The property Codex demanded is real and now exists; the disagreement, if there is one,
   is narrow and named.
3. **Do not close the schema window in this card.** It needs a change to a component outside the
   agreed scope, and the guard I could have added inside scope would have been untestable.
   Measure it, pin it, disclose it.
4. **Leave the checkpoints fingerprinted from their path.** Nothing in this stage ever opens a
   checkpoint, so there is no second reading for a first one to have to match, and loading a
   large model file into memory to state a property nobody uses is cost without a claim.
5. **Flag my own changed tests.** In the previous round I said no test had been deleted or
   weakened. Three now are. Their subject — the bracket — no longer exists, so I named them
   explicitly rather than letting the net count hide it.

---

## Files created or updated

**Created**
- `Reproducibility Packet/scripts/utils/authenticated_storage.py`
- `Reproducibility Packet/tests/test_authenticated_storage.py`
- `agents/Claude/Session Summaries/HumanReport143.md` (this file)

**Updated**
- `Reproducibility Packet/scripts/utils/connection_adapter.py`
- `Reproducibility Packet/tests/test_connection_adapter.py`
- `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md` (Round-3 owner response appended, `+298/-0`)
- `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/…- Active.md` (one turn appended, `+124/-0`)
- `agents/Claude/README.md`
- `agents/Claude/Permanent Instruments.md` (lessons 246–250)
- `agents/Claude/Summary of Only Necessary Context.md`

**Built and then reverted whole** — `storage_contract.py`, `role_contract.py`,
`test_data_contract.py`, `test_role_contract.py` are byte-identical to their approved
baselines, confirmed by blob identifier.

---

## Evidence at the handed-off state

- Focused suite **184 passed**; under `python -O` **184 passed**.
- Packet-wide suite **2,792 passed, 0 failed, 153.24 s** — 2,764 + 8 + 20 exactly, which is what
  says this response adds tests and breaks none.
- Two-pass 28-mutant control: 25/25 real caught, 2 of 3 controls surviving, identical across both
  passes, no bad anchors, 380.1 s, entirely outside the repository, deleted afterwards.
- `py_compile` and `git diff --check` clean; `git status --porcelain` for the whole repository is
  exactly the four candidate files plus the two appended documents.
- Fresh-interpreter import check: `torch` and `mujoco` stay absent; only `numpy` arrives.

**No scientific resource was spent.** No role payload, checkpoint, estimator output, controller
log, production configuration or held-out result was opened; no MuJoCo model built, no rollout
stepped, no fit run, no figure rendered. The three approved artifacts were read as tracked JSON,
for their recorded code-identity field only, to establish the blocker. Counters stand unchanged at
**278 rollouts, 67 fits, 67 checkpoints, and zero pilot/validation/test reads**.

**Live-Run README:** the heartbeat check ran and correctly appended nothing. No artifact was
finished, no phase closed, and a build inside an open review round is none of the three triggers —
the standing ruling on this file.

---

## Next steps

1. **Codex's delta-only Round-3 review**, including its ruling on the substitution.
2. If it holds, **sub-step 4b-ii-b** — the remaining rows, the coherent geometry fixture, the
   audit-hook observer and the roles CLI wiring — under its own new card and its own new chat.
3. The schema second-read disclosure stays on the record for whichever round is entitled to close
   it, which needs a change to a component outside this card's scope.
