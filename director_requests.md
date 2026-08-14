# Director Requests

This file is the project's **single source of truth for work only the director (Randy) can do** — reviews that need his judgment, or actions that need his identity, login, or accounts. It is **append-only**: agents add entries, the director replies in place under an entry, and nothing is deleted or rewritten. When an agent hits director-only work it logs it here, names a fallback, and keeps moving so the project never stalls waiting. See `Playbooks/director-requests.md` for the full protocol.

**Format of each entry:** date · what's needed · why · what's blocked · fallback (what the agents do meanwhile). The director appends a brief reply line under an entry when he resolves it.

---

## 1. Claim Sheet ready for director review — *(non-blocking)*

**Date:** 2026-07-17 (logged by Claude, Session 5, at Phase 1 close)

**What's needed:** Randy's review of the project's now-agreed **Claim Sheet** — the contract both agents converged on in Phase 1. His review is the **first invocation of the amendment protocol**: he can approve it as-is, or propose changes (an amendment names what to change and why; it is appended and dated, never overwritten). By design this is **non-blocking** — the agents do not wait on it.

**The director-facing reading path (built for exactly this — you do not need to read the technical contract cold):**
- [`Accessible Claim Sheet.md`](Accessible%20Claim%20Sheet.md) — the plain-language companion: the same commitments, bounds, and success/failure shapes in ordinary language. Start here.
- [`Study Guide/Pass 1 - Conceptual Foundation.tex`](Study%20Guide) (+ compiled PDF) — the conceptual foundation written for you: what the question is, why it's hard, and the ideas you need to follow and judge Phase 2.
- [`Claim Sheet.md`](Claim%20Sheet.md) — the precise technical contract itself (fifteen slots), if you want the exact wording of any commitment.

**Why it's needed:** the amendment protocol makes the director's review the checkpoint that the agreed contract actually matches your intent for the project. The agents own execution from the approved contract, but this review is how you keep the work pointed where you want it — early, when a course correction is cheap. It is deliberately structured so your review can land whenever your schedule allows, without holding up the work.

**What's blocked:** **nothing.** This is non-blocking by design. Phase 2 (execution) is open and proceeding.

**Fallback / what the agents do meanwhile:** the agents proceed with Phase 2 against the agreed contract — Codex runs the bounded physics **feasibility spike** (the gate that decides the simulation path), and Claude builds the **sensor-realism + fault-injection model** and the **evaluation-harness skeleton** against the jointly-approved data schema (`Reproducibility Packet/schema/schema-v1.0.md`). If your review later lands an amendment, it is applied through the protocol — appended and dated, with any work it invalidates moved to a dated `archive/` folder rather than deleted, and corrections propagated forward — so nothing done in the meantime is wasted or silently overwritten.

*Awaiting director reply.*

---

## 2. MuJoCo's DLL is blocked by a Windows Application Control policy on the agents' desktop

**Date:** 2026-08-13 (logged by Claude, Session 128)

**What's needed:** an allowance on this machine for the MuJoCo binaries inside the project
virtual environment, so `import mujoco` works again. Measured this session:

```text
..\venv\Scripts\python.exe -c "import mujoco"
ImportError: DLL load failed while importing _functions:
An Application Control policy has blocked this file.
```

The blocked file is `venv\Lib\site-packages\mujoco\_functions.pyd` (and, on the evidence
of the import order, its siblings in the same directory). Resolving it needs an administrator
decision about this machine's Smart App Control / WDAC policy, which is why it is here rather
than in a chat: no agent can or should change a security policy.

**Why it's needed:** MuJoCo is the project's plant. Twenty-eight of the packet's test modules
import it transitively and now fail at collection, and a twenty-ninth test fails inside the
same import. Nothing about the project changed to cause this; the interpreter itself cannot
load the DLL. The immediate consequence for review is that **the packet's full-suite count
cannot be measured while the block is in force** - the number a reviewer normally checks a
session's work against is unavailable, not merely different.

**What's blocked:** every MuJoCo-dependent path - any rollout, any replay, any plant-touching
screen, and the full-suite test count. **Not blocked:** the current lane. The Slot-8
verification-scene work built this session imports neither `mujoco` nor `torch` by design
(invariant V18), and its two test files run green on their own.

**Fallback / what the agents do meanwhile:** the suite is run with
`--continue-on-collection-errors` and the result reported honestly with the block named, rather
than quoting a smaller number as if it were the suite. Measured this session at that setting:
**1,328 passed, 1 failed, 28 collection errors**, with every one of the 29 failures traced to
this single import. The Slot-8 lane needs no MuJoCo and continues normally; nothing in the
project's current open work depends on a rollout.

*Awaiting director reply.*

### Reply — Repair Agent, 2026-08-13 17:19 PDT: **RESOLVED, but not by anyone's intervention.**

*(Appended under entry 2 per the append-only protocol. The `*Awaiting director reply.*` line above
is superseded by this note and left standing as the record. I am the **Repair Agent** — a
separate agent Randy authorized for this specific machine problem, outside the Collaboration
Station workflow. I am not Claude or Codex and I hold no turn.)*

**MuJoCo works. The block cleared on its own.** Measured at 16:50–16:59 PDT today:

```text
full packet suite   2,267 passed, 0 failed, 0 collection errors  (164.20 s)
12 fresh interpreters, each import + build a model + step it     12 ok / 0 failed
```

**The true full-suite figure is 2,267.** Nothing in the project was wrong; nothing needed repair.

#### What it actually was

Windows **Smart App Control** (SAC) is on this machine in **enforcement mode**
(`VerifiedAndReputablePolicyState = 1`). SAC refuses to load unsigned native binaries whose cloud
reputation it does not yet recognise. In the project venv, **321 of 344 native binaries are
unsigned** — scipy (106), sklearn (69), pandas (45), torch (26), mujoco (22), numpy (19), OpenGL,
matplotlib, PIL, fontTools. MuJoCo is not special here; it was simply first.

From the Windows Code Integrity log (events 3033/3077, policy ID `{0283ac0f-…}`):

| Time (2026-08-13) | Event |
|---|---|
| 8/11–8/12 | Windows updates KB5123304, KB5120708, KB5121003 install |
| 14:31 | Defender fires a burst of cloud-reputation lookups |
| 14:33 | First block on `mujoco/_functions.cp312-win_amd64.pyd` |
| 14:33–16:23 | **397 block events**, every one naming that same single file |
| 16:24 onward | **Zero blocks.** MuJoCo imports, builds models and steps them |

The file never changed: still unsigned, still stamped 2026-07-16. A Windows update appears to have
prompted SAC to re-evaluate, and the binary was refused for roughly two hours until Microsoft's
reputation service vouched for it. **This was an environment fault with a beginning and an end, not
a project regression and not a permanent condition.**

#### What I did, and what I deliberately did not do

**Did:** diagnosed to root cause from primary evidence (the Code Integrity log and the CI policy
registry state) rather than from the error string; confirmed stability across 12 fresh interpreters;
measured the true suite figure; and built two tools at
`C:\Users\cresp\Documents\Dandelion Engineering\tools\` — **outside this repository**:

- `Check-NativeImportBlocks.ps1` — read-only. Reports SAC state, Code Integrity block events in a
  window and which files they name, a live import test of eight native packages, and a MuJoCo
  build-and-step probe. Exit `0` healthy/recovered, `1` a real import problem, `2` Application
  Control is blocking.
- `README-SmartAppControl.md` — the full timeline, the options, and what does **not** work
  (Defender exclusions are a different subsystem; reinstalling returns identical unsigned bytes;
  running as administrator does not bypass a kernel code-integrity policy).

**Did not:** change any security setting, install or reinstall anything, touch the venv, or modify
any project file other than this one. **Nothing is committed** — see the handoff note at the end.

#### The correction this owes the record

Sessions 128 and 129 measured the suite *while the block was active* and wrote the conclusion
**"the packet's full-suite count is unmeasurable"** into entry 2 above, both agents' session
reports, both continuity summaries, and the Phase-2 chat. Entry 2's own `1,328 passed, 1 failed,
28 collection errors`, and Session 129's `1,344 passed, 1 failed, 28 collection errors`, are
**artifacts of the block**. They are honest measurements of a broken environment and worthless as
measurements of the suite.

Those documents are append-only and dated, so **do not edit them.** Carry the correction forward the
way the project already handles this: the next session that has cause to state a suite figure states
**2,267** and cites this note. The Technical Report inherits the same obligation.

#### How to move forward

1. **Before treating any native-import failure as a bug, run the diagnostic.** It answers
   "environment or code?" in one run:
   ```
   powershell -ExecutionPolicy Bypass -File "C:\Users\cresp\Documents\Dandelion Engineering\tools\Check-NativeImportBlocks.ps1"
   ```
2. **A number measured during a block is discarded, not published with a caveat.** This is the part
   that went wrong. Re-run the measurement once the diagnostic reports healthy, and record the
   clean number. Reporting a degraded figure alongside a disclaimer still puts the wrong number in
   the record, where a later session will find it and quote it.
3. **Expect recurrence, and do not absorb it.** SAC remains in enforcement by the director's
   decision (below). Any unsigned binary here can be blocked again after a Windows update or a
   package install. **If this happens again — MuJoCo or anything else — append a NEW numbered entry
   to this file rather than working around it quietly.** Include the diagnostic's output. The
   director is deciding policy from the pattern of incidents, and an incident that is silently
   absorbed is one he cannot see.
4. **Do not propose turning Smart App Control off.** That decision is the director's and he has
   made it for now.

#### The director's standing decision

**Randy has decided Smart App Control stays ON for the present**, having been shown that the only
durable fix is to disable it, that doing so is irreversible without a clean Windows reinstall, and
that it would not disable Defender antivirus, cloud protection, SmartScreen or the firewall. **He
will reassess after the next incident.** That is the reason for instruction 3: each new entry is
evidence for a decision he has explicitly deferred, so log every occurrence.

#### Handoff — read before committing

This edit to `director_requests.md` is **uncommitted by instruction.** The next agent to run
**includes this file in its own session commit**; it does not get a commit of its own and the Repair
Agent does not commit. Also note: Codex's Session-129 run was **paused before it began any project
work**, and the `.agent-session.lock` it had already created was **stale** — the working tree was
clean and no commit followed `12c729f`. I removed that lock so the next scheduled session is not
refused by it. **`.agent-turn` is untouched and still reads `Codex`.**

— **Repair Agent** (authorized by Randy, 2026-08-13)
