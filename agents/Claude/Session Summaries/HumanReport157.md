# Human Report — Claude Session 157

**Current date and time:** 2026-08-18 19:19 PDT (read from the shell while writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

Codex reviewed my finished Slot-8 Step-4b-ii-b candidate last session and returned
**Revisions Required** with two blocking findings. This session is the Round-2 owner response.
**Both findings are integrated. Neither is contested. Both were reproduced at source before a
single line of the repair was written, and my re-drive of the second one found seven more
accepted states than Codex reported.** That makes nine consecutive sessions in which Codex found a
real defect in my work and I found none of its findings wrong.

The first finding is the interesting one, and it is worth stating plainly for a non-specialist
reader.

**The problem.** The verification artifact publishes a small set of files into a folder inside the
project's reproducibility packet. Before it publishes, it is supposed to prove that the folder it
is about to write into really is part of the packet whose contents it just checked — not some other
folder a caller pointed it at. For four consecutive sessions I have written a check for this, and
for four consecutive sessions Codex has broken it the same way. Each of my checks compared one
piece of the caller's own data against another piece of the caller's own data. If someone can
supply the whole bundle of data, they can supply a *consistent* fake bundle, and every such check
passes. Last session I thought I had ended it by making the check open the file on disk and hash
its bytes — something no in-memory value can fake. Codex's finding is one step past that: I
compared those real bytes against a *number that also came from the caller*. Change the file and
change the number beside it, and the check passes again.

**The fix.** The answer is not a better comparison; it is a different source of authority. The
function that actually does the authentication — the one that opens the record, the schema, the
configuration, the data files and the model checkpoints — now issues a small sealed object
recording what it really resolved: which packet folder, where the record sits inside it, and which
identity it authenticated. That object cannot be built by anyone using the module's public
interface, and the publishing step checks it against a private register of the ones this program
actually issued. The single line that ends the four-session pattern is that the publishing step now
takes the packet folder **from that sealed object** instead of from the caller's data. Both of
Codex's attacks are now committed tests, and both were confirmed to fail against last session's
code before I changed anything.

**The second finding** is smaller but the same species. Row 21 checks that every published figure
really is a PNG saved at 300 DPI, and last session I made that check quite thorough: the file
signature, every chunk's boundaries and checksum, the chunk order, every header field the format
defines, and the exact expected size of the compressed image data. Codex showed that a file can
pass all of that and still not be an image: a scanline can declare a filtering method the format
does not define, a palette-based image can omit the palette it cannot be drawn without, and a file
can carry an unrecognised chunk the format says a reader must not ignore. I reproduced all three,
then asked the standard what *else* makes a PNG renderable and found seven more the same check
accepted — including one I would not have found from the report alone: an interlaced image where
only the **seventh** pass carries the bad filter, which a check that stopped after the first pass
would wave through. The walk now reads the decompressed image data itself.

The candidate is handed back to Codex for delta-only Round 2. Step 4b-ii-b, all of sub-step 4b and
every downstream gate remain shut.

## What I actually did

1. Read `AgentPrompt.md` and `Project Details/Project Details.md` in full, my continuity file, the
   Review Card including Codex's complete Round-1 ledger, the subject chat, `Playbooks/review-cycle.md`,
   and Codex's `HumanReport156.md` (the cross-review requirement).
2. **Reproduced both findings at source, before repairing anything.** The Round-1 module was
   restored from the Git object store into a scratch tree outside the repository, and every probe
   was driven against it. All of Codex's states reproduced exactly.
3. Built the repair for finding 1 (`_AuthenticationWitness`, its issuance register, and the
   re-rooting of `_require_one_packet_root` and `_authority_output_root`).
4. Built the repair for finding 2 (`_png_pass_layout`, `_png_require_image_data`,
   `_png_reconstructed_scanline`, `_png_paeth`, `_png_palette_indices`, plus the critical-chunk and
   palette rules inside the chunk walk).
5. Wrote 34 net new tests, rewrote the accept control Codex ruled non-decisive, and updated four
   committed tests whose asserted refusal message moved when the anchor moved.
6. Ran a **two-pass mutation sweep** over the new guards, in a scratch tree outside the repository.
7. Wrote the Round-2 Review Card section, the subject-chat turn, the build-plan appendix, this
   report, and the closeout files.

## Challenges, and how they were resolved

**The finding that has no fixed point.** The hardest part of this session was recognising that a
fifth comparison would have been defeated a fifth time. The three-line history in my own continuity
file (S153 → S154 → S155) was the evidence, and Codex's finding added the fourth line. Once the
pattern is written out, the shape of the answer is forced: stop comparing fields, and get the value
from the function that did the reading. The bound on that claim is stated explicitly in the code,
the card and the chat — it closes the *public* interface, not a caller reaching into the module's
private names, because Python offers no defence against that and claiming one would be an
overclaim.

**A repair that changes what green means.** Re-rooting the check left the suite green while four
committed tests silently began asserting a *different* refusal than the ones they were written for.
Nothing went red, because every one of those states is still refused — the tests simply stopped
measuring what their names say. I found this by reading the failures the first run produced and
then re-reading every test near the anchor. The four are disclosed in a table in the Review Card,
each docstring now says which check it lands on and why, and the digest comparison that lost its
only exercise got a test of its own. That is this session's transferable lesson (295).

**A mutation sweep that was four times slower than it needed to be.** My first sweep ran ~3 minutes
per mutant against a suite that takes 25 seconds. The cost was pytest writing forty full tracebacks
through a pipe for every mutant that turns forty tests red — output the harness never reads, since
it checks the return code. I stopped the run, added `--tb=no -p no:cacheprovider`, re-staged a
clean tree and re-ran. Nothing about what the sweep measures changed; the mandated harness shape
(caches cleared, no bytecode written, no `-x`, exact bytes restored in a `finally`, two identical
passes required) is unchanged.

**A mutation sweep whose baseline was red, and the only thing that noticed.** The corrected sweep
then ran against a tree I had staged from memory instead of from my own build-plan note — I copied
the code, the tests, the schema and the config and left out the `results` directory, so the test
that drives the four tracked figures found none and **the suite was failing before the first
mutation was applied**. Seventeen mutants dutifully reported “caught” and every one of those
results was worthless. The only signal that anything was wrong was that all three *negative
controls* — deliberately harmless edits that must survive — also reported “caught.” That is
exactly what they are in the harness for. I threw the run away whole, re-staged the tree, required
the unmutated suite green first, and re-ran from the start; the good run then found three genuine
gaps in my own new tests, all three now repaired with fixtures rather than with more assertions.

## Decisions I made, and the three I handed to the reviewer instead

**Decided.** The witness seals five values and no more — root, record path, record identity, record
label, authority — because those are exactly what the publishing step derives its destination and
its scene identities from. The PNG reconstruction runs only for palette-based images, because the
index-range rule is the only remaining obligation that depends on the pixel values, and no figure
this packet publishes is palette-based; the real accept path pays nothing for it.

**Handed over rather than decided.** Three questions in this repair are judgements a reviewer
should settle, so I stated my lean, kept the state coherent, and said plainly I will take the other
ruling without arguing it:

1. whether the four coherence checks below the witness are now subsumed and should be deleted;
2. whether the witness is a protocol-level change to invariant W8 (I read it as how the
   implementation *holds* W8 rather than a change to it, and no invariant, CLI argument, read-order
   row or exit code moved);
3. whether the palette reconstruction is in scope for this card at all.

Offering those costs one paragraph and removes three possible round-trips. That is lesson 296.

## Verification

```text
test_connection_adapter.py                          389 passed          (Round 1: 355)
focused pair (adapter + authenticated storage)      409 passed / 24.50 s (Round 1: 375)
focused pair under PYTHONOPTIMIZE=1                 409 passed / 24.69 s
scene pair (verification_scene + render)            162 passed          (unchanged)
PACKET-WIDE                                       3,068 passed / 0 failed / 169.39 s
```

3,034 + 34 = 3,068 exactly. The four tracked Step-3 figures still pass the stricter PNG
walk, driven at source this session.

**Mutation sweep — run twice, twice.** The main sweep drove **20 mutants (17 real + 3 negative
controls)** against the module in a tree staged outside the repository, under the mandated harness
shape: caches cleared, `PYTHONDONTWRITEBYTECODE=1`, no `-x`, anchors translated to the target's own
newline, bad anchors reported separately, exact bytes restored in a `finally`. **Both passes
identical, 0 bad anchors, 932.1 s for the pair. 13 of 17 real mutants caught; four survived, and
three of those were real test gaps:**

| survivor | why it survived | repair |
|---|---|---|
| `palette_entries > permitted` → `>=` | every indexed fixture carried 4 entries at bit depth 8, where the bound is 256, so **the boundary the check is written about was never reached** | a fixture *at* the bound — a two-entry palette at bit depth 1, accepted, beside the three-entry one that is refused |
| the Paeth tie order → strict inequalities | the two orders agree on every input that is **not** a tie, and no fixture contained one — **and the test's own encoder called the module's predictor, so the round trip inverted itself** | the test encoder got an independent Paeth, a row pair that reaches the tie, and a direct table test pinning `_png_paeth(3, 6, 5) == 3` |
| the Average filter's `(a + b) // 2` → `(a + b + 1) // 2` | measured only through the palette-range check downstream of it, and the wrong indices happened to land inside a four-entry palette | the reconstruction is now asserted against its own inverse, byte for byte |
| the witness write guard's **message**, reworded | **this one is my own bad mutant.** It changes prose, not behaviour, so it is an equivalent mutant rather than a gap | retired, and replaced by a behavioural mutant that neuters `__setattr__` outright |

**The negative controls are the reason any of that is trustworthy, and they earned their place
this session.** An earlier run of the same sweep staged `scripts`, `tests`, `schema` and `config`
and **omitted `results`**, so `test_the_png_walk_accepts_the_tracked_step_3_figure_set` found zero
figures and the baseline was red before the first mutation was applied. Seventeen real mutants
dutifully reported `caught` and **every one of those results was worthless** — the only signal that
anything was wrong was all three negative controls reporting `caught` too. That run was discarded
whole, the tree re-staged with `results`, the unmutated suite required green, and the sweep re-run
from the start.

**Supplementary sweep, on the exact final bytes:** 6 cases (4 real + 2 negative controls), **both
passes identical, 284.5 s, 0 unexpected** — every repaired survivor now caught and both controls
surviving. The module is **byte-identical** to the tree the main sweep ran against (`diff -q`,
no output), so the main sweep's module results stand; the delta is entirely in the test file and
was measured by diff rather than asserted.

**Final position: 17 real mutants in their final form, 17 caught; 5 negative controls, 5
surviving.**

**Delta boundary.** Six of the eight candidate files are **bit-identical** to the Round-1
candidate — their Git blob ids are unchanged. The two that moved are
`scripts/utils/connection_adapter.py` (`c50b0a47` → `a5310110`, +583/-70) and
`tests/test_connection_adapter.py` (`b992982a` → `894feea7`, +726/-33). Both are pure ASCII, LF, 0
CR, no BOM, final newline present, checked on the final bytes; both blob ids were written into the
object store and resolved with `git cat-file -t` before the card was written.

**Chat append integrity.** The prior transcript measured 13,521 B / 226 LF / 0 CR, SHA-256
`2e9fa1fd5e7dd184eac42be9c5aa774230ec6d614b0bccc0dd02d2f93f85f3c2` — which independently confirms
every figure Codex published for its own append. My append was conditioned on that digest, written
prefix-then-payload as bytes, and both halves re-asserted after the write.

## Scientific boundary

**This session spent zero scientific resource.** No MuJoCo model was built, no rollout stepped, no
fit run, no checkpoint written, no figure rendered. The counters are unchanged at **278 rollouts,
67 fits, 67 checkpoints, and zero pilot / validation / test reads**. No role index, role payload,
checkpoint, estimator output, controller log or production configuration was opened. The one class
of read outside tracked development text was the **four tracked Step-3 fixture PNGs** under
`Reproducibility Packet/results/verification_fixture/`, opened for their chunk structure only, to
show the stricter walk still accepts real matplotlib output. Every probe and both mutation-sweep
passes ran in scratch trees outside the repository. The two off-limits identity files were neither
read nor edited.

## Public heartbeat

The root Live-Run README was checked and **deliberately left unchanged**. A Round-2 response inside
an open review is not a finished artifact, a closed phase or a public milestone — the same reading
that left it unchanged at my Round-1 handoff and at Codex's Round-1 block. The entry for this
sub-step belongs at its terminal outcome.

No progress report is due; my next regular one is Session 160.

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — the witness, the re-rooted anchor,
  and the PNG payload walk.
- `Reproducibility Packet/tests/test_connection_adapter.py` — 21 net new tests, the rebuilt accept
  control, and four updated refusal assertions.
- `Review Card/Slot-8 Step-4b-ii-b Coherence Geometry and Output.md` — the Round-2 owner response
  and the status line.
- `chats/Claude-Codex/Slot-8 Step-4b-ii-b Coherence Geometry and Output/Slot-8 Step-4b-ii-b Coherence Geometry and Output - Active.md`
  — the Round-2 handoff turn.
- `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` — Appendix K.
- `agents/Claude/Permanent Instruments.md` — lessons 294–298.
- `agents/Claude/Session Summaries/HumanReport157.md` — this report.
- `agents/Claude/README.md` — navigation and current state.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 158.

## Next steps

1. **Codex's Round-2 delta review.** That is the next work on this lane and it is not mine to do.
   If it has not arrived when my next session opens, there is nothing to do here — and **the
   candidate must not be edited while it is with the reviewer.**
2. If Codex rules on any of the three open questions above, apply the ruling rather than argue it.
3. Until same-state approval closes this card, Step 4b-ii-b, all of sub-step 4b, production
   connection records, real-role reads, Steps 4c–4f, capacity and threshold selection, the config
   freeze, and every C1-versus-S statement remain unauthorized.
