# Human Report — Claude Session 137

**Current date and time:** 2026-08-14 17:47 PDT (measured with the shell immediately before writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

**Outcome:** Codex blocked my Session-136 candidate with five findings. I accepted and integrated
all five, disclosed one scope expansion into a previously closed file for Codex to rule on, and
handed three states back for a delta-only Round 2. Nothing closed. No scientific resource was spent.

---

## 1. What this session was

My Session 136 built the first half of the Slot-8 Step-4b adapter — the connection-record contract
— and handed it to Codex for the only full-artifact review the director's new method allows. Codex
did two things in its Session 136: it accepted my proposal to split the 4b build in half, and it
returned a **numbered ledger of five blocking findings** and did not approve the candidate.

This session is the owner response to that ledger. Under the method, the owner answers the complete
ledger in one turn and names both what changed and what is provably unchanged, so the next round can
be a bounded delta rather than a re-read.

**The single most useful fact about this session, stated first because it is uncomfortable and
because it is the point:** my Session-136 candidate passed 212 focused tests, 212 again under
Python's optimized mode, a 2,479-test packet-wide suite, and a 44-mutant two-pass mutation control
before I handed it over. Codex's review found five real defects anyway, and **not one of them was a
state any of those instruments constructed.** Green suites establish that the code does what its
tests say. They establish nothing about the states nobody thought to write a test for. That is what
a reviewer is for, and it is why the review method matters more than the test count.

## 2. The five findings, and what each one actually was

I re-drove every one of them against the Round-1 bytes before repairing it, so what follows is
measurement rather than acceptance of someone else's report.

**Finding 1 — the record was authorized but not located.** The contract hashed the connection
record's bytes and refused anything that was not the authorized bytes, which is correct. It then
never asked *where those bytes came from*. The design gives a record exactly one tracked location
inside the packet, and a sibling rule that keeps the record's directory out of the directory the
adapter has to create fresh. Neither was enforced: a copy of the approved bytes anywhere on the
machine drove the whole read order. Related and worse, the list of files the adapter is allowed to
open left out the record itself — even though the adapter opens the record first. That would have
gone wrong later in a way that is hard to see: the next build compares "files allowed" against
"files actually opened" and requires them to be equal, so a correct adapter would have failed the
check, and the tempting fix would have been to quietly filter the record out of the observed side.

**Finding 2 — an authenticated record was still editable.** Python's `frozen=True` on a data class
prevents replacing an attribute; it does nothing about the contents of a dictionary that attribute
points at. Codex demonstrated this by swapping one arm's `plant` file reference for its `labels`
reference and by overwriting the record's own label, both after authentication, both successful.
The consequence is not theoretical: the whole design rests on "the allowlist is exactly what was
hashed", and a later stage could have bound a list that was not.

**Finding 3 — a number too large to be a number.** JSON integers have no size limit. A record
carrying `10**400` passed every check and then hit Python's float conversion, which raised a raw
`OverflowError` — a crash where the design specifies a named refusal and an exit code. A raw
exception out of a contract layer is a silent failure wearing different clothes.

**Finding 4 — the path rule refused traversal, not portability.** I had refused `..`, rooted paths,
drive letters and empty segments. I had not refused the spellings that mean different things on
different machines. I measured all four of Codex's claims on this machine before writing the repair:
an embedded null byte makes Python's path resolver raise before any containment check can run;
writing `schema.json:stream` succeeds and the directory afterwards lists only `schema.json`, because
the colon opened an invisible NTFS side-channel; writing `trailing.` produces a file that lists as
`trailing`, so two different record spellings name one file; and `CON` — a reserved device name on
Windows — resolves to a perfectly ordinary-looking path, which is exactly why a containment check
can never catch it. Separately, the output directory was compared for equality but never *proved* to
be inside the packet, so a link anywhere in the path could have redirected an accepted destination
outside it while every string in the comparison still looked right.

**Finding 5 — a record field that becomes a filename.** The verification surface writes one image
and one data file per case, named after the case's identifier. While every menu was built inside
this packet, that identifier was a key nobody outside could choose. The moment an external record
supplies it, `../escape` writes files *beside* the output directory instead of inside it — and the
manifest the run returns reports the innocent-looking leaf name, so the escape does not even show up
in the record of what was written. Codex drove this through the already-approved renderer and got
two files in the wrong place.

## 3. What I changed

All five are integrated. The record's own path is now bound and proved to be inside the packet, is
carried through to the allowlist, and is refused if it sits anywhere else — including inside the
output tree, under both authority modes. The parsed record is now immutable all the way down, with
every one of its eight nested mappings probed separately. The number conversion is guarded and
translates overflow into the named refusal. Every path component must now be one portable name, and
every resolution failure becomes a named refusal instead of a crash. And the case identifier must be
a single portable filename-safe token, with an independent containment check at the write boundary.

**One scope decision, which is the thing I most want a second opinion on.** That last containment
check lives in a file that was closed and jointly approved four sessions ago. Answering half of a
blocking finding seemed worse than widening the candidate; widening it silently seemed worse than
both. So I made the edit, named it in the Review Card and the chat as a **scope expansion**, and
offered the revert explicitly: if Codex rules the renderer belongs to the second half of the build,
that file goes back to its approved state and the requirement becomes a tracked item there. The
record-boundary half stands either way.

Because that file *produces a tracked artifact* — the ten-file figure set published in the
reproducibility packet — I did not argue that the edit was harmless. I regenerated the whole figure
set and compared every file: all ten reproduce at the same SHA-256, and the bundle digest is
unchanged.

## 4. The measurement that went against me, again

The focused suite was green at every step of this work. The mutation control — which deliberately
breaks the code one line at a time and requires the tests to notice — was not. On its first sweep it
reported **five survivors out of forty-seven**, and all five were real.

Two of them are the same lesson I wrote down last session, arriving again in the same session I
wrote it: a refusal test that asserts only the error *code* is satisfied by any later check that
refuses the same input for a different reason. I had written three tests correctly, with a specific
expected sentence per case, and then written a fourth with a bare code assertion — and two of its
branches could be deleted with the suite staying green. That rule is now unconditional in my notes:
a parametrized refusal test always carries the sentence, never just the code.

One survivor was a defensive copy that nothing observed. Two were guards that no well-formed input
can reach — which is the hardest kind to hold, because a guard nothing can break is a guard nothing
checks. Both are now driven directly, and one of them by a genuinely nasty little test: a Windows
directory junction that links *only* the record's subtree outside the packet, so every equality
check still passes and only the containment proof separates accept from refuse.

That test taught me something worth recording separately. My first version used a symbolic link,
which on Windows needs Developer Mode or administrator rights — neither of which this machine has —
so it **skipped**. Permanently, on the only hardware the project runs on. A junction needs no
privilege at all and behaves identically for this purpose. A test that always skips is worse than no
test, because the suite counts it and the report reads as coverage.

After the repairs: **47 of 47 real mutants caught, zero survivors, both deliberate no-op controls
correctly surviving, identical across both passes**, and both files restored to their exact
pre-sweep bytes.

## 5. Evidence

- Focused suite `tests/test_connection_record.py`: **311 passed** (was 212), and 311 under
  `python -O`.
- Packet-wide suite: **2,578 passed, 0 failed, 0 collection errors, 176.07 s** (was 2,479).
- Step-3 figure set regenerated at `--fixture-seed 7`: **all ten files byte-identical**, bundle
  SHA-256 `3bf51e94…` unchanged.
- Two-pass mutation control, 49 mutants (47 real + 2 negative controls), staged entirely outside the
  repository: **47/47 caught, identical across both passes, no bad anchors, digests restored**.
- `git diff --check` clean. Diff: `+338/−43` module, `+707/−4` tests, `+66/−4` renderer.
- Byte-identical to `HEAD`, verified with `git hash-object` against `git rev-parse HEAD:<path>`:
  `verification_scene.py`, both Step-2/3 test files, the packet README, the public README, both
  `.gitattributes`, both `.gitignore`, and the approved Step-4a design.

## 6. Cross-review, and a correction I owe

I read Codex's HumanReport136 in full. Its non-blocking observation is **correct and I accept it**:
my HumanReport136 file list omitted `agents/Claude/Permanent Instruments.md`, which that session
changed by 25 lines. I verified it myself with `git show --stat 0bf316e`. The Session-136 report is
dated and stays as written; the correction propagates forward, this report lists every file, and I
have added the check to my own closeout.

I also found a stale clause in my own continuity file and corrected it: it named the public README's
blob and banner date from Session 130, but Codex moved that file in its Session 135 to add a dated
log entry. I read the entry as part of this session's recent-work review — it is accurate and it is
the lean shape the playbook asks for, so I have no correction to carry on it. The stale clause is a
recurrence of a failure this project has recorded before, and both times the rotten clause described
*another agent's* change to a file I index.

## 7. Live-run README heartbeat

Checked, and correctly appended nothing. No artifact finished, no phase closed, and a candidate
inside an open review round is none of the three triggers the playbook names. The banner is current
at 2026-08-14.

## 8. Preserved boundaries

This session opened no role index, role payload, checkpoint, estimator output, controller log,
configuration or split result; built no MuJoCo model; stepped no rollout; ran no fit; and wrote no
configuration, connection record or production output. Every path the new tests bind names a file
that does not exist, under a temporary directory. The one figure render was a reproduction of an
already-approved artifact into a git-ignored directory, purely to prove the renderer edit moved no
published byte. Counters are unchanged at **278 rollouts, 67 fits, 67 checkpoints and zero
pilot/validation/test reads**.

## 9. Files created or updated

- `Reproducibility Packet/scripts/utils/connection_record.py` — the five repairs (+338/−43).
- `Reproducibility Packet/tests/test_connection_record.py` — 99 new tests and four sharpened
  assertions (+707/−4).
- `Reproducibility Packet/scripts/render_verification_scene.py` — the disclosed scope expansion:
  one write-set containment helper and its call site (+66/−4).
- `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md` — Round-2 owner response, new
  candidate identities, five acceptance criteria added from the ledger, scope expansion recorded.
- `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/… - Active.md` — the owner
  response turn (+151/−0, prefix and payload both asserted).
- `chats/Claude-Codex-Human/Review Boundary and Convergence/… - Active.md` — one method data point
  and the scope-expansion question, for the director and Codex (+46/−0).
- `agents/Claude/Permanent Instruments.md` — standing lessons 225–228 and a recurrence note on 223.
- `agents/Claude/README.md` — the Step-4b-i bullet and the chats bullet.
- `agents/Claude/Summary of Only Necessary Context.md` — head block rewritten for Session 138,
  counters, suite figures, and the corrected public-README clause.
- `agents/Claude/Session Summaries/HumanReport137.md` — this report.

## 10. Next steps

1. Codex reviews the delta only: the five closures, the scope-expansion ruling, and any regression
   this response introduced.
2. If Codex approves the same three states, the first half of the build closes and I open a new card
   and chat for the second half — rows 4 through 21, the coherent geometry fixture, the audit-hook
   observer and the remaining acceptance tests. **The build sub-step does not close until that half
   closes too.**
3. If Codex rules the renderer belongs to the second half, one file reverts and the requirement
   becomes a tracked item there.
4. Round 3 would be the last one under the limit, and the limit never forces approval.
5. A production connection record, any real-role or scientific read, a capacity or threshold choice,
   a frozen configuration and every run remain separately blocked and unauthorized.
