# Claim Sheet — Robot Structural Proprioception

## How to read this document

This is the **contract** for the project. Every agent reads it at the start of every session, and every result the project produces is measured against it. It is written to be *precise* — the baselines, metrics, and success bars below are exact on purpose — but the section you are reading now is an on-ramp so the precision can be followed as a story rather than reconstructed from the other project files. If you read only this opening and the "Contract at a glance" box, you should be able to state the question, what has already been established, what this project tests, and what its success and failure would each mean.

The body is organized as **fifteen numbered slots**, each a structurally important commitment (domain, problem, claim, constraints, methods, relevance, evaluation, the director's verification path, the build plan, the environment, and the pre-declared shapes of success / failure / inconclusive results, the minimum artifact, and monetization). They can be read straight through as a throughline; each slot arrives to answer a question the previous one opened.

### The question, in ordinary language

Most robots run on a fixed factory model of their own body. But real bodies change: parts wear, loosen, heat up, go slightly soft, develop friction or backlash, or lose actuator strength — and the sensors watching all this drift and go noisy. A robot that keeps trusting its original model can become inaccurate or unsafe even while it is still physically capable of the task. Humans cope because we have a dense, distributed sense of our own bodies. This project asks whether giving a robot an analogous stream of **internal structural sensing** — strain and curvature measured along its own limbs, the kind of signal aerospace structures are already instrumented for — lets it do three things a conventional robot sensor suite cannot do as well: **notice** its body or its sensors have changed, **tell what** changed (the structure, an actuator, or the sensor itself), and **keep** as much useful capability as possible instead of treating every deviation as a terminal failure. The whole project runs in simulation; we are not building a sensor, we are testing whether the *information* such a sensor could provide is valuable enough to justify deeper research.

### A few sentences of narrative context

**The prior rung — what the field has already established.** Six adjacent research literatures each solve one piece of this and none solves the whole (surveyed in both agents' Phase 0 Literature Foundations). Robot *self-modeling* can revise a body model from experience, but it senses through joints or cameras and **trusts its sensors**, attributing every discrepancy to the body. *Rapid adaptation* methods (e.g. RMA) compensate for a changed body in a fraction of a second, but they compress every kind of change into a single control latent that is not built to say *what* changed. *Online system identification* re-estimates the robot's dynamics, but a formal result (Wensing–Niemeyer–Slotine, 2024) proves that some structural changes are invisible in principle to joint-space measurements — an identifiability "nullspace." *Structural health monitoring* reads dense strain and vibration to detect and localize damage, but it stops before the control loop. *Soft-robot and tactile proprioception* put distributed sensing inside a robot, but to estimate shape and external contact, not health. *Sensor-fault diagnosis* worries about the sensors, but a residual that flags "measurement disagrees with model" cannot by itself say whether the sensor or the plant moved.

**The current rung — what this project tests.** Laid side by side, those six leave one seam unoccupied: **source attribution.** When the command→sensor→motion relationship shifts, distributed structural sensing might supply the *analytical redundancy* — an extra, physically independent view of the body — that lets a robot separate a structural change from an actuator change from a sensor change, with calibrated uncertainty, and act on that. This project runs the smallest controlled experiment that can tell whether that extra information is actually there and actually useful: on a small simulated compliant manipulator, does adding a few local strain/curvature channels to a matched conventional sensor suite improve held-out attribution of three change types — link-stiffness loss, actuator-gain loss, and encoder corruption — under realistic sensor confounds, and does any attribution gain translate into better recovery of the task?

**What success and failure would mean.** *Success* is a robot's-eye demonstration that a few cheap structural channels carry source-separating information a rich conventional suite does not, and that this buys measurably better recovery — evidence that affordable robots could extend their own safe, useful life by sensing their structure. *Failure* is a clean negative: a well-matched conventional suite recovers the same information and the same performance, so structural hardware is not worth adding for this task. Both are real, publishable outcomes; a clean negative is not a disappointment here, it is a result that saves the field effort. Bounded outcomes in between (structural sensing helps for some change types but not others, or improves diagnosis without improving control) are pre-declared below so a partial win is never reported as a full one.

### Contract at a glance

| | |
|---|---|
| **Target** | A small simulated **compliant two-link manipulator** (flexible links modeled as deformable beams) with a few embedded **strain/curvature virtual gauges**, plus conventional proprioception. All in simulation on one desktop. |
| **Inputs (the controlled variable)** | Nested **sensor suites**: **C0** = joint encoders + commanded actuation · **C1** = C0 + motor current/torque + a body IMU/endpoint measurement (the richest suite an affordable robot plausibly already carries) · **S** = C1 + a small fixed set of local strain/curvature channels · **O** = privileged simulator state (oracle ceiling, never deployable). |
| **Baselines** | The **matched conventional suites C0 and C1** (same estimator/controller, structural channels removed); a **simple residual/linear system-ID** estimator (interpretable floor); an **RMA-style recurrent latent** adapter (strong control baseline); an **oracle-fault controller** (ceiling). IT&E/behavior-repertoire recovery is a *reference*, not a matched baseline. |
| **Success bar** | **S** beats the strongest conventional suite **C1** on held-out four-way (healthy/structure/actuator/sensor) attribution by a statistically stable margin, **and** yields a practically meaningful downstream control gain (post-change tracking error / recovery), under realistic drift, thermal, and held-out-severity confounds. Both layers required. |
| **Failure bar** | Matched **C1** with temporal adaptation recovers the same attribution and the same control performance — **S** adds no stable margin. (A clean, publishable negative.) |

With the on-ramp in place, the fifteen slots below make each of these commitments exact.

---

## Slot 1 — Domain and substrate

The project sits in **simulated articulated robotics with structural compliance**, at the boundary where robot control meets structural sensing. The substrate is a deliberately small robot: a **two-link manipulator** whose links are modeled not as rigid bars but as **deformable beams** — slender members that bend measurably under load — so that "strain" is a real, physically meaningful internal state rather than a label attached to a rigid body. The plant starts **planar** (motion in a plane), with torsion introduced on one link only if it proves necessary to separate two fault signatures that a purely planar model leaves degenerate (decided by the feasibility spike, Slot 9).

The signals the robot can access come from four physical sources, all synthesized inside the simulator with credible noise and drift (Slot 7 details the sensor-realism model):
- **Joint encoders** — measured joint position and velocity.
- **Actuator channels** — commanded torque, and (in the richer suites) measured motor current/torque.
- **A body inertial/endpoint measurement** — a body-mounted IMU or an endpoint pose measurement a conventional research robot could carry.
- **Distributed structural "virtual gauges"** — a small fixed set of local strain and curvature readings taken at points along the links, representing what an embedded fiber-Bragg-grating array or bonded strain-gauge set could plausibly measure on a future physical robot.

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

**Fault families (mapping one-to-one onto the three source classes):**
- **Structure** — localized link-stiffness reduction (a section of a link goes soft).
- **Actuator** — actuator torque/gain loss (a joint's drive weakens).
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
- Four-way (healthy / structure / actuator / sensor) **macro-F1** and **balanced accuracy**.
- **Per-class precision/recall and confusion matrices**, with special attention to structure-vs-actuator and structure-vs-sensor.
- **Detection delay** after a change, in control cycles and seconds.
- **Localization error** where more than one link/actuator/sensor location is possible.
- **Calibration** of fault probabilities — Brier score, negative log-likelihood, and reliability diagrams — **including the abstain/unknown option**.
- **Held-out generalization**: performance on held-out severities, trajectories, payloads, noise draws, and at least one held-out fault combination.

*Control layer*
- **Tracking RMSE and peak error** before the change, immediately after, and after adaptation.
- **Recovery time** and **recovered-performance ratio** relative to the healthy controller.
- **Control effort, saturation time, constraint violations, unsafe excursions.**
- The **paired difference between S and C1** over identical seeds and faults, with uncertainty intervals.

**Splitting and statistics.** Split by whole trajectories and fault settings, not by time samples from the same run (guards against the estimator learning simulator fingerprints). Report paired comparisons with uncertainty intervals over matched seeds.

**Where the bars come from.** "Better than chance" (0.25 balanced accuracy for four classes) is far too weak a bar. Exact numeric success thresholds are **set after a pilot** estimates the overlap of the fault signatures — pre-declared *before* the confirmatory runs, then locked (Slots 11–13). A defensible advantage requires **both** a statistically stable diagnosis improvement over the strongest conventional suite **and** a practically meaningful downstream control gain; diagnosis-without-control is explicitly a Slot-13 outcome, not success.

## Slot 8 — Director's verification path

This slot is the **director's** confidence path — the hands-on artifact the agents commit, before execution, to build so the director (and anyone who downloads the Reproducibility Packet) can verify the result without reading the Technical Report end to end. It lives *inside* the Reproducibility Packet and is paced into the project, not assembled at the end.

**The artifact:** a small **interactive side-by-side demo**. The director picks a body change from a short menu — *"soften link 2 by 30%," "weaken actuator 1," "bias encoder 1"* — and watches two copies of the robot run the same task at once: one driven by the **conventional suite C1**, one by the **structural suite S**. A live panel shows, for each copy, (a) its current **fault call and confidence** (or an honest *abstain*), and (b) its **tracking-error trace**. The director sees directly whether the structural robot names the right cause **sooner and more often** and **tracks better after the change** — or whether the two are indistinguishable, which is the honest negative shown *as* a result. A scripted, non-interactive version produces the same comparison as a set of 300-DPI figures for the reports.

What the director does: trigger a few changes, watch which robot correctly says *what* happened and *keeps doing the task*, and read the confidence/abstain behavior to see the system decline to guess when the signals are genuinely ambiguous. Naming this artifact now also disciplines the build — the experiment has to be designed so that this comparison is possible and legible. If results reshape what the artifact should show, the Slot-8 entry is amended through the normal protocol.

## Slot 9 — Architecture or build plan

Start with the smallest version that could plausibly work, and pre-commit to escalating **two** ladders — model capacity and physical fidelity — rather than a single fixed design.

**Feasibility spike first (the gate before committing the runtime).** Build the two-link compliant manipulator in **MuJoCo** using its native **flex/deformable** elements and test whether the flex outputs expose **stable, auditable virtual-gauge strain/curvature signals** that show **differential fault signatures at credible signal-to-noise** — i.e. a link-stiffness loss, an actuator-gain loss, and an encoder bias must produce *distinguishable* gauge responses under matched excitation, at strain magnitudes that survive a realistic noise floor (fiber-Bragg-grating scale: ~1 µε resolution, ~10 µε/°C thermal cross-sensitivity), and — importantly — at realistic (metal-ish) link stiffness, not just exaggerated compliance. Native flex is preferred not only for being one engine: its deformation degrees of freedom are integrated from applied forces and are therefore **physically independent** of the joint coordinates the baseline already sees, which lowers the risk that "strain" is a circular re-encoding of the baseline's own inputs. If native flex cannot clear that gate, fall back to a **PyElastica Cosserat-rod** reduced-order model (also independent, force-driven DOFs); full FEM stays offline validation only. **No dependency is committed until the spike passes.**

**Physical-fidelity ladder:** native MuJoCo flex → PyElastica reduced-order bridge (fallback) → offline FEM / independent beam calculation (ground-truth and validation, never in the control loop).

**Model-capacity ladder:** (rung 1) a compact recurrent/temporal-convolutional estimator (~10⁴–10⁵ parameters) plus the linear/residual baseline; (rung 2) a larger/deeper recurrent-plus-attention estimator; (rung 3) a probabilistic/ensemble head (e.g. deep ensembles or evidential output) for *calibrated* attribution and honest abstention. Escalate a rung when **(a)** there is partial signal worth strengthening, **or (b)** there is no signal yet but a larger-capacity model could plausibly capture one the smaller model cannot. Stop climbing only when the result **holds across the ladder**, the **hardware ceiling** is genuinely reached, or there is a stated **scientific** reason (not a budget reflex) that a bigger model would not help — and record that reason, because "a bigger model wouldn't help" is itself a claim.

**Hardware ceiling (named).** Single **RTX 5060 Ti, 16 GB VRAM; 32 GB system RAM; one 8-core/16-thread CPU** (Slot 10). The models this project needs are far under that ceiling, so the compute story is *breadth* — many seeds, faults, severities, and noise draws trained and evaluated in parallel — rather than one large network. The ceiling matters most for the simulation/data-generation budget, which the spike will size.

## Slot 10 — Computational and physical environment

- **Machine:** the dedicated Dandelion Engineering AI-agents desktop. OS Windows 11 Home (build 26200); CPU AMD Ryzen 7 8700F (8C/16T); GPU NVIDIA GeForce RTX 5060 Ti, 16 GB VRAM (observed driver 581.95, CUDA 13.0); 32 GB DDR5 RAM; 1 TB NVMe `C:`; external SSD `D:`.
- **Python:** 3.12.10 in the project-root virtual environment `venv`. Every Python/pip call uses `.\venv\Scripts\python.exe` / `.\venv\Scripts\pip.exe` — never bare `python`/`pip`.
- **Core libraries (all commercial-use-permitting; pinned in `requirements.txt` when installed):** MuJoCo (Apache-2.0, native-Windows, primary physics + native sensor suite); PyElastica (MIT, native-Windows, Cosserat validation/fallback); NumPy/SciPy; PyTorch (CUDA build — GPU availability verified at install, not assumed); matplotlib (figures at ≥300 DPI). Offline validation may use a FEM package (e.g. SOFA LGPL-2.1+ or FEniCSx LGPL-3+) *outside* the control loop only.
- **Portability discipline (Standards):** no hard-coded paths; machine-specific paths passed via `argparse` with `required=True`; outputs default to project-relative locations; shared logic in a `utils/` module; the Reproducibility Packet must run end-to-end from a fresh `requirements.txt` install on a copy of the packet folder alone.
- **Note:** JAX-GPU stacks would require WSL2 on this box; the project defaults to native-Windows PyTorch to avoid that dependency unless a concrete need forces a revisit.

## Slot 11 — What would count as success

**Pre-declared, before any confirmatory result is observed** (exact numeric thresholds fixed after the Slot-7 pilot, then locked):

> The **structural suite S** beats the **strongest conventional suite C1** on held-out four-way (healthy/structure/actuator/sensor) attribution by a **statistically stable margin** (paired over matched seeds, with uncertainty intervals excluding no-effect), **and** S yields a **practically meaningful downstream control gain** over C1 — lower post-change tracking error and/or faster recovery by the pre-registered margin — **and** both hold **under realistic confounds** (sensor drift, thermal cross-sensitivity, held-out severities/trajectories/payloads). All three conditions are required. A win on diagnosis alone, or a win only under idealized sensors, or a win only in-distribution, is **not** success — it is a Slot-13 outcome.

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

*This Claim Sheet is a Phase-1 draft handed to Codex for review (Claude is the default writer; Codex is the required reviewer). It synthesizes both agents' Phase 0 Literature Foundations against the five convergence points settled in `chats/Claude-Codex/Phase 0 Coordination/Summary.md`. The companion **Accessible Claim Sheet** and **Study Guide Pass 1** are produced in the Phase-1-close window, once this technical sheet is agreed, so they translate the settled contract rather than a draft in review.*
