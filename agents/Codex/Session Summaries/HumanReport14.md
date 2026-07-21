# Human Report 14 — Codex

**Current Date and Time:** 2026-07-20 19:51 PDT

**Agent:** Codex · **Session:** 14 · **Project phase:** Phase 2 — Execution

---

## Summary

This session discharged the one open Codex review obligation, found and corrected a
narrow trace-semantics defect in Claude's new recovery-seam regression, and then
implemented the real MuJoCo endpoint-contact extraction required before any
optional-contact pilot can be designed.

The multi-step recovery mechanism itself survived independent reproduction: a fixed,
localized actuator attribution drives sustained inverse-gain compensation and restores
delivered torque, while an otherwise-identical unlocalized/infinite-uncertainty diagnosis
stays nominal and leaves delivery degraded; a structural attribution sustains the bounded
global derate. The handed-off test fixture nevertheless claimed to latch the time of first
detection while actually rewriting `detection_time_s` to the current decision time at
every step. Codex added a resettable first-detection latch and a regression that pins the
correct schema-§D semantics. Codex explicitly approves the edited test state and returned
it to Claude; that review loop remains open pending Claude's genuine owner re-review.

The plant now has an optional, development-only endpoint contact profile. It adds one
explicit MuJoCo contact pair between the distal link-2 endpoint segment and a horizontal
plane; every other cable geometry remains collision-disabled. `CablePlant` filters all
reported contacts to that pair, extracts finite constraint-force truth with
`mujoco.mj_contactForce`, populates A1's `[tip_contact_force_n, tip_contact_active]` role,
and drives the seventh privileged safety flag. Omitting the contact CLI option preserves
the previous `[0,0]` no-contact default. This makes contact-profile screening possible;
it does not choose a contact grid, run a pilot, or freeze `config.json`.

The full Reproducibility Packet now passes **139 tests**. The endpoint-contact increment
is explicitly approved by Codex and handed to Claude for genuine first review. No phase
closed, no Claim-Sheet amendment was written, and the public Live-Run README remains
unchanged after the required lean-heartbeat check.

## What was accomplished

1. **Completed the AgentPrompt startup workflow.** Read `AgentPrompt.md`, all of
   `Project Details/Project Details.md`, Codex's continuity file, every concluded-chat
   `Summary.md` involving Codex, and the complete active Phase-2 transcript before
   replying. Re-read the in-force `Claim Sheet.md`, Claude's latest Human Report 14,
   and the review-cycle playbook before touching the handed-off seam regression.

2. **Reconciled current state against continuity.** The live repository was clean at
   `1cfa0ec Claude Session 14`. Claude had genuinely approved Codex's residual/linear-ID
   baseline without edits, closing that first-review loop, and had opened one new loop on
   `tests/test_recovery_seam.py`. Live git/chat state therefore superseded Codex's
   Session-13 continuity file where it was stale.

3. **Genuinely reviewed the recovery-seam regression.** Read the test against the Claim
   Sheet's separation of diagnosis and control metrics, schema §D's estimator-output
   semantics, and the jointly approved `EstimatorCommandPolicy`, recovery controller,
   online loop, and real `CablePlant` implementation. The artifact's scope statement is
   honest: fixed estimator outputs plus torque assertions make it a mechanism/interface
   regression, not a learned-attribution, `J_5s`, tracking-recovery, or safety result.

4. **Reproduced the seam independently.** Built a separate fixed estimator rather than
   invoking Claude's test helpers and drove 12 real online steps. Seven independent
   checks passed:
   - localized actuator attribution requested exactly 2× nominal at the weakened joint;
   - the plant's downstream 0.5 gain restored delivered torque to nominal;
   - the unlocalized/infinite-uncertainty arm stayed exactly nominal;
   - that arm's delivered torque remained at 0.5× nominal;
   - the structural arm applied the 0.75 global derate;
   - first-detection time stayed latched in the independent fixture; and
   - the active actuator arm did not saturate.

5. **Corrected the seam fixture's detection-time defect.** Claude's fixture documentation
   said `detection_time_s` latched at the first decision, but its four-step output was
   `[0.000, 0.002, 0.004, 0.006]`. Schema §D defines this field as the time the change was
   first flagged. Codex added an initialized/resettable latch and a regression asserting
   that every output preserves `0.0 s`. The focused seam file remains **4 passed**. The
   edit does not change controller output because the current controller ignores detection
   time, but it prevents the fixture from producing a semantically false estimator trace
   or contaminating later delay-aware seam work.

6. **Appended the review handoff safely.** Read the physical UTF-8 tail, appended the
   Session-14 review against a unique multi-line tail block, re-read the written tail,
   and confirmed the exact header appears once and is physically last. Codex explicitly
   approves the edited seam state and asks Claude for genuine owner re-review; later use
   or silence is not approval.

7. **Read the Reproducibility Packet playbook and A1 contract before plant changes.**
   The implementation had to stay self-contained, CLI-reachable, fail loud, and preserve
   the privileged/deployable boundary. A1 fixes the two contact fields and the seventh
   safety flag; exact numeric contact-profile values remain development/config choices.

8. **Verified the installed contact API against first-party documentation.** The project
   venv contains MuJoCo 3.10.0. Its official function reference defines
   `mj_contactForce` as the six-dimensional contact force/torque extractor in the contact
   frame, and the official MJCF reference supports explicit named geom pairs. Codex added
   this source and its project use to `agents/Codex/references.md`.

9. **Added an isolated endpoint-contact model profile.** `CableModelConfig` now carries
   an explicit `endpoint_contact_enabled` switch and plane height. When enabled,
   `model_xml` adds one horizontal plane and one predefined pair between that plane and
   the expanded distal `L2_G{last}` endpoint segment. All ordinary cable geoms retain
   `contype=0/conaffinity=0`; the role therefore cannot silently aggregate contacts from
   another link or segment.

10. **Implemented force extraction and fail-loud guards.** `_contact_state()` preserves
    `[0,0]` and rejects any unexpected contact when the profile is disabled. In the
    enabled profile it requires valid endpoint/plane handles, rejects any reported geom
    pair other than the intended pair, obtains a six-component wrench for each contact
    point, rejects non-finite values, and sums the finite 3-D force magnitudes. It records
    activity when at least one intended contact exists and rejects negative/non-finite
    final role values.

11. **Connected contact truth to safety without crossing the sensor boundary.** The
    already-approved `_safety_flags` path consumes `contact_state[0]` from privileged
    plant truth, so `tip_contact_force_exceeded` now evaluates real contact force. No
    contact field was added to `ObservedRecord`; deployable suites can see contact only
    through its physical consequences in motion/strain.

12. **Exposed a portable development CLI.** `make_mujoco_plant_trace.py` now accepts
    `--endpoint-contact-plane-z-m`. Supplying it enables the optional profile and includes
    the setting in the development config hash; omitting it retains the collision-disabled
    default. The packet runbook gives a copy-paste 0.2 s development command and labels
    the 0.498 m plane height as a fixture, not a frozen scenario value.

13. **Added and ran contact regression coverage.** The focused test drives a real
    100-step contact rollout, requires at least one active contact and force above a
    deliberately low test limit, and proves the seventh safety-flag series is exactly
    `tip_contact_force_n > limit`. The development run produced four endpoint-plane
    contact points at the final state and a 0.844 N peak aggregate force.

14. **Ran a portable CLI smoke.** A temporary, separately indexed 10-step privileged
    trace was generated through the public CLI and loaded back through
    `PrivilegedRecord`. It contained 10 active contact samples, a 0.574 N peak force, and
    no contact-force safety trip under the unchanged 5 N development threshold. The
    temporary directory was verified under the system temp root and removed afterward.

15. **Updated packet-facing documentation.** The runbook's test description, optional
    contact command/output paths, and current-boundary section now reflect real extraction
    while keeping the central honesty boundary loud: no contact profile/grid is frozen or
    piloted, and this is not a research result.

16. **Appended the endpoint-contact handoff safely.** The second Session-14 chat header
    was appended after re-reading the physical tail; both Session-14 headers occur exactly
    once and the contact handoff is physically last. Codex explicitly approves the exact
    implementation/test/CLI/runbook state and requests Claude's first review.

17. **Completed the public heartbeat check.** Left the root `README.md` unchanged. The
    contact work closes a development prerequisite and opens review, but it is not a
    finished public artifact, phase transition, frozen design, pilot result, or finding on
    the research hypothesis. A per-session log entry would make the lean public log less
    useful.

## Important decisions and reasoning

- **Correct the fixture even though controller behavior was unchanged.** A test fixture
  that violates the schema it claims to exercise can be copied into future evaluation
  work and turn into a silent metric defect. The edit is narrow and load-bearing for
  detection delay, so it belongs in the active review cycle rather than being carried as
  a cosmetic nit.
- **Use one explicit contact pair instead of enabling collision globally.** A1's field is
  specifically endpoint contact. Enabling every cable geom would allow link/plane events
  to enter a field named `tip_contact_force_n` and would change the plant far beyond the
  optional endpoint condition. One predefined pair makes the physical scope executable.
- **Use MuJoCo constraint force, not a penetration proxy.** Penetration depth or endpoint
  motion would be solver- and stiffness-dependent proxies. The simulator already exposes
  the solved contact wrench; recording its force is the direct privileged truth required
  by the schema.
- **Sum contact-point force magnitudes and state that convention.** A box-plane endpoint
  can generate multiple contact points. Summing finite 3-D magnitudes produces a
  conservative aggregate burden for the safety flag and is explicitly documented so the
  eventual frozen config can accept or amend it rather than inheriting an implicit rule.
- **Keep the contact profile disabled by default.** Existing mechanics/pilot artifacts
  were collision-free. The new capability must not silently change them or make their
  historical metrics irreproducible.
- **Do not run the optional-contact pilot yet.** Extraction unblocks profile design, but
  the actual plane/contact grid must be screened across healthy and every fault scenario,
  then reconciled with the still-open severity/onset and config choices. A single 0.498 m
  fixture cannot be promoted into that design.

## Challenges and how they were handled

- **The first collision-enablement attempt produced no contacts.** Codex initially added
  a plane and changed the already-compiled distal geom's collision bits. The focused test
  correctly failed: even as the endpoint moved through the plane, no candidate contact
  pair was generated. Codex diagnosed this by inspecting geom ids, bodies, collision bits,
  endpoint motion, and `data.ncon` across several plane heights. The implementation was
  replaced with an explicit MJCF `<contact><pair .../></contact>` between the expanded
  distal geom and plane. The same test then passed and the profile produced only the
  intended geom pair.
- **A combined verification shell returned exit 1 after successful tests.** The full
  suite had already reported 139 passed; the nonzero status came from truncating CLI-help
  output through a pipeline, not from pytest or compilation. Codex reran CLI help and
  `compileall` independently, captured both exit codes as zero, and did not misreport the
  pipeline artifact as a code failure.
- **The schema amendment text still carries historical proposal wording.** Live chat and
  both agents' continuity state establish A1 as jointly in force. This session did not
  alter the schema contract or reopen A1; it implemented the already-approved endpoint
  truth the amendment requires. The live thread remains the approval record.

## Files created

- `agents/Codex/Session Summaries/HumanReport14.md`

## Files updated

- `Reproducibility Packet/scripts/utils/cable_mechanics.py`
- `Reproducibility Packet/scripts/utils/cable_plant.py`
- `Reproducibility Packet/scripts/make_mujoco_plant_trace.py`
- `Reproducibility Packet/tests/test_cable_plant.py`
- `Reproducibility Packet/tests/test_recovery_seam.py`
- `Reproducibility Packet/README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/references.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

The root `README.md` and `.gitignore` are unchanged after their required checks. No
generated trace or temporary smoke artifact was retained.

## Verification performed

- Recovery-seam focused tests: **4 passed**.
- Independent recovery-seam reproduction: **7/7 properties passed** over 12 real steps.
- Contact/plant focused tests: **8 passed**.
- Full Reproducibility Packet: **139 passed**.
- `compileall -q` over packet scripts and tests: passed.
- `make_mujoco_plant_trace.py --help`: passed.
- Portable contact trace CLI smoke: passed and round-tripped through `PrivilegedRecord`.
- Active-chat Session-14 19:44 header count: exactly 1.
- Active-chat Session-14 19:51 header count: exactly 1 and physically last.
- `git diff --check`: clean apart from line-ending warnings.

## Next steps / pending actions

1. Claude must genuinely owner-re-review the edited `tests/test_recovery_seam.py` state.
   If Claude accepts the detection-time diagnosis and implementation, it must explicitly
   approve that exact state before the loop closes.
2. Claude must genuinely first-review the endpoint-contact implementation, focused test,
   portable CLI, and packet wording. If Claude edits, Codex must re-open the exact files
   and genuinely owner-re-review before that loop closes.
3. After review, design and screen an actual optional-contact profile/grid across healthy,
   structural, actuator, and sensor scenarios. Preserve the 0.498 m plane as a development
   extraction fixture unless evidence supports it; do not freeze it by inertia.
4. Build the evaluation-sized development comparison that separates exact actuator
   delivery compensation from `J_5s` tracking recovery and privileged safety. Keep the
   existing eight-step seam test below a tracking claim.
5. Before confirmatory generation, settle validation-sized healthy/known calibration
   roles, per-suite probability calibration, severity/onset grids, non-load-bearing sensor
   constants, split/leakage/storage/role-hash audits, contact cases, and then freeze/hash
   the complete config.
6. Learned temporal attribution and the RMA-style latent remain post-freeze. The central
   C1-vs-S diagnosis-and-control question remains unanswered.

Next regular Codex progress report: Session 16 unless a Claim-Sheet amendment or phase
transition triggers one earlier.
