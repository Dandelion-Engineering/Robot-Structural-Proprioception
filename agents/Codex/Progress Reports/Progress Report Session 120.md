# Progress Report — Codex, Session 120

**Written:** 2026-08-11 11:14 PDT
**Covers:** my Sessions 113–120 (previous regular report: Session 112)
**Phase:** 2 — Execution, with limited Phase-3 packet assembly
**Written for:** Randy

---

## The short version

The previous report ended with a reviewed design for the project's second learned-model rung.
This eight-session stretch turned that design into a real development run, but kept every step
separate: architecture, executable, zero-fit plan, fitting authorization, read-only analyzer,
exact result review, and interpretation each had its own gate.

The run completed successfully as an engineering operation. It fitted ten second-rung model arms
and reproduced two approved first-rung arms exactly. A separate reader then authenticated and
re-scored the saved checkpoints. Both agents independently audited the same final analysis bytes
and jointly applied the two sentences the pre-registered interpretation permits.

The scientific picture is much less flattering, and that is the important result to carry
forward honestly. Every second-rung arm scored zero [F1](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)
on the `healthy` and `structure` classes. Four of ten arms sat exactly at the majority-class
baseline; the other six learned some `actuator` discrimination, while all ten retained non-zero
`sensor` F1. The pre-registered optimization check still passed because the total training
objective fell, but that check was deliberately weak and never promised classification learning.

The licensed interpretation is therefore narrow:

> Slot 9's rung 2 is built and fitted; the ladder has more than one rung on it, and the
> development record contains one rung-2 fit at five seeds under the approved protocol.

> At rung 2, in-sample, the paired sign was not consistent across the five seeds.

Those sentences describe what was built and the signs of five paired development values. They do
not select a model, explain the zeros, compare C1 with S scientifically, establish generalization,
or authorize a held-out read.

## The idea that matters: a successful run can still reveal an unusable model

There are two different questions here:

1. Did the machinery perform the experiment it was designed to perform?
2. Did the resulting model learn the distinctions the project ultimately cares about?

The answer to the first is yes. The executable followed the frozen plan, used only development
rows, reproduced its two first-rung equivalence checks bit-for-bit, fitted all ten declared arms,
and stayed inside its exact resource budget. The analyzer then reloaded the saved weights and
required the new scores to match the recorded scores exactly.

The answer to the second is not yes. The second rung collapsed two classes completely. This is
why the project did not define success as “the loss went down.” The combined training objective
contains several terms, including a Gaussian severity term whose scale can improve while class
predictions do not. The frozen design explicitly says that objective reduction is not a learning
signal. This run is the concrete case that warning was written for.

That distinction is useful beyond this model. A pipeline can be reproducible, deterministic and
correctly executed while producing a disappointing scientific object. Good engineering makes the
disappointment trustworthy; it does not turn it into success.

## What happened in Sessions 113–120

### 1. The architecture and its tests closed

Claude implemented the 219,018-parameter recurrent-plus-attention network described by the
approved design. It combines a causal convolutional stem, a two-layer
[GRU](https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html), and a single-head temporal
attention pool. It is about 5.5 times the size of the 39,594-parameter first rung, but it also has
a much shorter stem receptive field. The two rungs therefore differ in architecture, capacity and
temporal reach at once; they are not two clean points on a one-variable curve.

Codex approved the module unchanged but found two blind spots in its tests. One test proved that
gradients reached every stage without proving that the stages were in the approved order. The
other used a substitute scorer instead of the real capacity-sweep seam. I repaired the tests,
Claude genuinely re-reviewed the changed bytes, and the module/test loop closed.

### 2. The executable and zero-fit plan closed separately

The fitting executable was reviewed as its own state. It claims a fresh run root atomically,
authenticates the approved first-rung records, performs two equivalence refits before any
second-rung arm, and refuses replay into an occupied namespace. The exact executable/test state
closed before plan mode was allowed.

Plan mode then wrote one canonical JSON description of the ten rung-2 arms, two equivalence arms,
their output paths, authenticated inputs and maximum spend. Codex audited that artifact with 107
independent checks and approved its exact digest. Only after both agents approved the plan did the
project consider an execution authorization.

### 3. One fitting invocation was authorized and spent

Both agents posted matching authorization halves naming the same plan digest, run label, output
base and maximum budget. The exact execute command ran once.

It reached `X_RUNG2_OK` after 1,274.6 wall-clock seconds:

```text
fits / checkpoints              12 / 12
rung-1 equivalence arms          2 / 2 PASS
rung-2 completed arms           10 / 10
simulator generation runs        0
physical rollouts                0
non-development reads            0
```

The recurrent model's synthetic timing probe was roughly 12 times slower per optimizer step than
rung 1 on this CPU despite having 5.5 times the parameters. Recurrent timesteps do not parallelize
like a dilated convolutional stack. That is an efficiency result about this architecture on this
hardware, not a reason to discard the run after seeing its outcome.

The two authorization halves are spent. There is no replay or retry authority.

### 4. The read-only analysis and exact-state review closed

Claude built a separate analyzer that fits nothing. Codex reviewed and approved its code and
tests before any production invocation. The agents then supplied two exact authorization halves
for one read into one fresh output directory.

The reader reached `X_ANALYSIS_OK`. It authenticated the plan, raw run, equivalence record,
approved fit ledger, approved first-rung analysis, design and code identities; then it re-scored
the saved checkpoints and wrote one canonical JSON artifact.

Claude audited and approved that artifact. Codex independently audited the same bytes with a
standalone 853-check instrument that imported nothing from the producer. The audit initially
refused twice because Codex's instrument used the wrong line-ending hash domain and a subtly
different floating-point sample-standard-deviation implementation. After those instrument defects
were corrected, all 853 checks passed. Neither refusal was an artifact defect.

Both agents now explicitly approve the same analysis blob.

### 5. The interpretation closed, then the runbook review found one forward correction

Codex and Claude independently re-derived the ordered status and the five paired signs, then
applied the same two frozen sentences. Section 5.4 is now jointly closed.

Claude added two consecutive rung-2 steps to the packet runbook and corrected its checkpoint
census from 55 to 67. Codex accepted the decision not to print the two rung-to-rung differences,
accepted the 67-checkpoint correction, and accepted the new Current-boundary paragraph.

One sentence said that the six non-baseline arms had non-zero actuator F1 “and nothing else.”
That was false because every arm also had non-zero sensor F1. Codex corrected the packet forward
to the exact record and explicitly approved the new blob. Claude owns the runbook, so its genuine
same-state re-review remains open.

## What was unexpected

- The larger recurrent-attention architecture passed the deliberately weak optimization check
  while completely missing `healthy` and `structure` on every seed.
- Four arms reproduced the majority-class predictor exactly at the recorded six-decimal metrics.
- The other six were not actuator-only classifiers; every one also retained sensor F1. That small
  wording distinction mattered because the runbook is supposed to let an outsider reconstruct
  the result without opening the JSON.
- A full text patch can preserve a Git additions-only diff while changing working-tree bytes on a
  mixed-line-ending transcript. The durable append mechanism now carries the whole asserted prior
  file as the literal prefix, not merely as patch context.

## What is working

- The gate sequence prevented an architecture implementation, executable approval, plan approval,
  fit, analyzer and interpretation from collapsing into one “looks good” decision.
- Independent instruments are allowed to fail, and their failures are diagnosed rather than
  quietly tuned until they pass.
- The saved analysis is canonical, self-authenticating against named inputs, and independently
  reproducible at the arithmetic level.
- The packet now tells the uncomfortable model story directly instead of letting a successful
  terminal code or falling objective stand in for learning.
- The public Live-Run README remains lean: it is waiting for one jointly approved packet-runbook
  state rather than logging an intermediate review blob.

## What is not working or remains open

- The second-rung classifier is degenerate on two of four classes. No cause has been established.
- Capacity, rung, probability threshold and abstention threshold remain undecided and owned by a
  later validation process, not by this development read.
- Pilot, validation and test outcome roles remain unread for those decisions.
- The final immutable `config/config.json` is absent.
- The 67 Git-ignored checkpoint files still lack an authenticated clean-machine recovery or
  distribution path. The tracked JSON records are auditable without them, but the packet cannot
  yet reproduce the checkpoint-dependent reads from a clean clone.
- Claude's owner re-review of packet README blob `7c9f394d...` remains open. The public interpreted
  heartbeat waits on that exact same-state approval.
- `director_requests.md` entry 1—the non-blocking Claim Sheet review—remains open. No new director
  action is required for this review loop.

## Verification artifact

The Slot-8 hands-on verification artifact did not change in this interval. The rung-2 work is an
internal development result and packet-runbook extension, not the final interactive verification
path. No update is manufactured here.

## What happens next

1. Claude re-opens the reviewer-edited packet README and either explicitly approves blob
   `7c9f394d...` or edits and returns a new state.
2. Once one exact runbook state has both approvals, the public Live-Run README can receive one lean
   interpreted-rung-2 heartbeat.
3. Any attempt to explain the zero-class result or design a next experiment begins as a new,
   reviewed design. Nothing in this run authorizes a retry or a held-out read.
4. Capacity, thresholds, final configuration and confirmatory work remain behind their existing
   gates.

The important state is simple: the second rung exists and ran correctly; its classifier did not
learn two classes; the project has not pretended those are the same question.

— Codex
