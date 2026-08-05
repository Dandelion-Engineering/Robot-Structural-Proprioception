# Claim Sheet — Robot Structural Proprioception

## How to read this document

This is the **contract** for the project. Every agent reads it at the start of every session, and every result the project produces is measured against it. It is written to be *precise* — the baselines, metrics, and success bars below are exact on purpose — but the section you are reading now is an on-ramp so the precision can be followed as a story rather than reconstructed from the other project files. If you read only this opening and the "Contract at a glance" box, you should be able to state the question, what has already been established, what this project tests, and what its success and failure would each mean.

The body is organized as **fifteen numbered slots**, each a structurally important commitment (domain, problem, claim, constraints, methods, relevance, evaluation, the director's verification path, the build plan, the environment, and the pre-declared shapes of success / failure / inconclusive results, the minimum artifact, and monetization). They can be read straight through as a throughline; each slot arrives to answer a question the previous one opened.

**Read the [Amendments](#amendments) section at the end before acting on any slot.** The sheet changes only by dated amendment, appended and never overwritten; where an amendment revises a slot, the amendment governs and the slot above it is preserved as the recorded prior turn.

### The question, in ordinary language

Most robots run on a fixed factory model of their own body. But real bodies change: parts wear, loosen, heat up, go slightly soft, develop friction or backlash, or lose actuator strength — and the sensors watching all this drift and go noisy. A robot that keeps trusting its original model can become inaccurate or unsafe even while it is still physically capable of the task. Humans cope because we have a dense, distributed sense of our own bodies. This project asks whether giving a robot an analogous stream of **internal structural sensing** — strain and curvature measured along its own limbs, the kind of signal aerospace structures are already instrumented for — lets it do three things a conventional robot sensor suite cannot do as well: **notice** its body or its sensors have changed, **tell what** changed (the structure, an actuator, or the sensor itself), and **keep** as much useful capability as possible instead of treating every deviation as a terminal failure. The whole project runs in simulation; we are not building a sensor, we are testing whether the *information* such a sensor could provide is valuable enough to justify deeper research.

### A few sentences of narrative context

**The prior rung — what the field has already established.** Six adjacent research literatures each solve one piece of this and none solves the whole (surveyed in both agents' Phase 0 Literature Foundations). Robot *self-modeling* can revise a body model from experience, but it senses through joints or cameras and **trusts its sensors**, attributing every discrepancy to the body. *Rapid adaptation* methods (e.g. RMA) compensate for a changed body in a fraction of a second, but they compress every kind of change into a single control latent that is not built to say *what* changed. *Online system identification* re-estimates the robot's dynamics, but a formal result (Wensing–Niemeyer–Slotine, 2024) proves that some structural changes are invisible in principle to joint-space measurements — an identifiability "nullspace." *Structural health monitoring* reads dense strain and vibration to detect and localize damage, but it stops before the control loop. *Soft-robot and tactile proprioception* put distributed sensing inside a robot, but to estimate shape and external contact, not health. *Sensor-fault diagnosis* worries about the sensors, but a residual that flags "measurement disagrees with model" cannot by itself say whether the sensor or the plant moved.

**The current rung — what this project tests.** Laid side by side, those six leave one seam unoccupied: **source attribution.** When the command→sensor→motion relationship shifts, distributed structural sensing might supply the *analytical redundancy* — an extra, physically independent view of the body — that lets a robot separate a structural change from an actuator change from a sensor change, with calibrated uncertainty, and act on that. This project runs the smallest controlled experiment that can tell whether that extra information is actually there and actually useful: on a small simulated compliant manipulator, does adding a few local strain/curvature channels to a matched conventional sensor suite improve held-out attribution of three change types — link-stiffness loss, actuator-gain loss, and encoder corruption — under realistic sensor confounds, and does any attribution gain translate into better recovery of the task?

**What success and failure would mean.** *Success* is a robot's-eye demonstration that a few cheap structural channels carry source-separating information a rich conventional suite does not, and that this buys measurably better recovery — evidence that affordable robots could extend their own safe, useful life by sensing their structure. *Failure* is a clean negative: a well-matched conventional suite recovers the same information and the same performance, so structural hardware is not worth adding for this task. Both are real, publishable outcomes; a clean negative is not a disappointment here, it is a result that saves the field effort. Bounded outcomes in between (structural sensing helps for some change types but not others, or improves diagnosis without improving control) are pre-declared below so a partial win is never reported as a full one.

### Contract at a glance

| | |
|---|---|
| **Target** | A small simulated **compliant two-link manipulator** (flexible links modeled as deformable beams) with four fixed **strain/curvature virtual-gauge stations**, plus conventional proprioception. All in simulation on one desktop. |
| **Inputs (the controlled variable)** | Nested **sensor suites**: **C0** = joint encoders + commanded actuation · **C1** = C0 + a noisy motor-current measurement converted to a nominal torque estimate + one six-axis IMU on the distal link (the richest fixed onboard suite an affordable robot plausibly already carries) · **S** = C1 + four fixed local bending-strain/curvature stations (two per link) · **O** = privileged simulator state (oracle ceiling, never deployable). External pose/vision and direct delivered-torque sensing are excluded from deployable suites. |
| **Baselines** | The **matched conventional suites C0 and C1** (same estimator/controller, structural channels removed); a **simple residual/linear system-ID** estimator (interpretable floor); an **RMA-style recurrent latent** adapter (strong control baseline); an **oracle-fault controller** (ceiling). IT&E/behavior-repertoire recovery is a *reference*, not a matched baseline. |
| **Success bar** | **S** improves held-out four-way macro-F1 over **C1** by ≥0.05 absolute (paired 95% interval excludes zero; every source-class recall difference has a lower 95% bound above −0.02) **and** reduces five-second post-change absolute tracking-error integral by ≥10% (paired 95% interval excludes zero; no safety regression), under realistic drift, thermal, and held-out-severity confounds. Both layers required. |
| **Failure bar** | Matched **C1** with temporal adaptation recovers the same attribution and the same control performance — **S** adds no stable margin. (A clean, publishable negative.) |

With the on-ramp in place, the fifteen slots below make each of these commitments exact.

---

## Slot 1 — Domain and substrate

The project sits in **simulated articulated robotics with structural compliance**, at the boundary where robot control meets structural sensing. The substrate is a deliberately small robot: a **two-link manipulator** whose links are modeled not as rigid bars but as **deformable beams** — slender members that bend measurably under load — so that "strain" is a real, physically meaningful internal state rather than a label attached to a rigid body. The plant starts **planar** (motion in a plane), with torsion introduced on one link only if it proves necessary to separate two fault signatures that a purely planar model leaves degenerate (decided by the feasibility spike, Slot 9).

The signals the robot can access come from four physical sources, all synthesized inside the simulator with credible noise and drift (Slot 7 details the sensor-realism model):
- **Joint encoders** — measured joint position and velocity.
- **Actuator channels** — commanded actuation in every suite and, in C1/S, a noisy motor-current measurement converted with the nominal factory motor constant into an estimated joint torque. The actuator-gain fault acts *after* this measurement, so C1 is not handed the true delivered torque.
- **A body inertial measurement** — one six-axis IMU (specific force and angular rate) mounted on the distal link. External vision/pose and direct delivered-torque sensing are reserved for labels or the oracle suite, never silently included online.
- **Distributed structural "virtual gauges"** — four fixed stations, two per link, providing local in-plane bending strain/curvature. Their exact normalized locations are fixed from the mechanics-only feasibility work before any learned estimator is trained and then held fixed for the matched comparison; placement sweeps are sensitivity analyses, not opportunities to tune on the confirmatory test set. The stations represent what an embedded fiber-Bragg-grating array or bonded strain-gauge set could plausibly measure on a future physical robot.

The data is **self-generated.** A finding from both Phase 0 surveys is that **no openly-licensed dataset exists that simultaneously carries robot commands, joint sensing, distributed structural measurements, multiple body/actuator/sensor faults, and downstream control** — so the project generates its own simulated benchmark and publishes the generation code. This is a resource gap the work partly fills, and a reason the project is naturally simulation-first.

## Slot 2 — Problem being addressed

The prior rung established the seam; this slot states the problem concretely enough that an answer is possible. When a robot's command→sensor→motion relationship changes, the existing tools each fall short in a specific way: self-models trust their sensors, fast-adaptation latents conflate causes, joint-space system-ID is bounded by a proven identifiability nullspace, structural health monitoring stops before control, soft/tactile proprioception senses shape and contact rather than health, and fault diagnosis cannot cleanly separate sensor from plant. The concrete problem is therefore an **information** question before it is a control question:

> On a small simulated compliant manipulator, do a few **local strain/curvature measurements add source-separating information beyond a matched conventional proprioceptive history** — enough to detect and *distinguish* link-stiffness loss (a **structural** change), actuator-gain loss (an **actuator** change), and encoder corruption (a **sensor** change) under realistic sensor confounds — and does any resulting attribution advantage translate into **better closed-loop recovery** of the task?

The problem is framed so that the *sensor suite* is the thing being varied and everything else (the robot, the estimator, the controller, the faults, the trajectories) is held fixed, so that any measured advantage is attributable to the **information the sensors carry**, not to a difference in the algorithm reading them.

## Slot 3 — The transferable claim

The single declarative sentence the project could assert if it succeeds:

> **In a compliant articulated robot, a small set of physically-grounded local structural measurements provides source-separating information about body, actuator, and sensor changes that a matched conventional proprioceptive suite cannot recover — and this attribution advantage translates into faster or safer closed-loop recovery.**

The claim is deliberately narrow: it is *not* "a robot can sense strain" (established), *not* "a robot can adapt after damage" (established), and *not* a claim that the robot "knows what body it has" in general. It is the incremental-information claim, with the downstream-control clause required for the word *advantage* to be earned. Its honest alternatives — the claim holds for some change types but not others, or improves diagnosis without improving control, or fails outright — are pre-declared in Slots 11–13, so the claim can only be asserted at the strength the evidence actually supports.

## Slot 4 — Constraints

The bounds the work lives inside:

- **Simulation only.** No physical components, robot hardware, paid datasets, paid services, or lab equipment. The simulated sensors must represent quantities a *future* physical system could plausibly measure, but the project does not produce a manufacturable sensor.
- **One desktop, free tools.** All work runs on the shared Dandelion desktop (Slot 10). Only free, open-source, **commercial-use-permitting** software, models, and datasets (Standards: Open source and licensing). Any resource with unclear licensing is treated as unusable until resolved.
- **Smallest-sufficient framing.** The *final shipped* solution is the smallest one that meets the success bar (Standards: Efficiency). This governs the shipped artifact, **not** the search: undersized-model null results are evidence about that model, not proof the signal is absent (see the Slot 9 capacity ladder).
- **Safety-of-excitation tension.** Parametric identification needs informative motion, but the aggressive motions that best excite the structural signatures are ones a possibly-damaged robot should avoid. Excitation design (Slot 5) must respect this rather than assume rich, safe excitation is free.
- **Evaluation honesty.** Leakage-free splits (by whole trajectories and fault settings, never by time samples from the same run); realistic sensor pathologies required, not idealized away; environmental/operational confounds present in both healthy and faulty data; every exclusion recorded (Standards: Scientific work).
- **Licensing posture (default, no relaxation requested).** Released code under **MIT** (`LICENSE`), released prose under **CC BY 4.0** (`LICENSE-docs`); scope map in `LICENSING.md`. All dependencies commercial-use-permitting (MuJoCo Apache-2.0, PyElastica MIT — Slot 10). No restrictive-license exception is currently required; if one becomes necessary it will be named with its downstream limits per the Standards.

## Slot 5 — Methods or approach

The method is a **matched sensor-suite ablation**: the same estimator and controller are run on each of the nested suites C0 ⊂ C1 ⊂ S (with O as an oracle ceiling), and the question is what the added structural channels in S buy over the strongest conventional suite C1. Holding the algorithm fixed and varying only the sensors is what makes a measured advantage attributable to *information* rather than to model capacity.

**Fault families (mapping onto the three source classes):**
- **Structure** — localized link-stiffness reduction (a section of a link goes soft).
- **Actuator** — multiplicative delivered-torque/gain loss downstream of the measured motor-current proxy (a joint's drive weakens without C1 receiving the true delivered torque).
- **Sensor** — encoder bias / drift / dropout (a joint sensor lies).

Each is applied one at a time first; then at least one **held-out compound case** (two simultaneous changes) is reserved as an unknown/generalization test. A **healthy** class is always present, and a calibrated **abstain/"unknown"** option is part of the task — forcing every run into a known class would overstate what was learned.

**Estimators / comparators (the baselines, strongest-control included):**
- A **matched temporal estimator** (a compact recurrent or temporal-convolutional model) shared identically across C0, C1, and S — the primary vehicle for the ablation.
- A **simple residual/observer or linear system-ID** baseline — the interpretable floor, so a gain is not just "a bigger black box won."
- An **RMA-style recurrent latent adapter** — the strong control baseline: it receives the same proprioceptive history but optimizes a latent for control, not for labeled attribution. This tests the deflationary hypothesis that conventional history plus temporal adaptation already recovers what structural sensing is supposed to add.
- An **oracle-fault controller** (given the true fault) — the ceiling, never a deployable baseline.
- Intelligent Trial-and-Error / behavior-repertoire recovery (Cully et al.) is a **recovery reference**, not a matched baseline: its large offline behavior map and online search are a different computational contract.

**Excitation.** A family of bounded task trajectories with randomized payload and optional endpoint contact, run under two conditions: an **ordinary-task-only** condition (does normal motion carry enough information?) and a **short safe diagnostic-excitation** condition (a brief, bounded probing motion). The diagnostic-excitation budget is one of the implementation choices Phase 1 leaves open (to be settled early in Phase 2).

**Adaptation / recovery.** Gain-scheduling or model-predictive reconfiguration driven by the *estimated fault distribution*, compared against a control-only latent that receives the same history but no explicit attribution objective — so we can tell whether *knowing what changed* helps control beyond simply *adapting to* it.

**Validation of the signals themselves.** The nominal strain/curvature profiles from the primary simulator are checked against an **independent beam / Cosserat-rod calculation** (Slot 9's fidelity ladder), plus mesh/timestep convergence and sensor noise/drift/placement sweeps. This guards against the failure mode where the structural channel is secretly an algebraic echo of the joint state the baseline already has.

Every method choice here traces to the Phase 0 Literature Foundations (`agents/Claude/Literature Foundation.md`, `agents/Codex/Literature Foundation.md`) and their ledgers, not to memory: the matched-ablation discipline and BIRDy/residual baselines from the identification and FDI literature (Wensing et al.; Dixon; Aghili & Namvar; BIRDy), the RMA comparator from rapid adaptation (Kumar et al.), the sensor-realism targets from embedded-sensing work (Thuruthel; Amirkhani; Sefati), and the environmental-confound discipline from SHM (LANL/Z24).

## Slot 6 — Application and downstream relevance

Why it matters and who it helps. Dandelion builds toward affordable technology for everyday people, and general-purpose robots are moving toward homes and small workplaces where they cannot be recalibrated by a technician after every knock, wear event, or hot afternoon. If a few cheap embedded structural channels carry source-separating information, that is a concrete, affordable route to robots that **extend their own safe, useful life** — noticing and adapting to wear, damage, and sensor drift instead of failing or, worse, continuing confidently while wrong. If instead the result is null or bounded, that is equally valuable in the other direction: it tells builders *not* to spend cost, weight, and complexity on structural sensing where a conventional suite already suffices, and — in the bounded case — maps precisely which change types make the extra sensing worth it. Either way the project feeds a possible larger Dandelion program on mechanically self-aware robots, and does so at the mission's bar: the smallest sufficient sensing that runs on hardware people already own.

## Slot 7 — Materials and evaluation design

This slot is the **team's** confidence path: how *we* will know whether the claim holds. (The director's path is Slot 8.)

**Materials.** A self-generated simulated benchmark: the two-link compliant manipulator, the four sensor suites, the three fault families plus healthy and a held-out compound case, and the trajectory/payload/contact distribution — with the generation code published in the Reproducibility Packet.

**Two metric layers, reported separately** (never collapsed into one aggregate reward, so a diagnosis result is not mistaken for a control result):

*Information / diagnosis layer*
- Four-way (healthy / structure / actuator / sensor) **macro-F1** (primary) and **balanced accuracy**. On known-class confirmatory runs, an abstention is scored as an error in these headline metrics; selective performance is reported separately so rejection cannot inflate the primary score.
- **Per-class precision/recall and confusion matrices**, with special attention to structure-vs-actuator and structure-vs-sensor.
- **Detection delay** after a change, in control cycles and seconds.
- **Localization error** where more than one link/actuator/sensor location is possible.
- **Probability calibration** — Brier score, negative log-likelihood, expected calibration error, and reliability diagrams on the four known classes.
- **Abstention / unknown behavior** — risk-coverage curves; coverage at a pre-registered 5% selective-error ceiling; selective error at 80% coverage; and false-abstention rate on known-class runs. The held-out compound fault is evaluated as unknown/OOD with AUROC, AUPRC, and false-acceptance rate at 95% unknown-detection sensitivity. This keeps class calibration, selective prediction, and unknown detection distinct.
- **Held-out generalization**: performance on held-out severities, trajectories, payloads, noise draws, and at least one held-out fault combination.

*Control layer*
- **Five-second post-change integral of absolute tracking error** (primary control metric).
- **Tracking RMSE and peak error** before the change, immediately after, and after adaptation.
- **Recovery time** and **recovered-performance ratio** relative to the healthy controller.
- **Control effort, saturation time, constraint violations, unsafe excursions.**
- The **paired difference between S and C1** over identical seeds and faults, with uncertainty intervals.

**Splitting and statistics.** Development/pilot, validation, and confirmatory-test partitions are separated by whole trajectories **and** fault settings, never by time samples from the same run. The pilot may size the confirmatory sample and expose method failures, but it may not set the effect-size bars below. Gauge placement, model/hyperparameters, class and abstention thresholds, the post-change analysis window, and the full seed/scenario manifest are frozen in a versioned configuration before confirmatory data are generated. Use at least five independent training seeds and report **paired 95% hierarchical-bootstrap confidence intervals**, resampling whole scenario/trajectory units and training seeds while preserving the C1-vs-S pairing.

**Pre-declared effect-size bars.** "Better than chance" (0.25 balanced accuracy for four classes) is far too weak. For the full success claim, S must improve four-way macro-F1 over C1 by **at least 0.05 absolute**, with the paired 95% interval excluding zero; for every source class, the lower 95% bound on the S-minus-C1 recall difference must also remain above the **−0.02 non-inferiority margin**. S must reduce the **five-second post-change integral of absolute tracking error by at least 10%**, with the paired 95% interval excluding zero, without increasing unsafe excursions or constraint violations. These are project design minima fixed before the pilot; the pilot determines sample size, not what size of result will be called success. Diagnosis-without-control and fault-specific benefits remain Slot-13 outcomes.

## Slot 8 — Director's verification path

This slot is the **director's** confidence path — the hands-on artifact the agents commit, before execution, to build so the director (and anyone who downloads the Reproducibility Packet) can verify the result without reading the Technical Report end to end. It lives *inside* the Reproducibility Packet and is paced into the project, not assembled at the end.

**The artifact:** a small **interactive side-by-side demo**. The director picks a body change from a short menu — *"soften link 2 by 30%," "weaken actuator 1," "bias encoder 1"* — and watches two copies of the robot run the same task at once: one driven by the **conventional suite C1**, one by the **structural suite S**. A live panel shows, for each copy, (a) its current **fault call and confidence** (or an honest *abstain*), and (b) its **tracking-error trace**. The director sees directly whether the structural robot names the right cause **sooner and more often** and **tracks better after the change** — or whether the two are indistinguishable, which is the honest negative shown *as* a result. A scripted, non-interactive version produces the same comparison as a set of 300-DPI figures for the reports.

What the director does: trigger a few changes, watch which robot correctly says *what* happened and *keeps doing the task*, and read the confidence/abstain behavior to see the system decline to guess when the signals are genuinely ambiguous. Naming this artifact now also disciplines the build — the experiment has to be designed so that this comparison is possible and legible. If results reshape what the artifact should show, the Slot-8 entry is amended through the normal protocol.

## Slot 9 — Architecture or build plan

Start with the smallest version that could plausibly work, and pre-commit to escalating **two** ladders — model capacity and physical fidelity — rather than a single fixed design.

**Feasibility spike first (the gate before committing the runtime).** Build the two-link compliant manipulator in **MuJoCo** and test the native mechanics that can actually represent beam bending: the cable/rod elasticity path and, if necessary, a slender 3-D flex with solid elasticity. MuJoCo's generic 1-D flex is primarily an extensible line, so the spike must not assume that "native flex" automatically supplies a bending beam or a strain sensor. Virtual gauges are derived from integrated deformable/rod coordinates and checked against an independent small-deflection beam or Cosserat calculation; they are not copied from a fault parameter or algebraically reconstructed from the corrupted encoder.

The spike passes only if the derived signals are stable under timestep/mesh refinement and the **joint command + conventional signal + gauge histories** contain differential signatures at credible signal-to-noise at realistic (metal-ish) stiffness, not just exaggerated compliance. For structural and actuator faults, at least one fixed gauge channel must show a repeatable fault-minus-healthy response above the modeled measurement-noise floor. An encoder bias is different by construction: it need not physically change the structure under matched open-loop excitation; it must instead be identifiable through a repeatable disagreement between the corrupted encoder and the independently evolved physical/gauge history. This relational signature—not a fictitious encoder-induced strain change—is the gate. The signals must survive a realistic fiber-Bragg-grating-scale floor (~1 µε resolution, ~10 µε/°C thermal cross-sensitivity). Native mechanics are preferred because they add simulator-integrated deformation coordinates rather than an algebraic copy of joint state, reducing (but not eliminating) circularity risk. If the native candidates cannot clear the gate, fall back to a **PyElastica Cosserat-rod** reduced-order model; full FEM stays offline validation only. **No dependency is committed until the spike passes.**

**Physical-fidelity ladder:** native MuJoCo cable/rod or slender-3D-flex candidate → PyElastica reduced-order bridge (fallback) → offline FEM / independent beam calculation (ground-truth and validation, never in the control loop).

**Model-capacity ladder:** (rung 1) a compact recurrent/temporal-convolutional estimator (~10⁴–10⁵ parameters) plus the linear/residual baseline; (rung 2) a larger/deeper recurrent-plus-attention estimator; (rung 3) a probabilistic/ensemble head (e.g. deep ensembles or evidential output) for *calibrated* attribution and honest abstention. Escalate a rung when **(a)** there is partial signal worth strengthening, **or (b)** there is no signal yet but a larger-capacity model could plausibly capture one the smaller model cannot. Stop climbing only when the result **holds across the ladder**, the **hardware ceiling** is genuinely reached, or there is a stated **scientific** reason (not a budget reflex) that a bigger model would not help — and record that reason, because "a bigger model wouldn't help" is itself a claim.

**Hardware ceiling (named).** Single **RTX 5060 Ti, 16 GB VRAM; 32 GB system RAM; one 8-core/16-thread CPU** (Slot 10). The models this project needs are far under that ceiling, so the compute story is *breadth* — many seeds, faults, severities, and noise draws trained and evaluated in parallel — rather than one large network. The ceiling matters most for the simulation/data-generation budget, which the spike will size.

## Slot 10 — Computational and physical environment

- **Machine:** the dedicated Dandelion Engineering AI-agents desktop. OS Windows 11 Home (build 26200); CPU AMD Ryzen 7 8700F (8C/16T); GPU NVIDIA GeForce RTX 5060 Ti, 16 GB VRAM (observed driver 581.95, CUDA 13.0); 32 GB DDR5 RAM; 1 TB NVMe `C:`; external SSD `D:`.
- **Python:** 3.12.10 in the project-root virtual environment `venv`. Every Python/pip call uses `.\venv\Scripts\python.exe` / `.\venv\Scripts\pip.exe` — never bare `python`/`pip`.
- **Core libraries (all commercial-use-permitting; pinned in `requirements.txt` when installed):** MuJoCo (Apache-2.0, native-Windows, primary physics + native sensor suite); PyElastica (MIT, native-Windows, Cosserat validation/fallback); NumPy/SciPy; PyTorch (CUDA build — GPU availability verified at install, not assumed); matplotlib (figures at ≥300 DPI). Offline validation may use a FEM package (e.g. SOFA LGPL-2.1+ or FEniCSx LGPL-3+) *outside* the control loop only.
- **Portability discipline (Standards):** no hard-coded paths; machine-specific paths passed via `argparse` with `required=True`; outputs default to project-relative locations; shared logic in a `utils/` module; the Reproducibility Packet must run end-to-end from a fresh `requirements.txt` install on a copy of the packet folder alone.
- **Note:** JAX-GPU stacks would require WSL2 on this box; the project defaults to native-Windows PyTorch to avoid that dependency unless a concrete need forces a revisit.

## Slot 11 — What would count as success

**Pre-declared before pilot or confirmatory results are observed:**

> The **structural suite S** improves held-out four-way macro-F1 over the **strongest conventional suite C1** by **≥0.05 absolute**, with the paired 95% hierarchical-bootstrap interval excluding zero and the lower 95% bound on every source-class recall difference above the **−0.02 non-inferiority margin**; **and** S reduces the **five-second post-change integral of absolute tracking error by ≥10%**, with its paired 95% interval excluding zero and no increase in unsafe excursions or constraint violations; **and** both results hold **under realistic confounds** (sensor drift, thermal cross-sensitivity, held-out severities/trajectories/payloads). All three conditions are required. A win on diagnosis alone, only for one fault family, only under idealized sensors, or only in-distribution is **not** full success — it is a Slot-13 outcome.

## Slot 12 — What would count as failure

**Pre-declared. A clean failure is a public artifact.** Two distinct failure shapes, and the difference matters:

- **Failure of the hypothesis (the scientifically interesting negative).** The matched conventional suite **C1**, with temporal adaptation, recovers the **same attribution and the same control performance** as **S** — no stable margin — under fair, realistic conditions. Conclusion: for this task and this class of changes, distributed structural sensing adds nothing beyond a rich conventional suite, and the extra hardware is not justified. This is reported plainly as the headline result, with the honesty bound intact.
- **Failure of the method (must be disclosed, not dressed up as a hypothesis result).** The feasibility spike (Slot 9) cannot produce differential fault signatures at credible SNR at all, or the simulator's structural channel turns out to be an algebraic echo of the joint state / leaks the fault label. In that case the simulation cannot fairly test the question, and the project says so rather than reporting a hollow negative or a leaked positive. The remedy is the fidelity ladder (PyElastica fallback) or an amended plant, not a quiet downgrade of the claim.

## Slot 13 — What would count as inconclusive or non-transfer

The "not this, not yet" shapes, pre-declared so partial wins are never reported as full ones:

- **Diagnostic-only.** S improves attribution but the improvement does **not** translate into a control gain over C1. Useful for monitoring; **not** evidence of an adaptive-control advantage. (This is why diagnosis and control metrics are kept separate.)
- **Fault-specific / bounded.** The benefit appears only for some change types — e.g. structural/stiffness changes — and not for actuator or sensor faults. This sharply maps where structural proprioception is worth adding, and is a genuinely useful bounded result.
- **Confound-fragile / inconclusive.** A benefit that exists under idealized conditions but **disappears** under plausible drift, temperature, sensor-placement error, or model mismatch — or that depends on privileged simulator leakage. Reported as inconclusive pending a cleaner test, not as a positive.
- **Excitation-dependent.** Attribution succeeds only under the dedicated diagnostic-excitation condition and fails under ordinary task motion — a practical caveat on when the information is actually available.

## Slot 14 — Minimum public artifact required to conclude

The project is complete only when all four required artifacts exist and meet the Claim Sheet's bar (Standards; Structure section of Project Details):

1. **Technical Report** (LaTeX, field-facing) containing: the question and its position in the six-literature seam; the simulated benchmark and its generation code; the C0/C1/S/O **matched ablation** with matched estimator capacity **and** the within-suite capacity sweep; the **two-layer metrics** (Slot 7) with **pre-declared** bars; held-out and confound results; the **independent validation** of the structural signals; every excluded file/sample/run named with its reason; and the honest headline (positive / bounded / null) at its true strength.
2. **Reproducibility Packet** — self-contained, runs end-to-end from the packet folder alone on a fresh install; includes the generation and analysis code, configs, `DATA.md`, and the **Slot-8 verification artifact**.
3. **Accessible Piece** — the same work for a general reader, honest and jargon-free (the artifact the director shares publicly).
4. **Study Guide** — two passes (Pass 1 at Phase 1 close, Pass 2 at Phase 3 under the no-spoiler rule), director-facing.

Plus the **Live-Run README** resolved from live status (State A) to the concluded landing page (State B).

## Slot 15 — Possible monetization paths

Forward-looking and honest.

- **Succeeds-as-scoped:** no *direct* revenue — the immediate value is a research signal (a validated open reference implementation + benchmark for cheap structural self-sensing) that de-risks a larger program and can seed a reusable, MIT-licensed self-monitoring library other builders adopt. Honest entry: **none identified directly** for the small sim project itself.
- **Succeeds-and-scaled:** a licensable or supported **"structural proprioception" self-monitoring layer** for low-cost robot arms — an estimation module that extends safe service life by detecting and attributing wear/damage/sensor-drift on affordable hardware, consistent with Dandelion's affordable-technology mission.
- **Clean negative:** no monetization path from the result itself, but real value in the negative preventing wasted hardware spend downstream — reputational/credibility value for Dandelion as a team that publishes honest negatives, not a revenue line.

---

# Amendments

Amendments are **appended and dated, never overwritten** (Project Details → *The amendment protocol*). The fifteen slots above are the sheet as originally agreed; each amendment below states what was found, why it changes the path, the new path, and the revised success / failure / non-transfer shapes. Where an amendment revises a slot, **the amendment text governs and the original slot text is preserved above as the recorded prior turn.**

*Numbering note.* Amendment **A1** is not in this file. It amended the shared plant/signal **schema**, not the Claim Sheet, and is recorded in place at `Reproducibility Packet/schema/schema-v1.0.md` → *Amendment A1 — fixed contact/safety role widths (2026-07-19)*. The letter sequence is project-wide, so the first amendment to this document is **A2**.

---

## Amendment A2 — Payload-bounded structural non-transfer (Option C) — 2026-08-04

**Provenance.** Drafted by Claude (Session 75, 2026-08-04) as the default writer, at Codex's Session-74 assignment. Under the review-cycle playbook this amendment is **in force only when both agents have explicitly approved the same state of this file and of `Accessible Claim Sheet.md`.** Until then it is a proposal and no downstream execution follows from it. *(On approval this line is replaced by the two approvals and their date.)*

### A2.1 — What was found

Three executed, jointly approved development measurements, in the order they arrived. All three are **development-only evidence**: every artifact carries a `dev-` hash and none of them can establish or refute the project's hypothesis.

**(i) The Protocol P Stage-A/B/C screen** (executed 2026-08-01, 135 physical rollouts; `Reproducibility Packet/results/protocol_p/stage_abc_screen.json`) returned `CASE_B`. Over the ten reserved structural severities — expressed as *remaining EI*, the fraction of a link's original bending stiffness that survives the fault, so **0.35 is severe damage and 0.90 is mild** — the screening statistic separated a faulted link from a healthy one at 0.35 / 0.40 / 0.45 and failed to at 0.50 through 0.90. The verdict is a conjunction over four development context cells.

**(ii) The Protocol P §9 role-coverage read** (zero rollouts; `results/protocol_p/role_coverage.json`, jointly approved) counted, per split, how many of that split's own reserved structural severities are `TESTABLE`:

```text
dev   {0.50, 0.75}   ->  0        pilot  {0.60, 0.85}   ->  0
val   {0.40, 0.90}   ->  1        test   {0.35, 0.65}   ->  1
```

That result already licensed a **role-coverage-bounded non-transfer shape**, which is in force.

**(iii) The Session-60 payload-conditioning read** (zero rollouts; `results/protocol_p/payload_conditioning.json`, jointly approved) then established that the screen's four cells are **not exchangeable**. Two carry 0.000 kg of distal payload and two carry 0.050 kg, and 50 g roughly halves the structural distance at every rung (ratio 0.4867–0.5366) while the noise floor it is measured against does not move. The screen is therefore a balanced **two-level payload contrast**, and two levels determine a ratio, not a curve.

**(iv) The payload-boundary extension** (`Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md`, canonical sha256 `538ae06b…f33b6a`, frozen and jointly approved before execution) was executed **once**, on 2026-08-04, for 127 physical rollouts. Its result — `Reproducibility Packet/results/payload_boundary_extension/payload_boundary.json`, canonical sha256 `7746372f1adea931722cf547adee36489971493c4e1b5217f588d4c6d1c9aa04` — was independently reconstructed and **explicitly approved by both agents at the same bytes** (Codex Session 73, Claude Session 74). Outcome `X_CASE_EMPTY` (rule R10), `mass_coverage = COMPLETE`, anchor `X_ANCHOR_PASS`, replay gate `PASS`, no exclusions:

```text
distal payload   reserved   own reserved   TESTABLE severities        role
    mass (kg)    by split    severities    (remaining EI)           retained?
      0.025       pilot     {0.60, 0.85}   0.35 0.40 0.45 0.50         no
      0.050        dev      {0.50, 0.75}   0.35 0.40 0.45              no   <- anchor
      0.075       pilot     {0.60, 0.85}   0.35 0.40                   no
      0.100        val      {0.40, 0.90}   0.35                        no
      0.125        val      {0.40, 0.90}   0.35                        no
      0.150       test      {0.35, 0.65}   (empty)                     no
      0.200       test      {0.35, 0.65}   (empty)                     no
```

Three things in that table are the amendment:

1. **The testable set never grows with distal payload mass**, falling from four severities at 0.025 kg to none at all at 0.150 and 0.200 kg. (`MONOTONE` holds over all 21 mass pairs and `PREFIX` at all seven, so this is the artifact's own shape verdict, not a reading of the table.)
2. **No measured mass retains a testable verdict at any severity its own split reserves.** `ROLE_RETAINED` is false at all seven. **Read this together with A2.8 item 2** — the finding holds as an aggregate, but three of the seven margins are inside the instrument's own reproducibility band, and A2 forbids writing it as a universal.
3. **The 1/1 coverage val and test appeared to have was established at masses neither split reserves.** The screen ran only at 0.000 kg and 0.050 kg, and the assignment reserves both of those for **dev** (`payload_dev_nominal`, `payload_dev_0p050kg`). Val's single surviving severity (0.40) is sub-threshold at both masses val reserves; test's (0.35) is sub-threshold at both masses test reserves. Measured at the payloads each split actually carries, the role coverage of (ii) is **0 / 0 / 0 / 0**.

**Scope, stated before any of this is used.** These are development verdicts at **one** environment profile (`env_dev_iso25c`), **one** contact profile (`contact_dev_none`), **one** trajectory (`trajectory_dev_diagnostic_b`), **one** probe (0.10 N peak, ramp fraction 0.25), and only the seven masses listed. A verdict about a severity that val or test reserves is a *development-context* verdict about a scalar severity, **not** a claim that the severity is testable or untestable in that split's own contexts (carried limitation 74). Point 3 above is a statement about payload mass, not about val's or test's environments.

### A2.2 — Why this changes the path

The sheet as written treats **distal payload mass as a generalization axis**: Slot 7 lists held-out payloads among the confounds a successful result must survive, and Slot 11 requires success to hold under them. That framing silently assumes the structural signal is roughly comparable across the payload range — an assumption nothing had tested, because every `TESTABLE` verdict the project holds was obtained at 0.000 kg and 0.050 kg.

It is false. Payload is not a nuisance axis the signal survives; it is the **strongest single determinant of whether the signal exists at all** among the factors measured so far, and at the two masses the confirmatory test split reserves it removes the signal entirely at every severity on the ladder. A confirmatory design that pooled across payload would report a structural null that is substantially a statement about payload mass, and would report it as though it were a statement about structural sensing.

### A2.3 — The new path: Option C, and why A and B are not available

Three options were pre-registered before the measurement, and the frozen extension document pinned in advance which outcome licenses which. At `X_CASE_EMPTY` (§9.5, *What each complete-coverage outcome licenses*):

- **Option A — move the severity grid down below the measured boundary.** **Not licensed by this result.** An empty testable set means no severity this extension measured clears those masses, so no lower grid is nameable from the evidence in hand; the across-mass intersection is empty as well. This is a statement about licensing, not a prohibition: a lower grid remains available in principle, but it would require a **new prospective measurement**, pre-registered and executed the same way, and it is not authorized here.
- **Option B — compress the payload ladder to a verified band.** **Not licensed.** Option B's cap is the maximum mass of the longest ascending initial prefix in which *every* mass retains its own role. The prefix breaks at the very first mass: 0.025 kg (pilot) misses its cheapest own reserved severity, 0.60, by **18.2% of that mass's own threshold**. There is no non-empty qualifying prefix, so there is no cap to take.
- **Option C — keep both ladders and pre-register a payload-bounded non-transfer shape.** **Licensed, and only with the empty masses named explicitly.** This is the path adopted.

**What Option C changes.** The pre-declared shapes in Slots 11, 12 and 13, and the reporting requirement in Slot 7. Those revisions are A2.4–A2.7 below.

**What Option C does not change, stated exactly because it determines whether existing work survives.** No reserved structural severity moves. No payload level moves. No split assignment, trajectory, environment, contact profile, or fault-grid entry moves. Because the assignment's fault expansion order (healthy → structure → actuator → sensor, per split) makes every later ordinal — and therefore every later seed — depend on the size of `grid["structure"]["severities"]`, and A2 changes no entry in it, **this amendment shifts no seed ordinal and by itself invalidates no already-generated development data.** No `archive/` move is required by A2, and none is performed by it. *(This corrects an expectation carried in both agents' continuity notes since Session 33, when A2 was still expected to add a severity band. It no longer does. If the delivered development set is superseded for some other reason, that is a separate decision, requires its own authorization, and carries its own archive and exclusion-trail obligations.)*

### A2.4 — Revised Slot 11 (success)

**The success bar itself is unchanged.** Every threshold, interval, margin, and seed requirement in Slot 11 stands exactly as pre-declared: ≥0.05 absolute macro-F1 improvement of S over C1 with the paired 95% hierarchical-bootstrap interval excluding zero; the lower 95% bound on every source-class recall difference above −0.02; a ≥10% reduction in the five-second post-change integral of absolute tracking error with its paired interval excluding zero and no safety regression; all under realistic confounds; all three conditions required. **A2 does not loosen, tighten, restate, or reinterpret any of them.**

What A2 adds is a **scope bound on the sentence a success would license**:

> A confirmatory success is stated **only over the distal payload masses at which it is measured**, and the headline sentence must name that range. It may not be extended to heavier payloads by interpolation, extrapolation, or silence. Where the confirmatory result is reported pooled across payload, the payload-stratified result (A2.7) is reported beside it, and the pooled number is never the only number given.

### A2.5 — Revised Slot 12 (failure)

Slot 12's two failure shapes are unchanged. A2 adds the **boundary between them and the new Slot-13 shape**, which the original sheet had no reason to draw:

> **A structural null is a hypothesis failure only where the structural signal was screened as present.** Slot 12's "failure of the hypothesis" — C1 with temporal adaptation recovering the same attribution and the same control performance as S — may be claimed for a fault family, severity, and payload region **only where the development screen found the signal detectable at all**. A null obtained in a region where the screening instrument is itself blind is **not** evidence that structural sensing adds nothing there; it is the Slot-13 payload-bounded non-transfer shape of A2.6. Reporting the second as the first would be reporting the absence of an instrument as the absence of an effect.

This boundary is deliberately conservative in the direction that costs the project its preferred headline: it makes a clean negative **harder** to claim, not easier.

### A2.6 — Revised Slot 13: the new payload-bounded non-transfer shape

Added to Slot 13's list, beside the role-coverage-bounded shape already in force, and pre-declared before any confirmatory result exists:

> **Payload-bounded non-transfer.** At the fixed development context of the payload-boundary extension, the structural screening signal is monotonically attenuated by distal payload mass, and at 0.150 kg and 0.200 kg — the two masses the confirmatory **test** split reserves — no severity on the ten-value reserved ladder is detectable at all. It is therefore pre-registered that:
>
> **(a)** If the confirmatory read returns no S-over-C1 advantage on the structural fault family, the result is reported as **payload- and severity-bounded non-transfer**, not as a hypothesis failure, and the report names the payload masses and severities at which the development screen had already found no detectable signal. Such a result establishes neither the hypothesis nor its failure for structural changes at payloads or severities where the screen retained signal.
>
> **(b)** If the confirmatory read returns an S-over-C1 advantage on the structural family, the claim is bounded to the payload masses at which it was measured, per A2.4.
>
> **(c)** In either direction, the reported result must state that the development screen found the structural signal payload-conditional, and must not attribute the attenuation to a mechanism. None is identified (A2.8).
>
> **(d)** This shape is about the **structural** fault family only. It makes no pre-declaration about the actuator or sensor families, whose signatures the payload-boundary extension did not measure.

### A2.7 — Revised Slot 7: payload-stratified reporting

Slot 7's materials, metric layers, splitting rule, statistics, and pre-declared effect-size bars are unchanged. A2 adds one reporting requirement, which follows directly from keeping the payload ladder as a generalization axis rather than compressing it:

> The confirmatory S-versus-C1 comparison on the **structural** fault family is reported **stratified by distal payload mass** as well as pooled. The stratified table is part of the minimum artifact (Slot 14) and appears in the Technical Report. Stratification is a **reporting** requirement: it does not create new per-stratum success bars, does not license selecting a stratum after seeing results, and does not change the pre-declared pooled bars of Slot 11. Its purpose is that a reader can see whether a pooled result is carried or masked by payload.

### A2.8 — Claim-strength limits this amendment carries

These are binding on A2's own wording, on the Technical Report, and on the Accessible Piece. They are recorded here so that no later write-up has to reconstruct them.

**1. The existence of an empty payload region is established. Its boundary is not resolved.** The extension document fixed a reproducibility band **before** any extension datum existed: `tau_anchor = 0.10` of a cell's own threshold, the margin §9.3 declared too small to constrain a verdict, derived from the executed screen's own published margins. Six of the seventy measured rungs sit inside that band, and the two that separate 0.125 kg from 0.150 kg are the two closest to a threshold anywhere in the grid:

```text
0.125 kg  remEI 0.35   +2.123%  TESTABLE       <- the only surviving rung at 0.125
0.150 kg  remEI 0.35   -4.141%  SUB_THRESHOLD  <- the whole reason 0.150 is empty
```

A single-rung flip sweep over all seventy rungs — counting only landings that do not break `PREFIX` or `MONOTONE` by construction, since an ill-shaped landing measures the flip rather than the result — finds **exactly four** well-shaped flips that change any reported quantity, and **all four are inside the band**. Under none of them does the outcome leave `X_CASE_EMPTY`, and under none of them does Option B acquire a cap.

So the two statements have different strengths and A2 keeps them apart. **"Some measured payload region has no testable reserved severity" is robust:** leaving `X_CASE_EMPTY` would require *both* heaviest masses to become non-empty at once, and 0.200 kg — the mass furthest from non-empty — misses by **22.6% of its own threshold**, well outside the band. **"The empty masses are exactly 0.150 and 0.200 kg" is not robust.** No write-up may promote 0.150 kg into a physical cutoff.

**2. "No mass retains its own role" holds as an aggregate; three of the seven are close calls.** Option B's unavailability is robust — the prefix breaks at 0.025 kg, 18.2% away, and no in-band flip repairs it. But the *universal* sentence is weaker than it looks: three of the seven role losses are inside the same 10% band, and a single well-shaped flip at any one of them would make that mass retain its role (without changing the outcome or the Option-B cap):

```text
0.050 kg  dev   cheapest own rung 0.50   -5.013%
0.100 kg  val   cheapest own rung 0.40   -5.746%
0.150 kg  test  cheapest own rung 0.35   -4.141%
```

Write the aggregate finding, not the universal one: **no measured mass retained its own reserved severity, and at three of the seven the margin was inside the instrument's own reproducibility band.**

**3. No curve, and no mechanism.** Seven levels are seven levels. No functional form in payload mass may be fitted through them, and any interpolation shown for illustration must be labelled as illustration wherever it appears. The mechanism of the attenuation is **not identified**: a linearized modal estimate places the diagnostic probe roughly two orders of magnitude below the lowest elastic mode (0.8 Hz against 77.34 Hz), which rules a resonance explanation out and puts nothing in its place. The plant is compiled with zero gravity, so distal payload acts purely as **tip inertia** — it applies no static load, produces no sag, and consumes none of the A1 strain envelope at rest.

**4. The seven per-mass nulls are not independent.** They are common-random-number-matched by construction (extension §5). This is deliberate and no analysis may forget it.

**5. Neither audit re-derived the harmonic coefficient vectors from raw time series.** Both agents independently reconstructed everything downstream of the persisted coefficients. The raw gauge traces were not persisted, so the step from time series to coefficients is covered by the replay gate, the anchor's agreement with the executed screen, and the X8 liveness check — and by nothing either audit did. Two independent reconstructions must not be allowed to imply coverage they do not have.

**6. All of this is development evidence.** The result artifact's own authority field reads: *"DEVELOPMENT ONLY: ineligible for confirmatory analysis; cannot change Protocol P outcome or role-coverage counts."* A2 changes the project's pre-declared shapes; it does not change any executed Protocol P verdict or role-coverage count, and it asserts no research result.

### A2.9 — What this amendment does not do

Named explicitly so that approving A2 cannot be read as approving anything downstream of it. A2 does **not** authorize, and nothing in it may be cited as authorizing: a second invocation of the payload-boundary extension or any further payload measurement; replacement of the assignment; coherent regeneration of any dataset; materialization of the final `config/config.json`; any pilot, validation, or test generation or outcome read; any confirmatory work; or any change to Protocol P v2.3.3, whose specification loop is closed. Each of those requires its own separately explicit authorization after this two-file review loop closes.
