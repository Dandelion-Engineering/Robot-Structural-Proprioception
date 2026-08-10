# Codex — Human Report, Session 107

**Date and time:** 2026-08-10 06:08 PDT

**Phase:** Phase 2 — Execution, with limited Phase-3 packet assembly

**Progress-report session:** No. The next regular Codex progress report is Session 112 unless a phase transition or approved Claim Sheet amendment fires one sooner.

---

## Summary

Claude Session 107 approved Codex's packet-local `.gitignore` blob unchanged, closing the
Findings AY/AZ/BA loop. Claude then found Finding BB: the repository's three end-of-line rules
all governed packet files but existed only in the repository-root `.gitattributes`, so they
would not travel when `Reproducibility Packet/` is copied or published as its own repository.
One rule is load-bearing: a Windows checkout without the schema pin changes `schema.json` from
LF to CRLF, changes its raw SHA-256, and makes the packet's first validation command refuse.

I genuinely reviewed Claude's new `Reproducibility Packet/.gitattributes`, reproduced the
positive and negative Windows checkout behavior in isolated Git fixtures, ruled on Claude's two
explicit questions, and approved the exact handed-off blob unchanged. The Finding-BB review loop
is closed at blob `76976c108853b5a9ff6712b8e5aac4345606f0bb`.

This was packaging/documentation review only. No scientific or executable state moved. Stage 1
remains complete as scoped; capacity selection, Stage 2, later-role reads and final configuration
remain unauthorized.

## What was accomplished

### 1. Closed the packet-ignore review loop

Claude independently rebuilt the runbook destination census, accepted Codex's Step-20
`/results/sensor_model/` rule unchanged, and explicitly approved the exact packet-ignore blob
Codex approved:

```text
Reproducibility Packet/.gitignore
  Git blob                 5082c2fc2c2277eef586c442b50a52881f6e5c95
  raw SHA-256              5120235af01356adac29a32424d2a6e18dde4ff1b3ac80dd1338b99aabbdee64
```

The packet-ignore loop is therefore closed. Its ten rooted scratch-output rules travel with the
packet, and Claude's fresh packet-only replica found no missing untracked runbook destination and
no tracked file swallowed by the packet rules.

### 2. Reviewed Finding BB and its exact implementation

The repository-root `.gitattributes` had three packet-scoped rules:

```text
Reproducibility?Packet/schema/schema.json text eol=lf
Reproducibility?Packet/config/proposed-gate3-assignment-v0.1.json text eol=lf
Reproducibility?Packet/protocol/*.md text eol=lf
```

Those rules work in the full repository but do not travel with a packet-only publication, and
their prefixes would not match a worktree rooted at the packet even if the root file were copied.
Claude added a packet-local file with the same three rules re-rooted:

```text
schema/schema.json text eol=lf
config/proposed-gate3-assignment-v0.1.json text eol=lf
protocol/*.md text eol=lf
```

I verified the exact file state:

```text
Reproducibility Packet/.gitattributes
  Git blob                 76976c108853b5a9ff6712b8e5aac4345606f0bb
  raw SHA-256              b1b549992d7f791caddf1e529d07626a121ed94b19ca63c06588b2be52627600
  size / encoding          1,693 B / ASCII UTF-8 / LF / no CR / no BOM / final newline
```

All three path classes resolve to `text: set / eol: lf`. The protocol pattern covers all three
tracked protocol Markdown files, which are direct children of `protocol/`.

### 3. Reproduced the load-bearing Windows behavior

I built two minimal Git repositories outside the project from the tracked schema and draft
config, then cloned each with `core.autocrlf=true`.

With the packet-local `.gitattributes` present:

```text
schema checkout             15,212 B / 0 CR / 670 LF
raw SHA-256                 0dae0dd0fec4269180139efc9a4c9ce38e7f8f23d890d182dc8eb063803e942f
Step-1 validator            exit 0 / status=draft / confirmatory=False
effective schema attribute  text=set / eol=lf
```

Without any `.gitattributes`:

```text
schema checkout             15,882 B / 670 CRLF
raw SHA-256                 b11fd1d8c3859aa17c29af097df4f0007584fd3fe8c125750cbe2b01d8387f14
Step-1 validator            exit 1 / configuration schema_sha256 does not match schema.json bytes
effective schema attribute  unspecified
```

This independently reproduces Claude's measurement and the exact refusal path at
`scripts/utils/config_contract.py:216`. Both temporary fixtures were removed after verification.

### 4. Ruled on duplication versus movement

I approved duplication and did not edit the repository-root file.

- The packet-local file is the portable authority for a packet-rooted publication.
- The existing root file remains a settled full-repository policy surface.
- In the nested full-repository checkout both files set the same values, so there is no conflict.
- Removing the root rules would be behavior-neutral today, but it would reopen a separately
  settled file without any requirement to do so.

The AY ignore-file precedent does not require a root-file edit here. The defect is cured by the
new portable file, and the exact current state is narrower than a governance reopening.

### 5. Ruled on the two defense-in-depth rules

I approved keeping the assignment and protocol pins. Those files are checked in a canonical
text domain that already folds CRLF to LF, so the rules are not needed to prevent a gate refusal.
They nevertheless preserve the packet's `raw_equals_canonical` diagnostics, agree with the
settled root policy, and are scoped narrowly to one assignment file and direct protocol Markdown
children. They add a useful portable invariant without broadening scientific or execution
authority.

## Verification

```text
exact packet-attribute blob             76976c108853b5a9ff6712b8e5aac4345606f0bb
all three effective attributes          text=set / eol=lf
protocol pattern coverage               3/3 direct Markdown children
isolated packet-rooted Windows clone     schema LF; Step-1 validator accepted
isolated no-attribute negative control   schema CRLF; Step-1 validator refused
pinned file working-tree bytes           LF-only
git diff --check before closeout          clean
packet test suite                         not repeated; no executable/content edit
```

Claude ran the full 1,792-test packet suite on the exact handed-off blob. I did not repeat it
because this review changed no packet file and the decision-bearing check was Git checkout and
attribute behavior.

The first combined fixture harness treated the expected negative validator traceback as a
PowerShell native-command error and stopped after the positive branch. I did not treat that as a
test failure or a negative-control result. I reran the no-attribute branch with stderr captured
as data, obtained exit 1 and the expected schema-digest refusal, and then removed its scratch
tree. An earlier convenience hash expression also used a .NET `HashData` method unavailable in
this PowerShell runtime; the compatible `Get-FileHash` measurement produced the digests above.

## Transcript integrity

The Session-107 approval used the stored append-only hard gate:

```text
pre-write bytes / physical lines   1,851,572 / 29,882
pre-write SHA-256                  f6f83287...61bbd50f
verified EOF anchor                multi-line / one occurrence
Codex header                       unique at line 29,884
old prefix                         byte-identical
transcript diff                    +79 / -0
last agent                         Codex
```

No monitoring note or correction append was needed.

## Decisions and reasoning

1. **Approve Finding BB unchanged.** The portable-file defect and first-command refusal are
   independently reproduced, and Claude's three-rule implementation is exact.
2. **Keep duplicate root and packet rules.** The duplication is behavior-consistent and avoids
   an unnecessary reopening of settled root policy.
3. **Keep the defense-in-depth pins.** They preserve useful raw-byte diagnostics and match the
   existing packet contract even though they are not refusal-critical.
4. **Close the exact-state loop.** Both agents now approve blob `76976c10...`; no handback remains.
5. **Do not update the public Live-Run README.** This closes a packaging sub-loop but does not
   finish the packet, close a phase, or change the public scientific result.

## Resource and evidence boundary

No fit, checkpoint write, simulator generation, physical rollout, C7 invocation, plan
publication, or pilot/validation/test read occurred. No observation payload, label payload or
checkpoint was opened. Lifetime Protocol-P-related physical rollouts remain 278. The final
`Reproducibility Packet/config/config.json` remains absent.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the owner review, rulings, exact-state approval and loop closure.
- `agents/Codex/Session Summaries/HumanReport107.md` — this report.
- `agents/Codex/README.md` — updated current authority, session index and tree.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the closed packet-documentation state.

Not changed: `Reproducibility Packet/.gitattributes`, either `.gitignore`, the packet README,
the root `.gitattributes`, scripts, tests, protocol, plans, results, checkpoints, Claim Sheet,
director requests, final config, or public Live-Run README.

## Next steps

1. Preserve the closed exact states for packet README, packet `.gitignore`, and packet
   `.gitattributes`; reopen only on a genuine new finding.
2. Keep the disclosed clean-machine checkpoint limitation explicit: tracked JSON consistency is
   auditable, but the tracked sweep and C7 reader cannot be re-driven without the exact original
   checkpoints.
3. Do not infer capacity selection, threshold selection, Stage 2, later-role reads, or final
   configuration from this packaging closure.
4. The next Codex session number is 108. The next regular progress report is Session 112.
