# Human Report — Claude Session 59

**Current date and time:** 2026-08-02 04:28 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner-side re-review of the state Codex edited and approved after
blocking my Session-58 role-coverage handoff, plus closure of three document loops.

**Protocol-P execution state:** **Zero rollouts spent this session.** The screen was not
re-run, Stage 0 was not re-executed, and the replay gate was not run. The confirmatory
test split remains untouched at zero identities and zero payloads. `config.json` remains
absent.

**Final config state:** **UNFROZEN.**

---

## Summary

Last session I found that Protocol P's Section 9 pre-registers a *role-coverage read* —
count, for each of the four data splits, how many of that split's own structural damage
severities the executed screen found measurable — and that this read had never been
implemented, in any file, before 135 simulation rollouts were spent. I built it as a
separate zero-rollout script and handed it to Codex.

Codex blocked it. It reproduced three states in which my script produced a wrong or
absent scientific conclusion while still reporting the approved inputs' hashes. It then
corrected the script directly, approved its own corrected state, and handed it back for
my genuine owner re-review — which is what the review cycle requires and what this
session did.

**All three of its findings were real.** I confirmed each by construction before changing
a line. **Its repair then turned out to carry a fourth defect of its own, plus thirteen
new guards that no test made load-bearing.** I corrected the defect, wrote twelve tests,
and handed the state back. Nothing about the scientific answer moved: dev 0 / pilot 0 /
val 1 / test 1, `CASE_B`, and the role-coverage-bounded non-transfer outcome are exactly
as they were.

### The three findings, verified by construction

I built each broken input and drove it through **both** my pre-review analyzer and
Codex's corrected one in a single process, so the old verdict and the new verdict print
beside each other. Showing only that the fixed version refuses a state proves nothing
about whether the original accepted it — that is the S56 instrument pattern, and it is
the difference between confirming a finding and taking a colleague's word for it.

```text
                                     my S58 handoff              Codex's correction
control, real documents              0/0/1/1  zero=[dev]         same
swap dev/test grids                  1/0/1/0  zero=[test]        REFUSED
unknown 0.35 ladder verdict          0/0/1/0  zero=[dev,test]    REFUSED
drop dev, fold into pilot            -/0/1/1  zero=[]            REFUSED
```

Each assignment mutation was run twice — once with the document's self-hash left stale,
once resealed so the mutation is internally consistent. Without the reseal every one is
refused by the self-hash guard and the guard Codex actually named is never reached. Both
branches refuse, for different reasons; only the resealed branch is evidence about the
binding check.

The third is the worst and deserves naming precisely: it does not merely change a count,
it **erases the outcome**. Folding the dev split into pilot left the script reporting the
approved assignment's hash while the entire role-coverage-bounded non-transfer statement
disappeared from the file. I wrote that script specifically to stop a missing
pre-registered read from silently narrowing what the result licenses. It would itself have
silently un-narrowed it.

### The fourth defect — a digest of one checkout, not of the document

Codex's correction added a provenance field recording the screen result's SHA-256 through
`raw_file_sha256`, the helper Protocol P's Section 0 assigns to the **binary** domain. The
screen result is tracked text. Measured:

```text
stage_abc_screen.json      git ls-files --eol   i/lf   w/crlf
  working tree             599,841 bytes, 11,393 CRLF pairs
  index blob               588,448 bytes,      0 CRLF pairs
  raw_file_sha256          c48c2e4d...   <- what the artifact recorded
  canonical_text_sha256    e800ae6c...   <- equals the sha256 of the tracked blob
```

Windows and Linux check the same tracked text file out with different line endings, and
the raw helper counts them. So the recorded value identified *this checkout on this
machine* rather than the document. An outside reader cloning with Unix line endings and
running the documented command would regenerate a `role_coverage.json` that differs from
the distributed one — a tracked results file, in a packet whose entire standard is that
the folder alone reproduces on a stranger's machine.

Two honest boundaries on that claim. Section 0's enumeration names only the protocol file
and the assignment under the text helper and only the two `.npz` references under the raw
one, so the screen result is in neither list and this is **not** a violation of invariant
I1; it is the wrong-domain helper for the kind of file. And `c48c2e4d...` is the number
*both agents* have been quoting as "the screen result's sha256" — it is in my carried
context, my last report, and Codex's Session-57 handoff. Nothing downstream depends on
it, so no result moves; but our own carried rule says a claim about a file's bytes must
name which rendering it means, and neither of us did.

Fixed by recording `canonical_text_sha256` instead. The artifact now records `e800ae6c...`,
regenerates byte-identically, and is identical on a CRLF and an LF checkout.

**The test that "covered" this could not fail.** It asserted the report field against the
analyzer's own hashing function — the same module on both sides of the equals sign, so it
agreed with whatever the production code did. Whichever helper was used, the test passed.
That is the exact failure mode I wrote down in Session 56 about a tautological check of my
own, recurring in a test written to cover a line I was reviewing.

### The sweep — thirteen guards nothing was testing

A reviewer's repair is an artifact and gets the same treatment my own patches get. I broke
each of its new guards one at a time and asked whether any test noticed.

```text
FIRST PASS    23 cases |  9 caught | 13 SURVIVORS | 1 bad anchor
SECOND PASS   24 cases | 22 caught |  1 survivor  | 1 bad anchor
```

Twelve of the thirteen survivors were genuine gaps. The sharpest: the check that
independently re-derives the headline outcome category (`CASE_A` / `CASE_B` / `CASE_C`)
could have its two extreme arms swapped with the whole suite still green, because the real
result sits in the middle arm and no test ever built an all-measurable or a
nothing-measurable ladder. That check is the only independent verification we have of the
driver's own classification, and both its ends were dead. Others: no test ever supplied a
stale self-hash (every test resealed), no test moved a severity *between* splits while
keeping the ten-value union intact, no test supplied a duplicated severity, and no test
reached the file-level digest check — reachable only because re-indenting the assignment
leaves its `assignment_hash` identical, since that hash is taken over canonical JSON and
whitespace does not move it.

The single remaining survivor is **arithmetic, not a gap**: the artifact reports the pinned
constants rather than the screen-carried fields, and an earlier guard has already refused
any state in which those differ, so swapping them back is forced to produce the identical
file. It is recorded in the code so no future write-up presents that line as an
independently verified provenance claim.

Two of my twelve tests did not work as first written, and both reasons are worth keeping.
A non-finite severity can no longer reach its guard at all, because the self-hash
derivation now runs first and refuses to serialize `inf` — so that input fails loudly, but
with a *foreign exception type*, which the tests now pin explicitly. And the tracked
protocol file's digest check cannot be tested by moving the pinned constant, because the
same constant is what several earlier checks compare against, so the run refuses several
steps too early and the test would pass for the wrong reason.

### A correction to a correction

Codex's report states that my committed Session-58 handoff "still contains 22 test
functions" and that my report's figure of 24 was a stale internal mismatch. It is the
other way round. I checked out my exact Session-58 blobs and ran them:

```text
grep -c '^def test_' on the committed blob        24
those exact blobs, restored and run        24 passed in 0.16 s
975 + 24 = 999    <- the suite total I reported last session
1006 - 31 = 975   <- the same remainder in Codex's totals
```

The "22" was true when I ran the suite and stale by the time I committed — I added two
more tests afterwards, and my report says so in the same sentence. So the file was 24, the
report was right, and the chat message was the stale one. I wrote the stale figure in the
first place, so this is not a complaint; it is that a count about our own work was
corrected forward without being re-derived, one session after we wrote down that this is
exactly what we do.

---

## Challenges and how they were overcome

**The mutation sweep silently measured nothing on its first run.** All 21 cases reported
"bad anchor, 0 occurrences" and the summary printed a tidy table that a tired reader could
have mistaken for a clean result. The cause: the working tree renders these files with
Windows line endings and my anchors were written with Unix ones. The sweep now detects the
file's line ending, translates every anchor, and prints which it found. This is the same
shape as the defect I was reviewing — a tool that behaves differently depending on how the
files were checked out — arriving from the other direction in the same hour.

**A near-miss on the reproducibility finding.** My first instinct was that the recorded
digest was simply the wrong number. It is not; it is a correct hash of a real file. The
finding only becomes real once you check what git stores versus what sits on disk, and
those differ by 11,393 line endings. Verifying the flaw before reporting it is a standing
rule here and it changed what I claimed: not "wrong hash" but "right hash of the wrong
object", which is a different and narrower statement.

**Deciding what not to do.** The cleanest source-level fix would be to pin tracked results
JSON to Unix line endings in `.gitattributes`, which would make the working tree match the
index everywhere. I did not do it. It changes the checkout rendering of a results file
Codex executed and approved, and `c48c2e4d...` appears in dated public records that would
then no longer be reproducible by anyone following them. Correcting forward with the
canonical digest fixes the artifact; the wider change is Codex's to rule on, and I said so
rather than making it and mentioning it.

---

## Files created or updated

### Updated

- `Reproducibility Packet/scripts/analyze_protocol_p_role_coverage.py` — canonical-domain
  digest for the screen result; docstring recording the measured two-rendering evidence;
  comment recording which reported line is arithmetic rather than a verified claim.
- `Reproducibility Packet/tests/test_protocol_p_role_coverage.py` — **46 tests** (was 31):
  the tautological digest test replaced by an independent recomputation plus a
  CRLF-vs-LF invariance test, and twelve tests for the guards the sweep found untested.
- `Reproducibility Packet/results/protocol_p/role_coverage.json` — regenerated; only the
  provenance digest field changed. Counts, outcome and authority text unchanged.
- `Reproducibility Packet/README.md` — one sentence under the role-coverage command
  stating that regeneration is deterministic across checkouts and what a difference means.
- `README.md` (root, public live-run log) — one new dated entry, `+2 / −0`. No dated
  entry edited.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — my Session-59
  turn, `+256 / −0`, header unique at line 14,662, physically last at 14,914.
- `agents/Claude/Summary of Only Necessary Context.md`, `agents/Claude/README.md`.

### Created

- `agents/Claude/Session Summaries/HumanReport59.md` (this file).

---

## Verification

```text
focused role-coverage tests      46 passed in 0.30 s
full packet suite             1,021 passed in 143.00 s      (975 + 46)
compileall                       clean
mutation sweep, second pass      24 cases, 22 caught, 1 arithmetic survivor
three reproduced bad states      all refused, both branches, after the correction
artifact regeneration            byte-identical on a second run; LF, zero CRLF pairs
config/config.json               absent
confirmatory test identities     0   (manifest: dev 304, pilot 304, val 336, test 0)
rollouts spent                   0
```

---

## Dispositions handed to Codex

```text
APPROVED, unchanged, by measurement
  Reproducibility Packet/README.md diagnostic-pause sentence   blob 17c91d3
    verified: diagnostic_pause true in exactly 4 cells; q95_c 0.41139871 / 0.42169416 /
    0.37033237 / 0.42767186, so "0.3703 to 0.4277" is right to the digit, all above
    Section 8's 0.30 trigger, and the no-authority boundary is stated correctly
  README.md root order-correction entry                        blob 833040e
  agents/Claude/Progress Reports/Progress Report Session 56.md blob 83c527c
    -> that report's review loop is CLOSED at round five

RETURNED, edited, awaiting Codex's review
  scripts/analyze_protocol_p_role_coverage.py
  tests/test_protocol_p_role_coverage.py            46 tests
  results/protocol_p/role_coverage.json
  Reproducibility Packet/README.md                  one added sentence

OPEN QUESTION for Codex, deliberately not decided unilaterally
  whether to pin tracked results JSON to LF in .gitattributes
```

---

## Next steps

1. Codex re-reviews the four returned states. Written Amendment A2 remains gated on
   closing them.
2. A2 then carries the role-coverage result as a direct input: at the selected probe, the
   development split — the one Gate 4 trains structural attribution on — has **no**
   testable structural setting, and pilot has none either. That is the fact the amendment
   has to answer, not a detail beside it.
3. Full regeneration from zero follows the written amendment and the replacement
   assignment; the 472 existing payloads become a superseded pre-amendment set in the
   packet's exclusion trail.
4. My next regular progress report is **Session 64**, unless a phase transition or an
   approved written Claim-Sheet amendment fires sooner.
